'''
Created on 2013-11-26

@author: adam
'''
import unittest
import sqlite3
from databasetable import DatabaseTable
from coursetable import CourseTable

class Test(unittest.TestCase):

    def testAbstract(self):
        self.assertRaises(Exception, DatabaseTable, sqlite3.Connection(":memory:"))

    def testCourse(self):
        table = CourseTable(sqlite3.Connection(":memory:"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAbstract']
    unittest.main()