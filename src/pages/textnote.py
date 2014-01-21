'''
Created on 2013-10-19

@author: Adam Gignac
'''
from gi.repository import Gtk, WebKit

import os
import json
from BeautifulSoup import BeautifulSoup
from xml.sax import saxutils

from page import Page
from tools import constants
from gui.embeddialog import EmbedDialog

class TextNote(Gtk.ScrolledWindow, Page):
    '''
    A text-based note.
    '''


    def __init__(self, filename=None):
        '''
        Constructor. If sourceFile is specified, the contents of
        sourceFile will be contained in the page.
        '''
        super(TextNote, self).__init__(None, None)
        
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(os.path.dirname(__file__), "embedDialog.glade"))
        self.embedDialog = EmbedDialog()
        
        self.webview = WebKit.WebView()
        #Populate the page with template
        if filename is None:
            targetFile = os.path.join(os.path.dirname(__file__), "TextNoteTemplate.html")
            self.filename = targetFile
        else:
            targetFile = os.path.join(constants.NOTES_DIR, filename)
        with open(targetFile, 'r') as f:
            try:
                content = "\n".join(f.readlines())
            except:
                content = "Well, this is awkward..."
        
        self.webview.load_html_string(saxutils.unescape(content), "file:///")
        self.add(self.webview)
        self.webview.set_editable(True)
        self.settings = self.webview.get_settings()
        self.settings.set_property("enable-spell-checking", True) #May not work
        self.show_all()

    def saveContents(self):
        '''
        Extracts the contents of the page and writes them to a file.
        '''
        
        with open(os.path.join(constants.NOTES_DIR, self.filename), 'w') as f:
            #Get HTML by packing it into the document title
            self.webview.execute_script("document.title=document.documentElement.innerHTML;")
            #Dump title to file
            content = self.webview.get_main_frame().get_title().replace("&gt;", ">") #Fix css selector not saving
            f.write(BeautifulSoup(content).prettify())
            
    
    def setFilename(self, filename):
        self.filename = filename
        
    
    def getFilename(self):
        return self.filename


    def getContextToolbarItems(self):
        '''
        Returns a list of toolbar items that are specific to the note
        type (i.e. text formatting for text notes, drawing tools for
        a diagram, etc)
        '''
        bold = Gtk.ToolButton(Gtk.STOCK_BOLD)
        bold.connect('clicked', self.onBoldClicked)
        italic = Gtk.ToolButton(Gtk.STOCK_ITALIC)
        italic.connect('clicked', self.onItalicClicked)
        underline = Gtk.ToolButton(Gtk.STOCK_UNDERLINE)
        underline.connect('clicked', self.onUnderlineClicked)
        embed = Gtk.ToolButton(Gtk.STOCK_NEW)
        embed.connect('clicked', self.onEmbedClicked)
        indent = Gtk.ToolButton(Gtk.STOCK_INDENT)
        indent.connect('clicked', self.onIndentClicked)
        unindent = Gtk.ToolButton(Gtk.STOCK_UNINDENT)
        unindent.connect('clicked', self.onUnindentClicked)
        #TODO: Add icons for lists
        unorderedList = Gtk.ToolButton()
        unorderedList.connect('clicked', self.onUnorderedListClicked)
        orderedList = Gtk.ToolButton()
        orderedList.connect('clicked', self.onOrderedListClicked)
        leftJustify = Gtk.ToolButton(Gtk.STOCK_JUSTIFY_LEFT)
        leftJustify.connect('clicked', self.onLeftJustifyClicked)
        centerJustify = Gtk.ToolButton(Gtk.STOCK_JUSTIFY_CENTER)
        centerJustify.connect('clicked', self.onCenterJustifyClicked)
        rightJustify = Gtk.ToolButton(Gtk.STOCK_JUSTIFY_RIGHT)
        rightJustify.connect('clicked', self.onRightJustifyClicked)
        undo = Gtk.ToolButton(Gtk.STOCK_UNDO)
        undo.connect('clicked', self.onUndoClicked)
        redo = Gtk.ToolButton(Gtk.STOCK_REDO)
        redo.connect('clicked', self.onRedoClicked)
        
        return [bold, italic, underline, embed, indent, unindent, 
                unorderedList, orderedList, leftJustify, centerJustify,
                rightJustify, undo, redo]
    
    def onBoldClicked(self, button):
        self.webview.execute_script("document.execCommand('bold', false, false);")
    
    def onItalicClicked(self, button):
        self.webview.execute_script("document.execCommand('italic', false, false);")
    
    def onUnderlineClicked(self, button):
        self.webview.execute_script("document.execCommand('underline', false, false);")
    
    def onEmbedClicked(self, button):
        if self.embedDialog.run() == Gtk.ResponseType.OK:
            html = json.dumps(self.embedDialog.getHtml())
            command = """document.execCommand('insertHTML', false, %s);""" % (html,)
            if __debug__:
                print command
            self.webview.execute_script(command)
        self.embedDialog.hide()
    
    def onIndentClicked(self, button):
        self.webview.execute_script("document.execCommand('indent', false, false);")
    
    def onUnindentClicked(self, button):
        self.webview.execute_script("document.execCommand('outdent', false, false);")
    
    def onUnorderedListClicked(self, button):
        self.webview.execute_script("document.execCommand('insertUnorderedList', false, false);")
    
    def onOrderedListClicked(self, button):
        self.webview.execute_script("document.execCommand('insertOrderedList', false, false);")
    
    def onLeftJustifyClicked(self, button):
        self.webview.execute_script("document.execCommand('justifyleft', false, false);")
    
    def onCenterJustifyClicked(self, button):
        self.webview.execute_script("document.execCommand('justifycenter', false, false);")
    
    def onRightJustifyClicked(self, button):
        self.webview.execute_script("document.execCommand('justifyright', false, false);")
    
    def onUndoClicked(self, button):
        self.webview.execute_script("document.execCommand('undo');")
    
    def onRedoClicked(self, button):
        self.webview.execute_script("document.execCommand('redo');")
