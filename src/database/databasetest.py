'''
Created on 2013-11-26

@author: Adam Gignac
'''
import unittest
import sqlite3
from databasetable import DatabaseTable
from coursetable import CourseTable
from notetable import NoteTable

class BadlyMadeSubclass(DatabaseTable):
    '''This will throw an exception because it is improperly named'''
    columns = {'dummy':'TEXT'}


DUMMY_DATABASE = sqlite3.Connection(":memory:")

class Test(unittest.TestCase):

    def testAbstract(self):
        self.assertRaises(Exception, DatabaseTable, DUMMY_DATABASE)
    
    def testBadTableName(self):
        self.assertRaises(Exception, BadlyMadeSubclass, DUMMY_DATABASE)

    def testCourses(self):
        table = CourseTable(DUMMY_DATABASE)
        table.insert(name="Senior Project", code="CSC390")
        table.insert(name="Operating Systems")
        self.assertEqual(len(table.listAll()), 2)
        table.remove(name="Senior Project")
        self.assertEqual(len(table.listAll()), 1)
    
    def testNotes(self):
        table = NoteTable(DUMMY_DATABASE)
        table.insert(path="/path/to/file", course="CSC390")
        self.assertEqual(len(table.listAll()), 1)


if __name__ == "__main__":
    unittest.main()
