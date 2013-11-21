'''
Created on 2013-11-20

@author: Adam Gignac
'''

import sqlite3

class DatabaseTable(object):
    '''
    Base class for DAOs
    '''

    columnDefs = {}

    def __init__(self, connection):
        '''
        Constructor
        connection = SQLite connection object
        '''
        
        self.tableName = self.__class__.__name__[:-5].lower()
        
        self.cursor = connection.cursor()
        if self.tableName =="database":
            raise Exception("This is an abstract class")
        else:
            self.ensureTableExists()
    
    def ensureTableExists(self):
        if len(type(self).columnDefs) == 0:
            raise Exception("This is an abstract class")
        query = """CREATE TABLE IF NOT EXISTS %s (%s)""" % (self.tableName, 
            ", ".join(["%s %s" % (k,v) for k,v in type(self).columnDefs.items()])
        )
        print query
        self.cursor.execute(query)