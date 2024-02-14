import csv
import codecs
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from src.secret_manager import SecretManagerGCP
import json

# Project ID for Google Cloud
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

# Initialize the FastAPI application
app = FastAPI()

def upload_csv_and_insert(file, table_name, columns):
    """
    Uploads a CSV file and inserts its data into the specified MySQL table.

    Args:
        file (UploadFile): The CSV file to upload and insert.
        table_name (str): The name of the MySQL table to insert the data into.
        columns (list): The list of column names for the table.

    Returns:
        dict: A dictionary containing a success message or an error message.
    """
    batch_size = 1000  # Size of the batch
    
    try:
        # Read the CSV file and process the data
        csvfile = codecs.iterdecode(file.file, 'utf-8')
        csvReader = csv.reader(csvfile, delimiter=';')
        
        data = []
        row_count = 0
        
        for row in csvReader:
            if row[0].startswith('\ufeff'):
                row[0] = row[0][1:]
            if any(item == '' for item in row):
                print("Missing fields in row:", row)
            else:
                data.append(row)
            
            row_count += 1
            
            if row_count % batch_size == 0:
                # Insert the current batch into the database
                insert_batch_to_database(data, table_name, columns)
                # Reset the data list for the next batch
                data = []
        
        # Insert the remaining batch into the database
        if data:
            insert_batch_to_database(data, table_name, columns)

    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        return {"error": str(e)}
    except Exception as e:
        # Handle other errors
        return {"error": str(e)}
    
    return {"message": "Data uploaded successfully"}

def insert_batch_to_database(data, table_name, columns):
    """
    Inserts a batch of data into the database.

    Args:
        data (list): The list of data rows to insert.
        table_name (str): The name of the MySQL table where the data will be inserted.
        columns (list): The list of column names for the table.
    """
    try:
        # Create a pandas DataFrame with the data and set column names
        df = pd.DataFrame(data, columns=columns)
        df.columns = columns
        
        # Define the connection string to the database
        connection_string = f"mysql+pymysql://{username}:{password}@{host_con}:3306/{database_name}"

        # Create an engine instance for the connection
        engine = create_engine(connection_string)
        
        # Insert the data into the specified table
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        raise e

@app.post("/upload_departments")
def upload_departments(file: UploadFile = File(...)):
    """
    Endpoint for uploading department data from a CSV file.
    """
    return upload_csv_and_insert(file, "departments", ["id", "department"])

@app.post("/upload_jobs")
def upload_jobs(file: UploadFile = File(...)):
    """
    Endpoint for uploading job data from a CSV file.
    """
    return upload_csv_and_insert(file, "jobs", ["id", "job"])

@app.post("/upload_hired_employees")
def upload_hired_employees(file: UploadFile = File(...)):
    """
    Endpoint for uploading hired employees data from a CSV file.
    """
    return upload_csv_and_insert(file, "hired_employees", ["id", "name", "datetime", "department_id", "job_id"])
