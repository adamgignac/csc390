'''
Created on 2013-10-04

@author: Adam Gignac
'''

from gi.repository import Gtk
from notetypes.TextNote import TextNote #TODO: Import all into a list

class MainWindow():
    '''
    The main interface window
    '''


    def __init__(self):
        '''
        Constructor
        '''
        builder = Gtk.Builder()
        builder.add_from_file("mainWindow.glade")
        window = builder.get_object("baseWindow")
        
        handlers = {
            'onDestroy':self.handleWindowExit
        }
        
        builder.connect_signals(handlers)
        
        testNote = TextNote()
        builder.get_object("notebook").add(testNote)
        
        window.show_all()
    
    def handleWindowExit(self, *args):
        '''
        Called when the window is destroyed via
        clicking on the 'X' or the 'Quit' menu
        item.
        '''
        #TODO: Ask to save all open documents
        Gtk.main_quit()

if __name__ == "__main__":
    w = MainWindow()
    Gtk.main()