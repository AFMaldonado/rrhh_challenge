from google.cloud import storage, secretmanager
import mysql.connector
import fastavro
import os
from secret_manager import SecretManagerGCP
import json

# Google Cloud Storage Configuration
bucket_name = 'backup-table'
client = storage.Client()
bucket = client.get_bucket(bucket_name)

# Cloud SQL Connection Configuration
def get_mysql_connection():
    project_id = "proyect-pma"

    # Initialize SecretManagerGCP with project_id
    secret_manager = SecretManagerGCP(project_id)

    # Retrieve MySQL credentials from Google Cloud Secrets
    secret_mysql = secret_manager.get_secret("mysql-creds")
    secret_mysql_dic = json.loads(secret_mysql)
    host_con = secret_mysql_dic['host']
    port_con = int(secret_mysql_dic['port'])
    username = secret_mysql_dic['user']
    password = secret_mysql_dic['pass']
    database_name = "rrhh"

    # Configure Cloud SQL connection
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host_con,
        database=database_name
    )

def backup_table(table_name):
    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Query to retrieve all data from the table
    query = f"SELECT * FROM {table_name}"

    # Execute the query
    cursor.execute(query)

    # Get column names
    column_names = [column[0] for column in cursor.description]

    # Get table data
    table_data = cursor.fetchall()

    # Convert data to a list of dictionaries
    table_data_dicts = []
    for row in table_data:
        # Convert values to strings
        row_dict = {col_name: str(value) if value is not None else None for col_name, value in zip(column_names, row)}
        table_data_dicts.append(row_dict)

    # Define Avro file name
    avro_filename = f"{table_name}.avro"

    # Write data to Avro file
    with open(avro_filename, 'wb') as avro_file:
        fastavro.writer(avro_file, schema={"type": "record", "name": table_name, "fields": [{"name": col_name, "type": ["null", "string"]} for col_name in column_names]}, records=table_data_dicts)

    # Upload Avro file to Google Cloud Storage
    blob = bucket.blob(avro_filename)
    blob.upload_from_filename(avro_filename)

    # Delete local Avro file
    os.remove(avro_filename)

    cursor.close()
    connection.close()

def main(request):
    try:
        # List of table names in your Cloud SQL database
        tables = ['departments', 'hired_employees', 'jobs']

        # Backup each table
        for table_name in tables:
            backup_table(table_name)

        return "Validation that it ran well"
    except Exception as e:
        error_message = str(e)
        print(f"The error that occurred is: {error_message}")
        return "Error"
