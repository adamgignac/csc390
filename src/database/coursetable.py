'''
Created on 2013-11-19

@author: Adam Gignac
Blatant rip-off of the way Django's DAOs work
'''
from databasetable import DatabaseTable

class CourseTable(DatabaseTable):
    '''
    Manages the database table related to Courses
    '''
    columns = {
        "name":"TEXT",
        "code":"TEXT",
        "days":"INTEGER",
        "startTime":"TEXT",
        "endTime":"TEXT",
    }
    #TODO: Store start and end times as well as days

if __name__ == "__main__":
    import sqlite3
    c = CourseTable(sqlite3.Connection(":memory:"))