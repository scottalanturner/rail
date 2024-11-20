import os
import boto3
import mysql.connector
from dotenv import load_dotenv

class DatabaseConfig:
    def __init__(self, is_lambda=False):
        self.is_lambda = is_lambda
        load_dotenv()
        self.DB_HOST = os.getenv('RDS_HOST')
        self.DB_NAME = os.getenv('RDS_DB_NAME')
        self.DB_PORT = int(os.getenv('RDS_PORT', '3306'))
        self.DB_USER = os.getenv('RDS_USERNAME')
        self.REGION = 'us-east-1'

    def get_connection(self):
        try:
            print(f"Attempting to connect to: {self.DB_HOST}")
            print(f"Database name: {self.DB_NAME}")
            print(f"Port: {self.DB_PORT}")
            print(f"Username: {self.DB_USER}")
            
            conn = mysql.connector.connect(
                host=self.DB_HOST,
                database=self.DB_NAME,
                user=self.DB_USER,
                password=os.getenv('RDS_PASSWORD'),
                port=self.DB_PORT,
                ssl_ca='rds-ca-2019-root.pem'
            )
            return conn
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            raise
