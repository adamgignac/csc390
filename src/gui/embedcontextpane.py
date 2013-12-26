'''
Created on 2013-12-23

@author: Adam Gignac
'''

class EmbedContextPane(object):
    '''
    Abstract interface for an embed type context pane.
    All subclasses must implement the getURL() method,
    which should return the path to the source of the
    item being embedded.
    '''
    
    def getURL(self):
        raise NotImplementedError