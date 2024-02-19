from fastapi import FastAPI, UploadFile, File
from secret_manager import SecretManagerGCP
from database import execute_query
from csv_handler import upload_csv_and_insert
import json

# Initialize the FastAPI application
app = FastAPI()

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

# Define endpoints
@app.post("/upload_departments")
def upload_departments(file: UploadFile = File(...)):
    """
    Endpoint for uploading department data from a CSV file.
    """
    return upload_csv_and_insert(file, "departments", ["id", "department"], host_con, username, password, database_name)

@app.post("/upload_jobs")
def upload_jobs(file: UploadFile = File(...)):
    """
    Endpoint for uploading job data from a CSV file.
    """
    return upload_csv_and_insert(file, "jobs", ["id", "job"], host_con, username, password, database_name)

@app.post("/upload_hired_employees")
def upload_hired_employees(file: UploadFile = File(...)):
    """
    Endpoint for uploading hired employees data from a CSV file.
    """
    return upload_csv_and_insert(file, "hired_employees", ["id", "name", "datetime", "department_id", "job_id"], host_con, username, password, database_name)

# Define a route for the endpoint that calculates hiring metrics by department and job in 2021
@app.get("/dept_job_hiring_2021")
async def dept_job_hiring_2021():
    # Define the query to obtain the required metrics
    query = """
        SELECT
            d.department,
            j.job,
            SUM(CASE WHEN QUARTER(h.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN QUARTER(h.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN QUARTER(h.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN QUARTER(h.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM
            rrhh.hired_employees h
        LEFT JOIN
            rrhh.departments d ON h.department_id = d.id 
        LEFT JOIN
            rrhh.jobs j ON h.job_id  = j.id 
        WHERE
            YEAR(h.datetime) = 2021
        GROUP BY
            d.department,
            j.job
        ORDER BY
            d.department,
            j.job;
    """
    # Execute the query and return the results as a JSON dictionary
    return {"metrics": execute_query(host_con, username, password, database_name, query)}

# Define a route for the endpoint that calculates departments that hired more than the average in 2021
@app.get("/dept_above_avg_hiring")
async def dept_above_avg_hiring():
    # Define the query to obtain the required metrics
    query = """
        WITH average_by_department AS (
            SELECT AVG(num_employees) AS average 
            FROM (
                SELECT COUNT(*) AS num_employees
                FROM rrhh.hired_employees
                WHERE YEAR(datetime) = 2021
                GROUP BY department_id
            ) AS avg_department
        )
        SELECT
            d.id,
            d.department,
            COUNT(*) AS hired
        FROM
            rrhh.hired_employees h
        LEFT JOIN
            rrhh.departments d ON h.department_id = d.id 
        GROUP BY
            d.id,
            d.department 
        HAVING
            COUNT(*) > (SELECT average FROM average_by_department)
        ORDER BY
            hired DESC;
    """
    # Execute the query and return the results as a JSON dictionary
    return {"metrics": execute_query(host_con, username, password, database_name, query)}
