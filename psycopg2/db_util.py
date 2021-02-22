#!/usr/bin/python
import psycopg2
import json
from psycopg2 import db_config

db_host = "database-1.cu4ufvn4rvo7.us-east-2.rds.amazonaws.com"
db_port = 5432
db_name = "AppSyncDatabase"
db_user = "postgres"
db_pass = "postgres"
db_table = "User"

def readRDS(query_cmd):
    conn = make_conn()
    result = fetch_data(conn, query_cmd)
    conn.close()
    return result
    

def make_conn():
    conn = None
    try:
        conn = psycopg2.connect(f"dbname='{db_name}' user='{db_user}' host='{db_host}' password='{db_pass}'")
        return conn
    except :
        print ("I am unable to connect to the database")
        return None


def fetch_data(conn, query):
    if (conn != None):
        result = {}
        print ("Now executing: %s" % (query))
        cursor = conn.cursor()
        cursor.execute(query)
        raw = cursor.fetchall()
        print (raw)
        return raw
    else:
        print("Connection unsuccessful")
        return None
    

