'''
Created on 2013-11-20

@author: Adam Gignac
'''

import sqlite3

class DatabaseTable(object):
    '''
    Base class for DAOs
    Child classes should be named '[Unique]Table' where '[Unique]' is
    the name of the table that should be created in the database
    '''

    columns = {}

    def __init__(self, connection):
        '''
        Constructor
        connection = SQLite connection object
        '''
        
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        
        #This is not quite clever, it depends on naming convention
        if not self.__class__.__name__.endswith("Table"):
            raise Exception("Name of child class must be of the form [tablename]Table")
        self.tableName = self.__class__.__name__[:-5].lower()
        
        self.cursor = connection.cursor()
        if self.tableName =="database":
            raise Exception("This is an abstract class and should not be instantiated")
        else:
            self.ensureTableExists()
    
    def ensureTableExists(self):
        if len(type(self).columns) == 0:
            raise Exception("This is an abstract class and should not be instantiated")
        query = """CREATE TABLE IF NOT EXISTS %s (%s)""" % (self.tableName, 
            ", ".join(["%s %s" % (k,v) for k,v in type(self).columns.items()])
        )
        self.cursor.execute(query)
    
    def insert(self, **kwargs):
        columnNames = []
        columnValues = []
        for key in kwargs.keys():
            if key not in type(self).columns.keys():
                raise Exception("Improper column specified")
            columnNames.append('"' + str(key) + '"')
            columnValues.append('"' + str(kwargs[key]) + '"')
        query = """INSERT INTO %s (%s) VALUES (%s)""" % (self.tableName,
            ", ".join(columnNames),
            ", ".join(columnValues) 
            )
        self.cursor.execute(query)
        self.connection.commit()
    
    def listAll(self):
        query = """SELECT * FROM %s""" % (self.tableName,)
        self.cursor.execute(query)
        results = []
        for r in self.cursor.fetchall():
            resultRow = {}
            for key in r.keys():
                resultRow[key] = r[key]
            results.append(resultRow)
        return results

    def remove(self, **kwargs):
        query = """DELETE FROM %s WHERE """ % (self.tableName,)
        for key in kwargs.keys():
            if key not in type(self).columns.keys():
                raise Exception("Improper column specified")
            query += "=".join((key, '"' + kwargs[key] + '"'))
        self.cursor.execute(query)
        self.connection.commit()