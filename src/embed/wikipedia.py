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
        self.entry = Gtk.Entry()
        self.add(self.entry)
        self.show_all()
    
    def getHtml(self):
        text = self.entry.get_text()
        url =  "http://en.wikipedia.org/wiki/%s" % (text.replace(" ", "_"))
        return '<iframe src="%s"></iframe>' % (url,)

def register():
    return ("Wikipedia", WikiContextPane())