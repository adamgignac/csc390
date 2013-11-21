'''
Created on 2013-11-19

@author: Adam Gignac
'''
import os
import fnmatch
from BeautifulSoup import BeautifulSoup

class SearchEngine(object):
    '''
    Reimplementation of grep in Python, with context
    '''
    
    def _findAllFilesInDirectory(self, directory, pattern):
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
        return matches
    
    def _fixLines(self, lines):
        return [BeautifulSoup(line).prettify() for line in lines]

    def findPattern(self, directory, pattern):
        savedNotes = self._findAllFilesInDirectory(directory, "*.html")
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

