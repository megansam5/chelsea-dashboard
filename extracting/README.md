# Chelsea Data Extraction

## 📋 Overview

This module is responsible for extracting chelsea data from an API, parsing the extracted content, and loading the final cleaned data. The extraction process involves:

1. Fetching the API data, as multiple JSON files.
2. Transforming the data into a dataframe and loading as a CSV into the correct S3 bucket, or files if locally.
3. Inserting this data into a Postgres database.

## 🛠️ Prerequisites

- **Python** installed
- **Local PostgreSQL** database running.
- Get an **API Key** for the 'football-data.org' API by following the instructions [here](https://www.football-data.org/client/register) (free tier)
- Read the Prequrequisites and Setup section of the following READMEs to create the tables and views in the database:

1. [database/README.md](../database/README.md)
2. [chelsea_dbt_project/README.md](../chelsea_dbt_project/README.md)

Optional (for running on the cloud):

- **Docker** installed.
- Setup **ECR** repository to store the daily extraction docker image.
- **AWS RDS (PostgreSQL)** database running.

## ⚙️ Setup

Create a `.env` file and fill with the following variables

```env
# API Details
API_URL='https://api.football-data.org/'
API_KEY=<your-api-key>

# Database Configuration
DB_HOST=<the-RDS-host-address>
DB_PORT=<the-RDS-port-number>
DB_NAME=<the-RDS-name>
DB_USER=<the-RDS-username>
DB_PASSWORD=<the-RDS-password>

# If run on cloud:

# AWS Configuration
AWS_ACCESS_KEY=<your_aws_access_key>
AWS_SECRET_KEY=<your_aws_secret_access_key>

# ECR Configuration
ECR_REGISTRY_ID=<id_of_ecr_repo_to_store_image>
ECR_REPO_NAME=<name_of_ecr_repo_to_store_image>
IMAGE_NAME=chelsea-extraction-image  # or any other appropriate name

# S3 Bucket Configuration
BUCKET_NAME=<s3_bucket_name>

```

### 💻 Running Locally

The Chelsea Data Extraction can be ran locally by:

1. Creating and activating virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
3. Run the entire process locally (fetching, cleaning, and uploading to database):
   ```bash
   python3 pipeline_local.py
   ```

### ☁️ Pushing to the Cloud (optional)

To deploy the overall cloud infrastructure the daily extractor must be containerised and hosted on the cloud:

1. Make sure you have the Docker application running in the background
2. Dockerise and upload the application:
   ```bash
   bash dockerise.sh
   ```
   This will:
   - Authenticate your aws credentials with docker
   - Create the docker image
   - Tag the docker image
   - Upload tagged image to the ECR repository
