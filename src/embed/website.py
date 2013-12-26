'''
Created on 2013-12-23

@author: Adam Gignac
'''

from gi.repository import Gtk
from gui.embedcontextpane import EmbedContextPane

class WebsiteContextPane(Gtk.HBox, EmbedContextPane):
    def __init__(self):
        super(WebsiteContextPane, self).__init__()
        self.add(Gtk.Label("URL: "))
        self.entry = Gtk.Entry()
        self.add(self.entry)
        self.show_all()
    
    def getURL(self):
        return self.entry.get_text()

def register():
    return ("Website", WebsiteContextPane())