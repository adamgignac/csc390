'''
Created on 2014-01-09

@author: Adam Gignac
'''

from gi.repository import Gtk
from gui.embedcontextpane import EmbedContextPane

class BlockQuoteContextPane(Gtk.VBox, EmbedContextPane):
    def __init__(self):
        super(BlockQuoteContextPane, self).__init__()
        self.quoteBox = Gtk.TextView()
        self.quoteBox.set_wrap_mode(Gtk.WrapMode.WORD)
        self.add(self.quoteBox)
        self.sourceBox = Gtk.Entry()
        self.add(self.sourceBox)
        self.show_all()
    
    def getHtml(self):
        buffer = self.quoteBox.get_buffer()
        start, end = buffer.get_bounds()
        quote = buffer.get_text(start, end, False)
        source = self.sourceBox.get_text()
        html = "<blockquote><p>%s</p><p><small>%s</small><p></blockquote>" % (quote, source)
        return html

def register():
    return ("Block Quote", BlockQuoteContextPane())