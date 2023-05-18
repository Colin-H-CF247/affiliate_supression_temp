# Stop script if any command fails
set -e

ENDPOINT_NAME="template-example"

# Try and create an endpoint. If it already exists, update it.
endpoint_status=$(( az ml online-endpoint create --name $ENDPOINT_NAME --json deployment_config/online_endpoint/online_endpoint.yml 2>&1))

if endpoint_status
then
  echo "Endpoint already exists. Updating it."
  az ml online-endpoint update --name $ENDPOINT_NAME
fi

# Now that we know the endpoint is there, we can deploy a service to it.
az ml online-deployment create --name blue --endpoint $ENDPOINT_NAME -f deployment_config/online_endpoint/deployment_aks.yml --all-traffic

# confirm endpoint exists
az ml online-endpoint show -n $ENDPOINT_NAME


# check if create was successful - either still provisioning, succeeded or failed
endpoint_status=`az ml online-endpoint show --name $ENDPOINT_NAME --query "provisioning_state" -o tsv`
echo $endpoint_status
if [[ $endpoint_status == "Succeeded" ]]
then
  echo "Endpoint created successfully"
else
  echo "Endpoint creation failed"
  exit 1
fi

# Once we know the endpoint is in a stable state, we can check to see if the deployment to it was successful.
deploy_status=`az ml online-deployment show --name blue --endpoint $ENDPOINT_NAME --query "provisioning_state" -o tsv`
echo $deploy_status
if [[ $deploy_status == "Succeeded" ]]
then
  echo "Deployment completed successfully"
else
  echo "Deployment failed"
  exit 1
fi

# Lets confirm that the deployment is actually running.  We need a sample request to test the endpoint with.
az ml online-endpoint invoke --name $ENDPOINT_NAME --request-file deployment_config/sample-request.json

# supress printing secret
set +x


ENDPOINT_KEY=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -o tsv --query primaryKey)
set -x
SCORING_URI=$(az ml online-endpoint show -n $ENDPOINT_NAME -o tsv --query scoring_uri)

curl --request POST "$SCORING_URI" --header "Authorization: Bearer $ENDPOINT_KEY" --header 'Content-Type: application/json' --data @endpoints/online/model-1/sample-request.json


# check that the response was received and logged
az ml online-deployment get-logs --name blue --endpoint $ENDPOINT_NAME






