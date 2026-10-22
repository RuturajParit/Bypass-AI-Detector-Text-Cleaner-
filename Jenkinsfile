```groovy
stage('Run on Kubernetes') {
    steps {
        sh '''
            set -eu

            kubectl delete job text-cleaner --ignore-not-found=true --wait=true

            sed "s|image: .*|image: $IMAGE:$BUILD_NUMBER|" \
                k8s/job.yaml | kubectl apply -f -

            kubectl wait --for=condition=complete \
                job/text-cleaner --timeout=180s

            echo "=== CLEANER OUTPUT ==="
            kubectl logs job/text-cleaner

            mkdir -p output

            echo "=== COPYING RESULT ==="

            POD=$(kubectl get pods \
                -l job-name=text-cleaner \
                -o jsonpath='{.items[0].metadata.name}')

            kubectl run text-cleaner-copy \
                --image=busybox:1.36 \
                --restart=Never \
                --command -- sleep 300

            kubectl wait --for=condition=Ready \
                pod/text-cleaner-copy --timeout=120s

            kubectl cp \
                "$POD:/app/output/clean_assignment.txt" \
                output/clean_assignment.txt \
                -c cleaner 2>/dev/null || true

            if [ ! -s output/clean_assignment.txt ]; then
                echo "Direct copy unavailable; retrieving file through helper pod."
                kubectl exec text-cleaner-copy -- \
                    sh -c 'mkdir -p /tmp/result'
                kubectl cp \
                    "$POD:/app/output/clean_assignment.txt" \
                    output/clean_assignment.txt
            fi

            kubectl delete pod text-cleaner-copy \
                --ignore-not-found=true --wait=false

            echo "=== RESULT FILE ==="
            cat output/clean_assignment.txt
        '''
    }
}
