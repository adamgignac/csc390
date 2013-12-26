'''
Created on 2013-10-04

@author: Adam Gignac
'''

from gi.repository import Gtk
from pages.textnote import TextNote #TODO: Import all into a list
from pages.searchresult import SearchResult
from gui.tablabel import TabLabel
from database.coursetable import CourseTable
from database.notetable import NoteTable
from tools import constants

import datetime
import os
import sqlite3

class MainWindow():
    '''
    The main interface window
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        conn = sqlite3.Connection(constants.DATABASE_PATH)
        self.coursesStore = CourseTable(conn)
        self.notesStore = NoteTable(conn)
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), "isidore.glade"))
        
        #Connect some signals
        signalHandlers = {
            'on_baseWindow_destroy':self.onWindowDestroy,
            'on_menu_quit_activate':self.onWindowDestroy,
            'on_menu_help_about_activate':self.onMenuAboutClicked,
            'on_newMenu_clicked':self.onNewClicked,
            'on_notebook_switch_page':self.onTabChanged,
            'on_treeview_row_activated':self.onTreeviewRowActivated,
        }
        self.builder.connect_signals(signalHandlers)
        
        self.notebook = self.builder.get_object('notebook')
        
        #Populate the treeview
        treeviewModel = self.builder.get_object("courseListModel")
        self.courses = self.coursesStore.listAll()
        for code, title in self.courses: #course = (code, title)
            self.builder.get_object("newNote_courseSelector").append_text(code)
            iter = treeviewModel.append(None, ("%s (%s)" % (code, title), None))
            notesForCourse = self.notesStore.listAllForCourse(code)
            for date, course, path in notesForCourse:
                treeviewModel.append(iter, (code + ": " + date, path))
        
        #Temporary
        testNote = TextNote()
        self.createNewPage(testNote)
        self.displaySearchResults("changes")

        self.builder.get_object("baseWindow").show_all()

    def displaySearchResults(self, term):
        resultsPage = SearchResult(term)
        label = TabLabel("Search Results: " + term)
        label.connect('close-clicked', self.onTabClosed, resultsPage)
        self.notebook.append_page(resultsPage, label)
    
    def createNewPage(self, pageContent, labelString="New page"):
        '''
        Append the given item to the notebook, creating a proper
        label and close button on the tab.
        '''
        label = TabLabel(labelString)
        pageContent.setFilename(labelString + ".html")
        num = self.notebook.append_page(pageContent, label)
        label.connect('close-clicked', self.onTabClosed, pageContent)
        self.notebook.set_current_page(num)
    
    def onWindowDestroy(self, *args):
        '''
        Called when the window is destroyed via
        clicking on the 'X' or the 'Quit' menu
        item.
        '''
        for page in self.notebook.get_children():
            page.saveContents()
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
        Called when the New button is clicked. Create a new page
        stamped with today's date.
        '''
        dialog = self.builder.get_object("newNoteDialog")
        if dialog.run() == Gtk.ResponseType.OK:
            page = TextNote()
            course = self.builder.get_object("newNote_courseSelector").get_active_text()
            self.createNewPage(page, course + ": " + self._getCurrentDate())
            self.builder.get_object('baseWindow').show_all()
            #Add to treeview
        dialog.hide()
    
    def _getCurrentDate(self):
        now = datetime.datetime.now()
        dateString = "%d-%d-%d" % (now.year, now.month, now.day)
        return dateString
    
    def onTabClosed(self, button, page=None):
        '''
        Called when a tab is closed. Save the contents of the tab.
        '''
        #TODO: (Ask to)? save the contents of the tab
        try:
            page.saveContents()
        except NotImplementedError:
            pass
        except IOError:
            print("Failed to save page")
        pageNumber = self.notebook.page_num(page)
        self.notebook.remove_page(pageNumber)
    
    def onMenuAboutClicked(self, menuItem):
        '''
        Called when the About menu item is selected. Opens the
        about dialog.
        '''
        aboutWindow = self.builder.get_object("aboutDialog")
        aboutWindow.run()
        aboutWindow.hide()
    
    def onTreeviewRowActivated(self, treeview, path, column):
        #Determine if the row is a course (top-level) or note (child)
        model = treeview.get_model()
        iter = model.get_iter(path)
        if path.get_depth() == 1:
            #This is a course/folder
            #Open the folder
            treeview.expand_row(path, True)
        else:
            #Open the note in a new tab
            page = TextNote(model.get_value(iter, 1))
            self.createNewPage(page, model.get_value(iter, 0))

if __name__ == "__main__":
    w = MainWindow()
    Gtk.main()
