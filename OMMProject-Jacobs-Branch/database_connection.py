import mysql.connector
from config import config

def makeConnection():
    return mysql.connector.connect(user = config.database_username, 
                                   password = config.database_pass, 
                                   host = config.database_host, 
                                   database = config.database)
