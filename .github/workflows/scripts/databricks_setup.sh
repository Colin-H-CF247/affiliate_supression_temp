# Setup databricks cli
python -m pip install --upgrade pip
pip install databricks-cli

# Upload cluster setup script, training notebook and dataset build notebook
databricks fs cp --overwrite ./databricks/cluster_setup.sh dbfs:/Shared/dbx/cluster_init_scripts/template_cluster_setup.sh
databricks fs cp --overwrite ./databricks/notebook_jobs/train_and_register_model.ipynb dbfs:/Shared/train_jobs/template_train_job.ipynb
databricks fs cp --overwrite ./databricks/notebook_jobs/build_dataset.ipynb dbfs:/Shared/dataset_build_jobs/template_dataset_job.ipynb


# Create secret scope
databricks secrets delete-scope --scope $DBUTILS_SCOPE || true
databricks secrets create-scope --scope $DBUTILS_SCOPE --initial-manage-principal users
databricks secrets put --scope $DBUTILS_SCOPE --key $SP_CLIENT_ID_KEY --string-value "$SP_CLIENT_ID"
databricks secrets put --scope $DBUTILS_SCOPE --key $SP_SECRET_KEY --string-value "$SP_SECRET"
databricks secrets put --scope $DBUTILS_SCOPE --key $SP_TENANT_ID_KEY --string-value "$SP_TENANT_ID"