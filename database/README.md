# 🗄️ The Database

This folder contains the schema and script to create the tables in the database.

## 📋 Overview

The database created is a PostgreSQL database, which can be ran locally or hosted on an AWS RDS instance.

## 🛠️ Prerequisites

- **PostgreSQL** database running locally.

Optional:

- **AWS RDS (PostgreSQL)** database running.

## ⚙️ Setup

1. Create a `.env` file and fill with the following variables
   ```env
   # Database Configuration
   DB_HOST=<the-RDS-host-address>
   DB_PORT=<the-RDS-port-number>
   DB_NAME=<the-RDS-name>
   DB_USER=<the-RDS-username>
   DB_PASSWORD=<the-RDS-password>
   ```
2. Initialise and the database using:
   ```bash
   bash create_db.sh
   ```
   This will initialise the database according to the schema.sql file.
