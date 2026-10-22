stage('Run on Kubernetes') {
    steps {
        sh '''
            set -eu

            kubectl delete job text-cleaner --ignore-not-found=true --wait=true

            sed "s|image: .*|image: $IMAGE:$BUILD_NUMBER|" k8s/job.yaml | kubectl apply -f -

            kubectl wait --for=condition=complete job/text-cleaner --timeout=180s

            echo "=== CLEANER LOGS ==="
            kubectl logs job/text-cleaner

            mkdir -p output

            echo "=== SAVING OUTPUT ==="
            kubectl logs job/text-cleaner > output/clean_assignment.txt

            test -s output/clean_assignment.txt
        '''
    }
}
