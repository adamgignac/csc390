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

    columnDefs = {}

    def __init__(self, connection):
        '''
        Constructor
        connection = SQLite connection object
        '''
        
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
        if len(type(self).columnDefs) == 0:
            raise Exception("This is an abstract class and should not be instantiated")
        query = """CREATE TABLE IF NOT EXISTS %s (%s)""" % (self.tableName, 
            ", ".join(["%s %s" % (k,v) for k,v in type(self).columnDefs.items()])
        )
        print query
        self.cursor.execute(query)