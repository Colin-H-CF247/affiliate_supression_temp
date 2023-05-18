config_name=$1
job_name=$2

databricks jobs create --json-file ./deployment_config/databricks/$config_name
databricks jobs run-now --job-name $job_name