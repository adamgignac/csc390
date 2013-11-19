'''
Created on 2013-10-04

@author: Adam Gignac
'''

class AbstractNote(object):
    '''
    Interface for note types
    '''


    def __init__(self, sourceFile=None):
        '''
        Constructor. If sourceFile is specified, the contents of
        sourceFile will be contained in the page.
        '''
        raise NotImplementedError()
    
    def saveContents(self):
        '''
        Extracts the contents of the page and writes them to a file.
        '''
        raise NotImplementedError()
    
    def getContextToolbarItems(self):
        '''
        Returns a list of toolbar items that are specific to the note
        type (i.e. text formatting for text notes, drawing tools for
        a diagram, etc)
        This should be of the form: [(icon, callback), ...]
        '''
        raise NotImplementedError()