'''
Created on 2013-11-19

@author: Adam Gignac
'''
import os
import fnmatch
from BeautifulSoup import BeautifulSoup

def fixLines(lines):
    '''
    Since we're just pulling a handful of lines out of a file, pass it
    through BeautifulSoup to fix any unmatched tags that pop up.
    '''
    return [BeautifulSoup(line).prettify() for line in lines]

class SearchEngine(object):
    '''
    Reimplementation of grep in Python, with context
    '''
    
    def __init__(self, directory):
        self.directory = directory
    
    def _findAllFilesInDirectory(self, namePattern):
        '''
        Given a directory, finds all files whose names match the specified
        pattern.
        '''
        matches = []
        for root, dirnames, filenames in os.walk(self.directory):
            for filename in fnmatch.filter(filenames, namePattern):
                matches.append(os.path.join(root, filename))
        return matches

    def findPattern(self, pattern):
        '''
        Given a directory, recursively search through all files to find any
        occurences of the specified pattern.
        '''
        savedNotes = self._findAllFilesInDirectory("*.html")
        for note in savedNotes:
            with open(note, 'r') as target:
                lines = target.readlines()
                numLines = len(lines)
                if numLines > 3:
                    for i in range(3):
                        if pattern.lower() in lines[i].lower(): #Case-insensitive
                            yield ("%s: %d" % (note, i), self._fixLines(lines[0:5]))
                    for i in range(3, numLines - 2):
                        if pattern.lower() in lines[i+2].lower():
                            yield ("%s: %d" % (note, i), self._fixLines(lines[i:i+5]))

