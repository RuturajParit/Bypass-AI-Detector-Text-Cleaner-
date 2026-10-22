pipeline {
    agent any

    environment {
        IMAGE = 'ruturajparit/cca2-text-cleaner'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    set -eu
                    python3 -m compileall -q src
                    test -f src/cleaner.py
                    test -f examples/assignment.txt
                    echo "Build checks passed."
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -eu
                    docker build -t "$IMAGE:$BUILD_NUMBER" .
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        set -eu
                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKER_USER" --password-stdin
                        docker push "$IMAGE:$BUILD_NUMBER"
                        docker logout
                    '''
                }
            }
        }

        stage('Run on Kubernetes') {
            steps {
                sh '''
                    set -eu

                    echo "=== DELETE PREVIOUS JOB ==="
                    kubectl delete job text-cleaner \
                        --ignore-not-found=true --wait=true

                    echo "=== DEPLOY NEW JOB ==="
                    sed "s|image: .*|image: $IMAGE:$BUILD_NUMBER|" \
                        k8s/job.yaml | kubectl apply -f -

                    echo "=== WAIT FOR CLEANER OUTPUT ==="
                    POD=""

                    for i in $(seq 1 60); do
                        POD=$(kubectl get pods \
                            -l job-name=text-cleaner \
                            -o jsonpath='{.items[0].metadata.name}' \
                            2>/dev/null || true)

                        if [ -n "$POD" ]; then
                            LOGS=$(kubectl logs "$POD" 2>/dev/null || true)
                            echo "$LOGS"

                            if echo "$LOGS" | grep -q \
                                'Output file: output/clean_assignment.txt'; then
                                break
                            fi

                            if echo "$LOGS" | grep -q \
                                'CLEANER_EXIT_CODE='; then
                                if ! echo "$LOGS" | grep -q \
                                    'CLEANER_EXIT_CODE=0'; then
                                    echo "Cleaner failed."
                                    exit 1
                                fi
                            fi
                        fi

                        sleep 2
                    done

                    if [ -z "$POD" ]; then
                        echo "ERROR: Kubernetes pod not found."
                        kubectl get pods
                        exit 1
                    fi

                    echo "=== RETRIEVE OUTPUT ==="
                    mkdir -p output

                    kubectl cp \
                        "$POD:/app/output/clean_assignment.txt" \
                        output/clean_assignment.txt

                    test -s output/clean_assignment.txt

                    echo "=== OUTPUT PREVIEW ==="
                    head -20 output/clean_assignment.txt

                    echo "=== CLEANER LOGS ==="
                    kubectl logs "$POD"
                '''
            }
        }

        stage('Archive Result') {
            steps {
                archiveArtifacts(
                    artifacts: 'output/clean_assignment.txt',
                    fingerprint: true
                )
            }
        }
    }

    post {
        always {
            echo 'CCA2 pipeline execution finished.'
        }
        success {
            echo 'SUCCESS: Image built, pushed, deployed, and output archived.'
        }
        failure {
            echo 'FAILURE: Check the stage logs above.'
        }
    }
}
