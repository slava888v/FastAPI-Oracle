import os, urllib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
#import pyodbc
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# ORACLE
connect_url = URL(
    "oracle+cx_oracle",
    username=urllib.parse.quote_plus(str(os.environ.get('DB_USERNAME', 'DEFAULT_DB_USERNAME'))),
    password=urllib.parse.quote_plus(str(os.environ.get('DB_PASSWORD', 'DEFAULT_DB_PASSWORD'))),
    host=str(os.environ.get('DB_HOST', 'DEFAULT_DB_HOST')),
    port=str(os.environ.get('DB_PORT', 'DEFAULT_DB_PORT')),
    database=str(os.environ.get('DB_DATABASE', 'DEFAULT_DB_DATABASE')),
)

# Azure SQL Server
# connect_url = URL.create(
#     "mssql+pyodbc",
#     username=urllib.parse.quote_plus(str(os.environ.get('DB_USERNAME', 'DEFAULT_DB_USERNAME'))),
#     password=urllib.parse.quote_plus(str(os.environ.get('DB_PASSWORD', 'DEFAULT_DB_PASSWORD'))),
#     host=urllib.parse.quote_plus(str(os.environ.get('DB_HOST', 'DEFAULT_DB_HOST'))),
#     database=str(os.environ.get('DB_DATABASE', 'DEFAULT_DB_DATABASE')),
#     query={
#         "driver": "ODBC Driver 17 for SQL Server"
#     },
# )


engine = create_engine(connect_url, max_identifier_length=128)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

