'''
Created on 2013-11-20

@author: adam
'''
from abstractnote import AbstractNote
from tools.searchengine import SearchEngine

from gi.repository import Gtk, WebKit
import os

class SearchResult(Gtk.ScrolledWindow, AbstractNote):
    '''
    Displays the results of a search
    '''

    #TODO: Change this path (hardcoded now for testing)
    NOTES_DIRECTORY = os.path.expanduser("~/Documents/")
    
    HTML = """
    <html>
        <head>
            <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap.min.css">
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
        for result in self.engine.findPattern(type(self).NOTES_DIRECTORY, searchTerm):
            resultContext = "\n".join([line for line in result[1]])
            resultsHTML.append(type(self).RESULT_BLOCK % (result[0], resultContext))
        
        content = type(self).HTML % ("\n".join(resultsHTML),)
        self.webview.load_html_string(content, "file:///")
        self.show_all()
    
    def getContextToolbarItems(self):
        label = Gtk.ToolItem()
        label.add(Gtk.Label("Search for: %s" % (self.searchTerm,)))
        return [label]