'''
Created on 2013-10-19

@author: Adam Gignac
'''
from gi.repository import Gtk, WebKit
import os
import json
from BeautifulSoup import BeautifulSoup
from xml.sax import saxutils

from pages.page import Page
from tools import resources
from gui.embeddialog import EmbedDialog

COMMANDS = {
'bold':"document.execCommand('bold', false, false);",
'italic':"document.execCommand('italic', false, false);",
'underline':"document.execCommand('underline', false, false);",
'indent':"document.execCommand('indent', false, false);",
'outdent':"document.execCommand('outdent', false, false);",
'unorderedList':"document.execCommand('insertUnorderedList', false, false);",
'orderedList':"document.execCommand('insertOrderedList', false, false);",
'justifyLeft':"document.execCommand('justifyleft', false, false);",
'justifyCenter':"document.execCommand('justifycenter', false, false);",
'justifyRight':"document.execCommand('justifyright', false, false);",
'undo':"document.execCommand('undo');",
'redo':"document.execCommand('redo');"
}

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
        gladeFile = os.path.join(os.path.dirname(__file__), "embedDialog.glade")
        builder.add_from_file(gladeFile)
        self.embedDialog = EmbedDialog()
        
        self.webview = WebKit.WebView()
        #Populate the page with template
        if filename is None:
            targetFile = os.path.join(os.path.dirname(__file__), 
                                      "TextNoteTemplate.html")
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
        self.add(self.webview)
        self.webview.set_editable(True)
        self.settings = self.webview.get_settings()
        self.settings.set_property("enable-spell-checking", True) #May not work
        self.show_all()

    def saveContents(self):
        '''
        Extracts the contents of the page and writes them to a file.
        '''
        
        filePath = os.path.join(resources.NOTES_DIR, self.filename)
        with open(filePath, 'w') as saveFile:
            #Get HTML by packing it into the document title
            #Save the old title
            command = "oldtitle=document.title;"
            command += "document.title=document.documentElement.innerHTML;"
            self.webview.execute_script(command)
            #Dump title to file
            content = self.webview.get_main_frame().get_title()
            content = content.replace("&gt;", ">") #Fix css selector not saving
            #Restore the old title
            self.webview.execute_script("document.title=oldtitle;")
            saveFile.write(BeautifulSoup(content).prettify())
            
    
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

    def _makeToolButton(self, iconName, label, command, showText=False):
        iconPath = resources.getIcon(iconName)
        button = Gtk.ToolButton()
        button.set_label(label)
        icon = Gtk.Image()
        icon.set_from_file(iconPath)
        button.set_icon_widget(icon)
        button.set_is_important(showText)
        button.connect('clicked', self.onButtonClicked, command)
        return button

    def getContextToolbarItems(self):
        '''
        Returns a list of toolbar items that are specific to the note
        type (i.e. text formatting for text notes, drawing tools for
        a diagram, etc)
        '''
        bold = self._makeToolButton("font_bold", "Bold", COMMANDS['bold'])
        italic = self._makeToolButton("font_italic", "Italic", COMMANDS['italic'])
        underline = self._makeToolButton("font_underline", "Underline", COMMANDS['underline'])
        indent = self._makeToolButton("indent_increase", "Indent", COMMANDS['indent'])
        unindent = self._makeToolButton("indent_decrease", "Outdent", COMMANDS['outdent'])
        unorderedList = self._makeToolButton("list_bullets", "Bulleted List", COMMANDS['unorderedList'])
        orderedList = self._makeToolButton("list_num", "Numbered List", COMMANDS['orderedList'])
        leftJustify = self._makeToolButton("align_left", "Align Left", COMMANDS['justifyLeft'])
        centerJustify = self._makeToolButton("align_center", "Center", COMMANDS['justifyCenter'])
        rightJustify = self._makeToolButton("align_right", "Align Right", COMMANDS['justifyRight'])
        undo = self._makeToolButton("undo", "Undo", COMMANDS['undo'])
        redo = self._makeToolButton("redo", "Redo", COMMANDS['redo'])

        #Embed button is a special case
        embed = Gtk.ToolButton()
        embed.set_label("Embed...")
        embedIcon = Gtk.Image()
        embedIcon.set_from_file(resources.getIcon("import"))
        embed.set_icon_widget(embedIcon)
        embed.set_is_important(True)
        embed.connect('clicked', self.onEmbedClicked)
        
        return [bold, italic, underline, embed, indent, unindent, 
                unorderedList, orderedList, leftJustify, centerJustify,
                rightJustify, undo, redo]
    
    def onButtonClicked(self, button, command):
        '''
        Called when a button is clicked.
        The command to run for each button press is passed when connecting
        the signal.
        '''
        self.webview.execute_script(command)
    
    def onEmbedClicked(self, button):
        '''
        Called when the embed button is clicked.
        This is a special case because it's more than just running one line
        of Javascript
        '''
        if self.embedDialog.run() == Gtk.ResponseType.OK:
            html = json.dumps(self.embedDialog.getHtml())
            command = "document.execCommand('insertHTML', false, %s);" % (html,)
            if __debug__:
                print command
            self.webview.execute_script(command)
        self.embedDialog.hide()
