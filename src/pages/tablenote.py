'''
Created on 2014-02-04

@author: Adam Gignac
'''

from gi.repository import Gtk, WebKit
import os
from xml.sax import saxutils

from pages.page import Page
from tools import constants

class TableNote(Gtk.ScrolledWindow, Page):
    '''
    A page representing a table.
    '''


    def __init__(self, filename=None):
        '''
        Constructor
        '''
        super(TableNote, self).__init__(None, None)
        self.webview = WebKit.WebView()
        
        if filename is None:
            targetFile = os.path.join(os.path.dirname(__file__), 
                                      "TableTemplate.html")
            self.filename = targetFile
        else:
            targetFile = os.path.join(constants.NOTES_DIR, filename)
        with open(targetFile, 'r') as sourceFile:
            try:
                content = sourceFile.read()
            except IOError:
                content = "Well, this is awkward..."
        
        self.webview.load_html_string(saxutils.unescape(content),
                                      "file://%s/" % constants.NOTES_DIR)
        self.webview.set_editable(True)
        self.add(self.webview)
        self.show_all()

    def setFilename(self, filename):
        '''
        Assign a filename to the note, usually the course code and date
        '''
        self.filename = filename

    def getFilename(self):
        '''
        Get the base path where the note is stored
        '''
        return self.filename
        
    def getContextToolbarItems(self):
        addRowButton = Gtk.ToolButton(Gtk.STOCK_ADD)
        addRowButton.set_label("Add row")
        addRowButton.set_is_important(True)
        addRowButton.connect('clicked', self._insertRow)
        addColButton = Gtk.ToolButton(Gtk.STOCK_ADD)
        addColButton.set_label("Add column")
        addColButton.set_is_important(True)
        addColButton.connect('clicked', self._insertCol)
        return [addRowButton, addColButton]
    
    def _insertRow(self, *args):
        self.webview.execute_script("addRow()")
        
    def _insertCol(self, *args):
        self.webview.execute_script("addColumn()")
    
    def saveContents(self):
        pass