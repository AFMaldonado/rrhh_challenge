import csv
import codecs
from database import insert_batch_to_database
from fastapi import UploadFile

def upload_csv_and_insert(file: UploadFile, table_name: str, columns: list, host_con: str, username: str, password: str, database_name: str):
    """
    Uploads a CSV file and inserts its data into the specified MySQL table.

    Args:
        file (UploadFile): The CSV file to upload and insert.
        table_name (str): The name of the MySQL table to insert the data into.
        columns (list): The list of column names for the table.
        host_con (str): The host address for the MySQL connection.
        username (str): The username for the MySQL connection.
        password (str): The password for the MySQL connection.
        database_name (str): The name of the MySQL database.

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
                insert_batch_to_database(data, table_name, columns, host_con, username, password, database_name)
                # Reset the data list for the next batch
                data = []

        # Insert the remaining batch into the database
        if data:
            insert_batch_to_database(data, table_name, columns, host_con, username, password, database_name)

    except Exception as e:
        # Handle errors
        return {"error": str(e)}

    return {"message": "Data uploaded successfully"}
