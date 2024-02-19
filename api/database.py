from sqlalchemy import create_engine
import mysql.connector
import pandas as pd

def execute_query(host, username, password, database_name, query):
    """
    Executes a query on the MySQL database.

    Args:
        host (str): The host address for the MySQL connection.
        username (str): The username for the MySQL connection.
        password (str): The password for the MySQL connection.
        database_name (str): The name of the MySQL database.
        query (str): The SQL query to execute.

    Returns:
        list: The result set returned by the query.
    """
    db_connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database_name
    )
    cursor = db_connection.cursor()
    cursor.execute(query)
    metrics = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return metrics

def connect_to_database(host, username, password, database_name):
    """
    Connects to the MySQL database.

    Args:
        host (str): The host address for the MySQL connection.
        username (str): The username for the MySQL connection.
        password (str): The password for the MySQL connection.
        database_name (str): The name of the MySQL database.

    Returns:
        object: The engine object for the MySQL connection.
    """
    connection_string = f"mysql+pymysql://{username}:{password}@{host}:3306/{database_name}"
    engine = create_engine(connection_string)
    return engine

def insert_batch_to_database(data, table_name, columns, host_con, username, password, database_name):
    """
    Inserts a batch of data into the database.

    Args:
        data (list): The list of data rows to insert.
        table_name (str): The name of the MySQL table where the data will be inserted.
        columns (list): The list of column names for the table.
        host_con (str): The host address for the MySQL connection.
        username (str): The username for the MySQL connection.
        password (str): The password for the MySQL connection.
        database_name (str): The name of the MySQL database.
    """
    try:
        # Create a pandas DataFrame with the data and set column names
        df = pd.DataFrame(data, columns=columns)

        # Connect to the database
        connection_string = f"mysql+pymysql://{username}:{password}@{host_con}:3306/{database_name}"
        engine = create_engine(connection_string)

        # Insert the data into the specified table
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    except Exception as e:
        # Handle errors
        raise e
