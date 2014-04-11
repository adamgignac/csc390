'''
Created on 2014-03-31

@author: Adam Gignac
'''

from gi.repository import Gtk
from embedcontextpane import EmbedContextPane

TEMPLATE = """
</p>
<p><strong>{title}<strong></p>
<button onClick="addRow('{id}')">Add row</button><button onClick="addColumn('{id}')">Add column</button>
<table class="table table-bordered" id="{id}">
	<tr>
		<td>
			Data
		</td>
		<td>
			Data
		</td>
	</tr>
	<tr>
		<td>
			Data
		</td>
		<td>
			Data
		</td>
	</tr>
</table>
<p>
"""

class TableContextPane(Gtk.HBox, EmbedContextPane):
    def __init__(self):
        super(TableContextPane, self).__init__()
        self.label = Gtk.Label("Title:")
        self.tableTitle = Gtk.Entry()
        self.add(self.label)
        self.add(self.tableTitle)
        self.show_all()
    
    def getHtml(self):
    	title = self.tableTitle.get_text()
    	tableID = "table_" + title.lower().replace(" ", "")
        return TEMPLATE.format(title=title, id=tableID)

def register():
    return ("Table", TableContextPane())
