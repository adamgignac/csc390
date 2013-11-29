'''
Created on 2013-11-26

@author: Adam Gignac
'''
import unittest
import sqlite3
from databasetable import DatabaseTable
from coursetable import CourseTable

class BadlyMadeSubclass(DatabaseTable):
    columns = {'dummy':'STRING'} 


DUMMY_DATABASE = sqlite3.Connection(":memory:")

class Test(unittest.TestCase):

    def testAbstract(self):
        self.assertRaises(Exception, DatabaseTable, DUMMY_DATABASE)
    
    def testBadTableName(self):
        self.assertRaises(Exception, BadlyMadeSubclass, DUMMY_DATABASE)

    def testCourse(self):
        table = CourseTable(DUMMY_DATABASE)
        table.listAll()
        table.insert(name="Senior Project", code="CSC390")
        table.insert(name="Operating Systems")
        table.listAll()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAbstract']
    unittest.main()