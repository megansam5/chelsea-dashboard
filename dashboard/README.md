# 📈 Chelsea Dashboard

## 📋 Overview

This folder contains the **Streamlit dashboard** for the Chelsea Data Project.  
The dashboard provides interactive insights into Chelsea FC’s matches, standings, squad, and performance metrics.

### Features:

- 🏠 **Overview** – Team summary, recent matches, performance charts
- 📊 **League Standings** – Interactive tables with filters
- ⚽ **Matches** – Past & upcoming fixtures with competition filters
- 👥 **Squad** – Player roster with filtering & analytics
- 📈 **Performance Analytics** – Goals over time, results distribution, home vs away analysis, and squad demographics

## 🛠️ Prerequisites

- Read the Prequrequisites and Setup section of the following READMEs to create the tables and views in the database and fill them with data:

1. [database/README.md](../database/README.md)
2. [chelsea_dbt_project/README.md](../chelsea_dbt_project/README.md)
3. [extracting/README.md](../extracting/README.md)

- **Python** installed

OPtions (for pushing to cloud):

- **EC2** deployed from running [Terraform](../terraform/README.md)
- **PEM Key** generated from running [Terraform](../terraform/README.md)
- **ec2.env** file generated from running [Terraform](../terraform/README.md)

## ⚙️ Setup

Create a `.env` file with the following environment variables:

```
# Database Configuration
DB_HOST=<the-RDS-host-address>
DB_PORT=<the-RDS-port-number>
DB_NAME=<the-RDS-name>
DB_USER=<the-RDS-username>
DB_PASSWORD=<the-RDS-password>

# If pushing to cloud:

# AWS Configuration
AWS_ACCESS_KEY=<your_aws_access_key>
AWS_SECRET_KEY=<your_aws_secret_access_key>
REGION=eu-west-2

# EC2 Configuration
KEY_PATH=<path-to-PEM-key>
```

### 💻 Running Locally

The dashboard can be ran locally by:

1. Creating and activating virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
3. Running the dashboard:
   ```bash
   streamlit run main.py
   ```

### ☁️ Transferring to EC2 (**Optional**)

As part of deploying the overall cloud infrastructure, the dashboard files must be transferred to the EC2 and then run in the background:

1. upload and upload the application:

   ```bash
   bash upload_dashboard.sh
   ```

   This will:

   - Delete existing dashboard and nltk folders
   - Transfer the dashboarding files
   - Create and activate python virtual environment
   - Install requirements
   - Run the streamlit dashboard

2. You can exit the EC2 terminal by pressing `CTRL + c` buttons together

3. You can look at the dashboard by typing the EC2 dns address in the generated ec2.env file and adding `:8501` to the end e.g:  
   `ec2-35-176-239-59.eu-west-2.compute.amazonaws.com:8501`
