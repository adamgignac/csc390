'''
Created on 2013-10-04

@author: Adam Gignac
'''

#TODO: Allow notes to be deleted

from gi.repository import Gtk, GLib, Gdk
from pages.textnote import TextNote #TODO: Import all into a list
from pages.tablenote import TableNote
from pages.searchresult import SearchResult
from pages.calendar import Calendar
from gui.tablabel import TabLabel
from database.coursetable import CourseTable
from database.notetable import NoteTable
from tools import resources

import datetime
import os
import sqlite3

AUTOSAVE_TIME = 30

def getCurrentDate():
    '''
    Returns the current date for use in a note title
    '''
    now = datetime.datetime.now()
    dateString = "%d-%d-%d" % (now.year, now.month, now.day)
    timeString = "%d:%d:%d" % (now.hour, now.minute, now.second)
    return dateString, timeString

class MainWindow():
    '''
    The main interface window
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        conn = sqlite3.Connection(resources.DATABASE_PATH)
        self.coursesStore = CourseTable(conn)
        self.notesStore = NoteTable(conn)
        
        self.builder = Gtk.Builder()
        
        _gladeFile = os.path.join(os.path.dirname(__file__), "isidore.glade")
        self.builder.add_from_file(_gladeFile)
        self.builder.get_object("baseWindow").set_icon_from_file(resources.getMainIconSVG())
        
        #Connect some signals
        signalHandlers = {
            'on_baseWindow_destroy':self.onWindowDestroy,
            'on_menu_quit_activate':self.onWindowDestroy,
            'on_menu_help_about_activate':self.onMenuAboutClicked,
            'on_newMenu_clicked':self.onNewClicked,
            'on_notebook_switch_page':self.onTabChanged,
            'on_treeview_row_activated':self.onTreeviewRowActivated,
            'on_searchBox_activate':self.onSearchBoxActivated,
            'on_menu_course_add_activate':self.onMenuCourseAdd,
            'on_open_calendar_clicked':self.onOpenCalendarClicked,
            'on_deleteNote_activate':self.deleteNote,
            'on_treeview1_button_press_event':self.onTreeviewButtonPress,
        }
        self.builder.connect_signals(signalHandlers)
        
        self.notebook = self.builder.get_object('notebook')
        
        #Populate the treeview
        treeviewModel = self.builder.get_object("courseListModel")
        self.courses = self.coursesStore.listAll()
        for course in self.courses:
            courseSelector = self.builder.get_object("newNote_courseSelector")
            courseSelector.append_text(course['code'])
            newIter = treeviewModel.append(None, ("%s (%s)" % 
                                        (course['code'], course['name']), None))
            notesForCourse = self.notesStore.listAllForCourse(course['code'])
            for note in notesForCourse:
                displayString = "%s: %s (%s)" % (course['code'], note['date'], note['time'])
                treeviewModel.append(newIter, (displayString, note['path']))

        #Build note type menu
        newIcon = Gtk.Image()
        newIcon.set_from_file(resources.getIconPath("doc_new"))
        self.builder.get_object("newMenu").set_icon_widget(newIcon)
        noteTypes = self.buildNoteTypesMenu()
        self.builder.get_object("newMenu").set_menu(noteTypes)

        self.builder.get_object("baseWindow").show_all()
        
        self.createNewPage(Calendar(self.coursesStore), "Calendar")
        
        #Hide the progress bar unless we're saving
        self.builder.get_object("autosaveProgress").set_visible(False)
        
        #Add autosave timeout
        GLib.timeout_add_seconds(AUTOSAVE_TIME, self._saveAllWithProgressBar)


    def buildNoteTypesMenu(self):
        '''
        Create the context menu for the New button
        '''
        noteTypes = Gtk.Menu()
        m = Gtk.MenuItem(label="Text")
        noteTypes.append(m)
        m.connect('activate', self._onNoteTypesTextClicked)
        m = Gtk.MenuItem(label="Table")
        noteTypes.append(m)
        m.connect('activate', self._onNoteTypesTableClicked)
        noteTypes.show_all()
        return noteTypes

    def _onNoteTypesTextClicked(self, *args):
        self.onNewClicked(None, pageType="text")

    def _onNoteTypesTableClicked(self, *args):
        self.onNewClicked(None, pageType="table")

    def displaySearchResults(self, term):
        '''
        Search for the given term and open a page displaying the results
        '''
        resultsPage = SearchResult(term)
        label = TabLabel("Search Results: " + term, type="search")
        label.connect('close-clicked', self.onTabClosed, resultsPage)
        num = self.notebook.append_page(resultsPage, label)
        self.notebook.set_current_page(num)
    
    def createNewPage(self, pageContent, labelString="New page"):
        '''
        Append the given item to the notebook, creating a proper
        label and close button on the tab.
        '''
        if isinstance(pageContent, TableNote):
            type_ = "table"
        elif isinstance(pageContent, Calendar):
            type_ = "calendar"
        else:
            type_ = "text"
        label = TabLabel(labelString, type_)
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
    
    def _saveAllWithProgressBar(self, *args):
        '''
        Called automatically every few minutes to save the notes.
        '''
        #Note: the progress bar doesn't appear to be showing
        if __debug__:
            print "Autosave...",
        progressBar = self.builder.get_object('autosaveProgress')
        numPages = len(self.notebook.get_children())
        progressBar.set_visible(True)
        for count, page in enumerate(self.notebook.get_children()):
            progressBar.set_fraction(float(count) / numPages)
            if __debug__:
                print float(count) / numPages
            page.saveContents()
        progressBar.set_visible(False)
        if __debug__:
            print "Done"
        return True
    
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
    
    def onNewClicked(self, button, pageType="text"):
        '''
        Called when the New button is clicked. Create a new page
        stamped with today's date.
        '''
        dialog = self.builder.get_object("newNoteDialog")
        if dialog.run() == Gtk.ResponseType.OK:
            if pageType =="text":
                page = TextNote()
            elif pageType =="table":
                page = TableNote()
            courseSelector = self.builder.get_object("newNote_courseSelector")
            course = courseSelector.get_active_text()
            date, time = getCurrentDate()
            self.createNewPage(page, "%s: %s (%s)" % (course, date, time))
            self.notesStore.insert(date=date, time=time, course=course, 
                                   path=page.getFilename()
                                   )
            self.builder.get_object('baseWindow').show_all()
            #TODO: Add note to treeview
            treeviewModel = self.builder.get_object("courseListModel")
            courseIter = self._findIterForRow(course)
            if pageType == "text":
                displayString = "%s: %s (%s)" % (course, date, time)
            elif pageType == "table":
                displayString = "(Table) %s: %s (%s)" % (course, date, time)
            treeviewModel.append(courseIter, (displayString, page.getFilename()))

        dialog.hide()

    def _findIterForRow(self, searchString):
        '''
        Returns the iter for the first row containing searchString in its first column
        '''
        model = self.builder.get_object("courseListModel")
        i = model.get_iter_first()
        while i and searchString not in model.get_value(i, 0):
            i = model.iter_next(i)
        return i
    
    def onTabClosed(self, button, page=None):
        '''
        Called when a tab is closed. Save the contents of the tab.
        '''
        try:
            page.saveContents()
        except NotImplementedError:
            pass
        except IOError:
            if __debug__:
                print("Failed to save page")
        pageNumber = self.notebook.page_num(page)
        self.notebook.remove_page(pageNumber)
        
    def onOpenCalendarClicked(self, button):
        self.createNewPage(Calendar(self.coursesStore), "Calendar")
    
    def onMenuAboutClicked(self, menuItem):
        '''
        Called when the About menu item is selected. Opens the
        about dialog.
        '''
        aboutWindow = self.builder.get_object("aboutDialog")
        aboutWindow.run()
        aboutWindow.hide()
    
    def onTreeviewRowActivated(self, treeview, path, column):
        '''
        Called when a row in the sidebar is clicked.
        If the row is a 'folder', expand it. Otherwise, open the
        specified note.
        '''
        
        #Determine if the row is a course (top-level) or note (child)
        model = treeview.get_model()
        selectedIter = model.get_iter(path)
        if path.get_depth() == 1:
            #This is a course/folder
            #Open the folder
            treeview.expand_row(path, True)
        else:
            #Open the note in a new tab
            page = TextNote(model.get_value(selectedIter, 1))
            self.createNewPage(page, model.get_value(selectedIter, 0))
    
    def onSearchBoxActivated(self, entry):
        '''
        Called when Enter is pressed in the search box.
        Display the results.
        '''
        self.displaySearchResults(entry.get_text())
    
    def onMenuCourseAdd(self, menuItem):
        '''
        Called when the Course > Add menu item is clicked
        '''
        dialog = self.builder.get_object("newCourseDialog")
        if dialog.run() == Gtk.ResponseType.OK:
            widget = self.builder.get_object("newCourse_title")
            courseTitle = widget.get_text()
            widget = self.builder.get_object("newCourse_code")
            courseCode = widget.get_text()
            self.builder.get_object("newCourse_startHours")
            courseStartHours = widget.get_value()
            widget = self.builder.get_object("newCourse_startMinutes")
            courseStartMinutes = widget.get_value()
            widget = self.builder.get_object("newCourse_endHours")
            courseEndHours = widget.get_value()
            widget = self.builder.get_object("newCourse_endMinutes")
            courseEndMinutes = widget.get_value()
            dayKeys = {'monday':1, 
                       'tuesday':2,
                       'wednesday':4, 
                       'thursday':8, 
                       'friday':16} #UNIX permissions-style
            days = 0
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
                if self.builder.get_object(day).get_active():
                    days += dayKeys[day]
            self.coursesStore.insert(name=courseTitle, code=courseCode, days=days,
                                     startTime="%d:%d" % (courseStartHours, courseStartMinutes),
                                     endTime="%d:%d" % (courseEndHours, courseEndMinutes))
            model = self.builder.get_object('courseListModel')
            model.append(None, ["%s (%s)" % (courseCode, courseTitle), None])
            
        dialog.hide()

    def deleteNote(self, *args):
        treeview = self.builder.get_object("treeview1")
        model, selectedIter = treeview.get_selection().get_selected()
        filePath = model.get_value(selectedIter, 1)
        msg = "Delete %s?" % model.get_value(selectedIter, 0)
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO, text=msg)
        if dialog.run() == Gtk.ResponseType.YES:
            self.notesStore.remove(path=filePath)
            #TODO: Remove from treeview
            treeview.get_model().remove(selectedIter)
            #TODO: Remove from filesystem
        dialog.hide()

    def onTreeviewButtonPress(self, treeview, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == Gdk.BUTTON_SECONDARY:
            #Only show menu if clicking on a child row
            (path, column, relativeX, relativeY) = treeview.get_path_at_pos(int(event.x), int(event.y))
            if path.get_depth() > 1:
                self.builder.get_object("treeviewMenu").popup(None, None, None, None, event.button, event.time)
