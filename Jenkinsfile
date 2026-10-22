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
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER .'
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

                    kubectl delete job text-cleaner \
                        --ignore-not-found=true --wait=true

                    sed "s|image: .*|image: $IMAGE:$BUILD_NUMBER|" \
                        k8s/job.yaml | kubectl apply -f -

                    kubectl wait --for=condition=complete \
                        job/text-cleaner --timeout=180s

                    echo "=== CLEANER LOGS ==="
                    kubectl logs job/text-cleaner

                    mkdir -p output

                    echo "=== RETRIEVING CLEANED FILE ==="

                    POD=$(kubectl get pods \
                        -l job-name=text-cleaner \
                        -o jsonpath='{.items[0].metadata.name}')

                    kubectl cp \
                        "$POD:/app/output/clean_assignment.txt" \
                        output/clean_assignment.txt || {
                            echo "Could not retrieve output from completed pod."
                            exit 1
                        }

                    test -s output/clean_assignment.txt

                    echo "=== OUTPUT PREVIEW ==="
                    head -20 output/clean_assignment.txt
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
    }
}
