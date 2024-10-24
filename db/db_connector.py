"""This module is to write all the required script
to make database connection with SQLAlchemy
"""
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Function to connect to the MySQL database 
def get_db_connection():
    """this function is to create the connection with the sql database using SQLAlchemy
    if the connection is success return the engine instance if it is fails
    to connect print the error message and return none

    Returns:
        engine/none: if the connection succeed return engine else return none
    """
    try:
        # Create the connection string for SQLAlchemy
        connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
