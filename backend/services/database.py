import pymysql
from config import Config

def get_db_connection():
    return pymysql.connect(**Config.DB_SOURCE)

def get_moodle_connection():
    return pymysql.connect(**Config.DB_VM_A)