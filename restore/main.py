from google.cloud import storage, secretmanager
import mysql.connector
import fastavro
import os
from api.secret_manager import SecretManagerGCP
import json

# Configuration for Google Cloud Storage
bucket_name = 'backup-table'
client = storage.Client()
bucket = client.get_bucket(bucket_name)

# Configuration for Cloud SQL connection
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

    # Configure the connection to Cloud SQL
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host_con,
        database=database_name
    )

def get_avro_schema_columns(avro_schema):
    # Extract column names and types from Avro schema
    columns = []
    for field in avro_schema['fields']:
        column_name = field['name']
        column_type = field['type']
        columns.append(f"{column_name} {avro_type_to_mysql_type(column_type)}")
    return columns

def avro_type_to_mysql_type(avro_type):
    if isinstance(avro_type, list) and len(avro_type) == 2 and 'null' in avro_type:
        # If it's a union type with 'null', use the non-'null' type
        avro_type = next(t for t in avro_type if t != 'null')

    # Map Avro types to MySQL types
    type_mapping = {
        'int': 'INT',
        'string': 'VARCHAR(255)',  # Adjust the length as needed
        'long': 'BIGINT',
        'float': 'FLOAT',
        'double': 'DOUBLE',
        # Add more mappings as needed
    }
    
    # Return the corresponding MySQL type or default to VARCHAR(255)
    return type_mapping.get(avro_type, 'VARCHAR(255)')

def restore_table(table_name):
    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Obtain the Avro backup file from Google Cloud Storage
    backup_filename = f"{table_name}.avro"
    blob = bucket.blob(backup_filename)
    blob.download_to_filename(backup_filename)

    # Read data from the Avro file
    with open(backup_filename, 'rb') as avro_file:
        avro_reader = fastavro.reader(avro_file)
        schema = avro_reader.schema
        records = list(avro_reader)

    # Extract columns and types from Avro schema
    columns_definition = ', '.join(get_avro_schema_columns(schema))

    # Drop table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    # Create the table if it doesn't exist
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")

    # Insert data into the table
    for record in records:
        columns = ', '.join(record.keys())
        values = ', '.join(['%s'] * len(record))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(query, list(record.values()))

    # Commit and close the connection
    connection.commit()
    cursor.close()
    connection.close()

    # Delete the local backup file
    os.remove(backup_filename)

def main(request):
    try:
        # List of table names in your Cloud SQL database
        tables = ['departments', 'hired_employees', 'jobs']

        # Restore each table from its backup
        for table_name in tables:
            restore_table(table_name)

        return "Validation that it ran well"
    except Exception as e:
        error_message = str(e)
        print(f"The error that occurred is: {error_message}")
        return "Error"
