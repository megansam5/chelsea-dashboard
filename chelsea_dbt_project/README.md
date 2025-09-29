# 📊 Chelsea DBT Project

This folder contains the **dbt project** for transforming and modeling data on top of the PostgreSQL database.

## 📋 Overview

The dbt project builds **staging** and **mart** models on the PostgreSQL database hosted on an AWS RDS instance.  
It assumes that the database schema has already been created and seeded using the instructions in the [`database`](../database) folder.

## 🛠️ Prerequisites

- **AWS RDS (PostgreSQL)** database running.
- Database initialized and seeded as described in the [`database`](../database) folder.
- [dbt](https://docs.getdbt.com/docs/get-started/installation) installed (via pip or Homebrew).

## ⚙️ Setup

1. Ensure the `.env` file is already set up in the project root with the following variables (as defined in the database setup):

   ```env
   # Database Configuration
   DB_HOST=<the-RDS-host-address>
   DB_PORT=<the-RDS-port-number>
   DB_NAME=<the-RDS-name>
   DB_USER=<the-RDS-username>
   DB_PASSWORD=<the-RDS-password>
   ```

2. Configure dbt to connect to the PostgreSQL database.  
   Run:

   ```bash
   dbt init
   ```

   or update your existing `profiles.yml` file (usually found in `~/.dbt/`) with:

   ```yaml
   chelsea_dbt_project:
     target: dev
     outputs:
       dev:
         type: postgres
         host: "{{ env_var('DB_HOST') }}"
         port: "{{ env_var('DB_PORT') | int }}"
         user: "{{ env_var('DB_USER') }}"
         password: "{{ env_var('DB_PASSWORD') }}"
         dbname: "{{ env_var('DB_NAME') }}"
         schema: public
   ```

3. Test the connection:

   ```bash
   dbt debug
   ```

4. Run the dbt models (staging and marts):
   ```bash
   dbt run
   ```

## 📁 Project Structure

- `models/staging/` contains staging models that clean and structure raw data.
- `models/marts/` contains mart models used for analytics and reporting.
