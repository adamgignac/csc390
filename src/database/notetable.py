'''
Created on 2013-11-19

@author: Adam Gignac
Blatant rip-off of the way Django's DAOs work
'''
from databasetable import DatabaseTable

class NoteTable(DatabaseTable):
    '''
    Manages the database table related to Notes
    '''
    columns = {
        "date":"TEXT",
        "course":"TEXT",
        "FOREIGN KEY (course)":"REFERENCES course(code)",
        "path":"TEXT",
    }
    
    def listAllForCourse(self, course):
        query = """SELECT * FROM note WHERE course="%s" """ % (course,)
        self.cursor.execute(query)
        return self.cursor.fetchall()