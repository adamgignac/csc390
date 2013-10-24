'''
Created on 2013-10-04

@author: Adam Gignac
'''

from gi.repository import Gtk
from notetypes.TextNote import TextNote #TODO: Import all into a list
from gui.TabLabel import TabLabel
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
        
        #Connect some signals
        window.connect('destroy', self.onWindowDestroy)
        self.builder.get_object('newMenu').connect('clicked', self.onNewClicked)
        self.builder.get_object('notebook').connect('switch-page', self.onTabChanged)
        
        #Temporary
        testNote = TextNote()
        self.createNewPage(testNote)
        testNote2 = TextNote()
        self.createNewPage(testNote2)

        window.show_all()
    
    def createNewPage(self, pageContent, labelString="New page"):
        '''
        Append the given item to the notebook, creating a proper
        label and close button on the tab.
        '''
        self.builder.get_object('notebook').append_page(pageContent, TabLabel(labelString))
    
    def onWindowDestroy(self, *args):
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
        
        #Get the current date and time
        now = datetime.datetime.now()
        dateString = "%d/%d/%d" % (now.year, now.month, now.day)
        page = TextNote()
        self.createNewPage(page, dateString)
        self.builder.get_object('baseWindow').show_all()
    
    def onTabClosed(self, button):
        pass

if __name__ == "__main__":
    w = MainWindow()
    Gtk.main()