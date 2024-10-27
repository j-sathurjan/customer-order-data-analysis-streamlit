"""
Database Connection Module for Streamlit Application

This module establishes a connection to the MySQL database using SQLAlchemy.
Database credentials are securely accessed from Streamlit's `secrets.toml`.
The `get_db_connection` function attempts to connect and returns an SQLAlchemy 
engine instance if successful. In case of a failure, it returns `None`.

Functions:
- get_db_connection: Establishes a database connection using SQLAlchemy.
"""
from sqlalchemy import create_engine  # SQLAlchemy for database connections
import streamlit as st # Streamlit to access secret environment variables


# Function to connect to the MySQL database 
def get_db_connection():
    """
    Establish and return a MySQL database connection using SQLAlchemy.

    This function retrieves database credentials from Streamlit's `secrets.toml`,
    creates a connection string, and initializes an SQLAlchemy engine to connect
    to the MySQL database. If the connection is successful, the engine instance is
    returned; otherwise, an error is caught, and `None` is returned.

    Returns:
        engine (sqlalchemy.engine.Engine): Database connection engine if successful.
        None: Returns `None` if the connection fails.
    """
    try:
        # Retrieve database credentials securely from Streamlit's secrets
        DB_HOST = st.secrets["delivergate_db"]["DB_HOST"]
        DB_USER = st.secrets["delivergate_db"]["DB_USER"]
        DB_PASSWORD = st.secrets["delivergate_db"]["DB_PASSWORD"]
        DB_NAME = st.secrets["delivergate_db"]["DB_NAME"]
        DIALECT = st.secrets["delivergate_db"]["dialect"]
        
        # Create connection string using provided credentials
        connection_string = f"{DIALECT}+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        
        # Initialize SQLAlchemy engine with the connection string
        engine = create_engine(connection_string)
        return engine # Return the engine instance if connection is successful
    except Exception as e:
        # Log the exception message in Streamlit and return None if connection fails
        st.error(f"Database connection failed: {e}")
        return None
