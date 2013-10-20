'''
Created on 2013-10-19

@author: Adam Gignac
'''
from gi.repository import Gtk, WebKit
from notetypes.AbstractNote import AbstractNote

class TextNote(Gtk.ScrolledWindow, AbstractNote):
    '''
    A text-based note.
    '''


    def __init__(self, sourceFile=None):
        '''
        Constructor. If sourceFile is specified, the contents of
        sourceFile will be contained in the page.
        '''
        super(TextNote, self).__init__(None, None)
        webview = WebKit.WebView()
        self.add(webview)
        webview.set_editable(True)
        self.show_all()

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