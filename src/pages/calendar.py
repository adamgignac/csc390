'''
Created on 2014-02-16

@author: adam
'''
from pages.page import Page
from gi.repository import Gtk, GooCanvas

def _occursOnDay(course, day):
    return course['days'] & day

def _timeAsDecimal(time):
    t = time.split(":")
    return float(t[0]) + float(t[1])/60

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
        self.draw(allocation.width, allocation.height)
    
    def draw(self, width, height):
        self.set_bounds(0, 0, width, height)
        HOURS = 14
        NUM_DAYS = 5
        HOUR_HEIGHT = height/HOURS
        GooCanvas.CanvasRect(parent=self.root,
                             x=0,
                             y=0,
                             width=width,
                             height=height,
                             fill_color="white")
        GooCanvas.CanvasGrid(parent=self.root, #Major lines
                             x=0,
                             y=0,
                             width=width,
                             height=height,
                             x_step=width/NUM_DAYS,
                             y_step=HOUR_HEIGHT,
                             horz_grid_line_width=1,
                             horz_grid_line_color="grey",
                             vert_grid_line_width=1,
                             vert_grid_line_color="grey"
                             )
        GooCanvas.CanvasGrid(parent=self.root, #Minor lines
                             x=0,
                             y=0,
                             width=width,
                             height=height,
                             x_step=width/NUM_DAYS,
                             y_step=HOUR_HEIGHT/4,
                             horz_grid_line_width=1,
                             horz_grid_line_color="lightgrey",
                             vert_grid_line_width=1,
                             vert_grid_line_color="lightgrey"
                             )
        for course in self.courses:
            for day in enumerate([1, 2, 4, 8, 16]):
                if _occursOnDay(course, day[1]):
                    duration = _timeAsDecimal(course['endTime']) - _timeAsDecimal(course['startTime'])
                    GooCanvas.CanvasRect(parent=self.root,
                                         x=day[0] * width/NUM_DAYS,
                                         y=HOUR_HEIGHT * _timeAsDecimal(course['startTime']),
                                         width=width/NUM_DAYS,
                                         height=duration * HOUR_HEIGHT,
                                         fill_color="red"
                                         )
    
    def getContextToolbarItems(self):
        addCourseButton = Gtk.ToolButton(Gtk.STOCK_NEW)
        addCourseButton.set_label("Add course")
        addCourseButton.set_is_important(True)
        return [addCourseButton]