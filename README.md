## General Overview

This repository contains code for managing human resources data, including uploading CSV files to a database, calculating hiring metrics, and restoring database tables from backups. Below is a general overview of each functionality:

### 1. API (Cloud Run)

- This functionality enables the uploading of CSV files containing department, job, and hired employee data to a MySQL database using FastAPI. It leverages services such as API Gateway, Cloud Run, Secret Manager, and Docker for deployment and secure credential management.

### 2. Sending Historic Data to an API (Cloud Run)

- A cloud run job is used to retrieve historical CSV data from Google Cloud Storage and send it to an API endpoint using the requests module. The CSV files include information about departments, jobs, and hired employees.

### 3. Backup Tables to Google Cloud Storage (Cloud Function)

This script enables the backup of tables from a MySQL database to Google Cloud Storage using the Avro file format

### 4. Restoring Tables from Backups (Cloud Function)

- Another cloud function is responsible for restoring database tables (departments, jobs, and hired employees) from Avro backup files stored in Google Cloud Storage to a MySQL database.

Each functionality serves a specific purpose in efficiently managing and processing human resources data. Various Google Cloud services such as Cloud Storage, Secret Manager, Cloud Functions, API Gateway, and Cloud Run are utilized for secure storage, deployment, and data processing.
