'''
Created on 2013-11-20

@author: adam
'''
from page import Page
from tools.searchengine import SearchEngine
from tools import constants

from gi.repository import Gtk, WebKit
import os

class SearchResult(Gtk.ScrolledWindow, Page):
    '''
    Displays the results of a search
    '''
    
    HTML = """
    <html>
        <head>
            <link rel="stylesheet" href="dist/css/bootstrap.css">
        </head>
        <body>
            %s
        </body>
    </html>
    """
    
    RESULT_BLOCK = """
    <div class="alert alert-info">
        <p class="lead">%s</p>
        <p>%s</p>
    </div>
    """

    def __init__(self, searchTerm):
        '''
        Constructor
        '''
        super(SearchResult, self).__init__(None, None)
        self.searchTerm = searchTerm
        self.webview = WebKit.WebView()
        self.add(self.webview)
        self.engine = SearchEngine()
        
        resultsHTML = []
        for result in self.engine.findPattern(constants.NOTES_DIR, searchTerm):
            resultContext = "\n".join([line for line in result[1]])
            filename = result[0].split(os.path.sep)[-1].replace(".html", "")
            resultsHTML.append(type(self).RESULT_BLOCK % (filename, resultContext))
        
        content = type(self).HTML % ("\n".join(resultsHTML),)
        self.webview.load_html_string(content, "file://%s/" % constants.NOTES_DIR)
        self.show_all()
    
    def getContextToolbarItems(self):
        label = Gtk.ToolItem()
        label.add(Gtk.Label("Search for: %s" % (self.searchTerm,)))
        return [label]
    
    def saveContents(self):
        """There is no need to save search results"""
        pass
