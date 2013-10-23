'''
Created on 2013-10-04

@author: Adam Gignac
'''

from gi.repository import Gtk
from notetypes.TextNote import TextNote #TODO: Import all into a list
import datetime

class MainWindow():
    '''
    The main interface window
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.builder = Gtk.Builder()
        self.builder.add_from_file("mainWindow.glade")
        window = self.builder.get_object("baseWindow")
        
        window.connect('destroy', self.handleWindowExit)
        
        self.builder.get_object('newMenu').connect('clicked', self.onNewClicked)
        
        notebook = self.builder.get_object('notebook')
        notebook.connect('switch-page', self.onTabChanged)
        
        testNote = TextNote()
        notebook.add(testNote)
        
        testNote2 = TextNote()
        notebook.add(testNote2)

        window.show_all()
    
    def handleWindowExit(self, *args):
        '''
        Called when the window is destroyed via
        clicking on the 'X' or the 'Quit' menu
        item.
        '''
        #TODO: Ask to save all open documents
        Gtk.main_quit()
    
    def onTabChanged(self, notebook, page, page_num):
        '''
        Called when a page is selected from the list of tabs.
        Updates the context toolbar with the items provided by
        the page.
        '''
        #Remove previous contents
        contextToolbar = self.builder.get_object('contextToolbar')
        for item in contextToolbar.get_children():
            contextToolbar.remove(item)
        #Add new items
        for item in page.getContextToolbarItems():
            contextToolbar.add(item)
        contextToolbar.show_all() #Force a refresh of GUI
    
    def onNewClicked(self, button):
        '''
        Called when the New button is clicked
        '''
        
        now = datetime.datetime.now()
        print "Current date: %d/%d/%d" % (now.year, now.month, now.day)
        page = TextNote()
        self.builder.get_object('notebook').add(page)

if __name__ == "__main__":
    w = MainWindow()
    Gtk.main()