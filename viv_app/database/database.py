import mysql.connector
import cx_Oracle
connection=None
cursor=None

class Connection(object):
    def __init__(self, dbType):
        self.dbType = dbType
        
    def getConnection(self, config):
        if self.dbType =="mysql":
            connection= mysql.connector.Connect(**config)
           
        if self.dbType =="oracle":
            connection= cx_Oracle.connect(config)
        return connection
    
    def getCursor(self,connection):
        self.connection=connection
        if self.dbType =="mysql":
            cursor= connection.cursor(buffered=True)
           
        if self.dbType =="oracle":
            cursor= connection.cursor()
        return cursor