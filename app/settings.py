import os
from dotenv import load_dotenv

load_dotenv()


def generate_db_connection_string():
    engine = os.environ.get('DB_ENGINE')
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    dbhost = os.environ.get('DB_HOST')
    dbname = os.environ.get('DB_NAME')
    return f"{engine}://{username}:{password}@{dbhost}/{dbname}"


SQLALCHEMY_URL = generate_db_connection_string()

ADMIN_DEFAULT_PASSWORD = 'password'
