'''
Created on 2013-12-23

@author: Adam Gignac
'''

from gi.repository import Gtk
from gui.embedcontextpane import EmbedContextPane

class WikiContextPane(Gtk.HBox, EmbedContextPane):
    def __init__(self):
        super(WikiContextPane, self).__init__()
        self.add(Gtk.Label("Subject: "))
        self.add(Gtk.Entry())
        self.show_all()
    
    def getURL(self):
        return "http://en.wikipedia.org"

def register():
    return ("Wikipedia", WikiContextPane())