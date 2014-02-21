'''
Created on 2014-02-04

@author: Adam Gignac
'''

from gi.repository import Gtk, WebKit
import os
from xml.sax import saxutils

from pages.page import Page
from tools import resources

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
            targetFile = os.path.join(resources.NOTES_DIR, filename)
        with open(targetFile, 'r') as sourceFile:
            try:
                content = sourceFile.read()
            except IOError:
                content = "Well, this is awkward..."
        
        self.webview.load_html_string(saxutils.unescape(content),
                                      "file://%s/" % resources.NOTES_DIR)
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

    def _makeToolButton(self, iconName, label, callback, showText=False):
        iconPath = resources.getIcon(iconName)
        button = Gtk.ToolButton()
        button.set_label(label)
        button.set_is_important(showText)
        icon = Gtk.Image()
        icon.set_from_file(iconPath)
        button.set_icon_widget(icon)
        button.connect('clicked', callback)
        return button
        
    def getContextToolbarItems(self):
        addRowButton = self._makeToolButton("cursor_H_split", "Insert Row", self._insertRow, showText=True)
        addColButton = self._makeToolButton("cursor_V_split", "Insert Column", self._insertCol, showText=True)
        return [addRowButton, addColButton]
    
    def _insertRow(self, *args):
        self.webview.execute_script("addRow()")
        
    def _insertCol(self, *args):
        self.webview.execute_script("addColumn()")
    
    def saveContents(self):
        pass