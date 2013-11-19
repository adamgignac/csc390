'''
Created on 2013-10-24

Written by Micah Carrick
(http://www.micahcarrick.com/gtk-notebook-tabs-with-close-button.html)

'''

from gi.repository import Gtk, GObject

class TabLabel(Gtk.Box):
    '''
    A label with a close button for use in a Gtk.Notebook
    '''


    __gsignals__ = {
        "close-clicked": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, labelText):
        '''
        Constructor
        '''
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_spacing(5) # spacing: [icon|5px|label|5px|close]  
        
        # icon
        icon = Gtk.Image.new_from_stock(Gtk.STOCK_FILE, Gtk.IconSize.MENU)
        self.pack_start(icon, False, False, 0)
        
        # label 
        label = Gtk.Label(labelText)
        self.pack_start(label, True, True, 0)
        
        # close button
        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.set_focus_on_click(False)
        button.add(Gtk.Image.new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU))
        button.connect("clicked", self.button_clicked)
        data =  ".button {\n" \
                "-GtkButton-default-border : 0px;\n" \
                "-GtkButton-default-outside-border : 0px;\n" \
                "-GtkButton-inner-border: 0px;\n" \
                "-GtkWidget-focus-line-width : 0px;\n" \
                "-GtkWidget-focus-padding : 0px;\n" \
                "padding: 0px;\n" \
                "}"
        provider = Gtk.CssProvider()
        provider.load_from_data(data)
        # 600 = GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
        button.get_style_context().add_provider(provider, 600) 
        self.pack_start(button, False, False, 0)
        
        self.show_all()
    
    def button_clicked(self, button, data=None):
        self.emit("close-clicked")