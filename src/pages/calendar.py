'''
Created on 2014-02-16

@author: adam
'''
from pages.page import Page
from tools import resources
from gi.repository import Gtk, GooCanvas

def _occursOnDay(course, day):
    return course['days'] & day

def _timeAsDecimal(time):
    t = time.split(":")
    return float(t[0]) + float(t[1])/60

NUM_HOURS = 14
NUM_DAYS = 5
START_HOUR = 8

class Calendar(GooCanvas.Canvas, Page):
    '''
    Displays a calendar of student courses and allows modification of them
    '''


    def __init__(self, courseStore):
        '''
        Constructor
        '''
        super(Calendar, self).__init__()
        self.root = self.get_root_item()
        self.connect('size-allocate', self.on_resize)
        self.show_all()
        self.courses = courseStore.listAll()
    
    def on_resize(self, widget, allocation):
        self.width = allocation.width
        self.height = allocation.height
        self.hour_height = self.height/NUM_HOURS
        self.draw()
    
    def draw(self):
        self.set_bounds(0, 0, self.width, self.height)
        self._drawGrid()
        for course in self.courses:
            self._drawCourse(course)
    
    def _drawGrid(self):
        GooCanvas.CanvasRect(parent=self.root,
                             x=0,
                             y=0,
                             width=self.width,
                             height=self.height,
                             fill_color="white")
        GooCanvas.CanvasGrid(parent=self.root, #Major lines
                             x=0,
                             y=0,
                             width=self.width,
                             height=self.height,
                             x_step=self.width/NUM_DAYS,
                             y_step=self.hour_height,
                             horz_grid_line_width=1,
                             horz_grid_line_color="grey",
                             vert_grid_line_width=1,
                             vert_grid_line_color="grey"
                             )
        GooCanvas.CanvasGrid(parent=self.root, #Minor lines
                             x=0,
                             y=0,
                             width=self.width,
                             height=self.height,
                             x_step=self.width/NUM_DAYS,
                             y_step=self.hour_height/4.0,
                             horz_grid_line_width=1,
                             horz_grid_line_color="lightgrey",
                             vert_grid_line_width=1,
                             vert_grid_line_color="lightgrey"
                             )
    
    def _drawCourse(self, course):
        for day in enumerate([1, 2, 4, 8, 16]):
            if _occursOnDay(course, day[1]):
                duration = _timeAsDecimal(course['endTime']) - _timeAsDecimal(course['startTime'])
                position_x = day[0] * self.width/NUM_DAYS
                position_y = self.hour_height * (_timeAsDecimal(course['startTime']) - START_HOUR)
                width = self.width/NUM_DAYS
                height = duration * self.hour_height
                GooCanvas.CanvasRect(parent=self.root,
                                     x=int(position_x),
                                     y=int(position_y),
                                     width=int(width),
                                     height=int(height),
                                     fill_color="lightblue"
                                     )
                GooCanvas.CanvasText(parent=self.root,
                                     x=int(position_x),
                                     y=int(position_y),
                                     width=int(width),
                                     height=int(height),
                                     text=course['code']
                                     )
    
    def getContextToolbarItems(self):
        addCourseButton = Gtk.ToolButton()
        icon = Gtk.Image()
        icon.set_from_file(resources.getIconPath("sq_plus"))
        addCourseButton.set_icon_widget(icon)
        addCourseButton.set_label("Add course")
        addCourseButton.set_is_important(True)
        addCourseButton.connect('clicked', self.on_addCourse_clicked)
        return [addCourseButton]
    
    def on_addCourse_clicked(self, button):
        pass