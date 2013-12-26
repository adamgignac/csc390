'''
Created on 2013-11-19

@author: adam
'''
from gi.repository import Gtk

import os
import sys
import imp

import embed

class EmbedDialog(Gtk.Dialog):
    '''
    A custom GTK dialog
    '''
    
    def __init__(self):
        super(EmbedDialog, self).__init__(None)
        self.add_button("Embed", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        
        content_area = self.get_content_area()
        self.comboBox = Gtk.ComboBoxText()
        self.comboBox.connect('changed', self.on_combobox_changed)
        
        self.embedTypes = self.loadEmbedTypes()
        for embedType in self.embedTypes.keys():
            self.comboBox.append_text(embedType)
        content_area.add(self.comboBox)
        
        self.contextPane = Gtk.HBox()
        content_area.add(self.contextPane)
        content_area.show_all()
    
    def loadEmbedTypes(self):
        '''
        Load all embed types defined in the embed module
        Returns a list of (name, contextPane) where:
            - name is a string describing the type
            - contextPane is an instance of Gtk.Container providing
                and interface for specifying the source
        '''
        #Search embed module for embed types
        pluginpath = imp.find_module("embed")[1]
        ignore = ('test', 'init')
        pluginfiles = [fname[:-3] for fname in os.listdir(pluginpath) if fname.endswith(".py") and not any([i in fname for i in ignore])]
        if not pluginpath in sys.path:
            sys.path.append(pluginpath)
        
        importedTypes = []
        for fname in pluginfiles:
            try:
                importedTypes.append(__import__(fname))
            except ImportError:
                pass
        
        loadedTypes = {}
        for embedType in importedTypes:
            try:
                k, v = embedType.register()
                loadedTypes[k] = v
            except AttributeError:
                pass
            
        return loadedTypes
    
    def on_combobox_changed(self, comboBox):
        '''
        Called when a type is selected from the combo box.
        '''
        #Update the context pane
        for item in self.contextPane.get_children():
            self.contextPane.remove(item)
        pane = self.embedTypes[comboBox.get_active_text()]
        self.contextPane.add(pane)
    
    def getHtml(self):
        '''
        Returns the HTML that should be embedded in the page.
        '''
        contextPane = self.contextPane.get_children()[0]
        return '<iframe src="%s"></iframe>' % (contextPane.getURL(),)
        
