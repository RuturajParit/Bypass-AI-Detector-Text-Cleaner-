
stage('Run on Kubernetes') {
    steps {
        sh '''
            set -eu

            echo "=== REMOVE PREVIOUS JOB ==="
            kubectl delete job text-cleaner \
                --ignore-not-found=true --wait=true

            echo "=== DEPLOY CURRENT IMAGE ==="
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

                    if echo "$LOGS" | grep -q 'CLEANER_EXIT_CODE='; then
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
                echo "ERROR: Kubernetes pod was not created."
                kubectl get pods
                exit 1
            fi

            echo "=== RETRIEVE CLEANED FILE ==="
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
