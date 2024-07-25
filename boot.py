import sqlite3
import requests
from dotenv import load_dotenv
from exceptions import KernelException
import os
from utils import sys_msg
from datetime import datetime, timedelta

def initialize_environment_variables():
    """
    Loads the environment variables from the '.env' 
    file loacated inside this folder.
    """

    loaded_env = load_dotenv("./.env")

    if loaded_env: return True
    else: raise KernelException("Unable to load environment variables. Do you even have the '.env' file?")

def initialize_constants():
    global BACKEND_URL
    BACKEND_URL = os.getenv("BACKEND_ROOT_URL")

def initialize_database_connection():
    """
    Return the database connection for performing queries.
    """

    db_conn = sqlite3.connect('db.sqlite3')

    tables = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if len(tables.fetchall()) == 0:
        # creation of database and adding the deadlines of scrapers
        db_conn.execute(f"CREATE TABLE scraper_deadlines(market_name VARCHAR(30) UNIQUE NOT NULL, deadline DATE NOT NULL)")

    return db_conn


def test_backend_connection():
    """
    Existence check for the backend. Returns an exception
    if the backend returns a 404 or some code other than 
    200 or 500.
    """
    
    response = requests.get(f"{BACKEND_URL}/api/products/")
    if response.status_code in [200, 500]:
        return True
    else: raise KernelException(f"Unable to find the server at root url {BACKEND_URL}. Is the server running?")


def start_kernel():
    try:
        initialize_environment_variables()
        initialize_constants()
        # test_backend_connection()

        db_conn = initialize_database_connection()

        return db_conn
    except Exception as e:
        raise e
    finally:
        sys_msg("kernel", "Kernel boot complete.")