az ml compute create --file ./conf/batch_endpoint/compute_target.yml
az ml batch-endpoint create --file ./conf/batch_endpoint/batch_endpoint.yml
az ml batch-deployment create --file ./conf/batch_endpoint/deployment_batch_endpoint.yml --set-default

# Test the batch endpoint
az ml batch-endpoint invoke -n "${AZURE_BATCH_ENDPOINT_NAME}" --input-file ./conf/sample_request.json --output-file ./tmp/output.json

cat /tmp/output.json
