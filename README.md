# Package [![Coverage Status](./.reports/coverage/coverage-badge.svg)](./.reports/coverage/index.html)

[__API Documentation__](https://ds-core-docs.azurewebsites.net/datascience_core.html) | [__Confluence User Guide__](https://247group.atlassian.net/wiki/spaces/247PROD/pages/2818539589/Data+Science+Core)

## Tech Stack

- MLStudio (Azure) - Responsible for hosting deployed services and the model registry
- Databricks - Responsible for running training jobs and building datasets
- Github Actions - Triggers all pipeline steps (orchestrator)
- Python + pyproject.toml - Implementation language and the package build tool responsible for making the model available locally


