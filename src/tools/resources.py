'''
Created on 2013-12-02

@author: Adam Gignac

Contains paths and other constants that need to be accessed
from multiple places in the application.
'''
import os

NOTES_DIR = os.path.expanduser("~/.isidore")
DATABASE_PATH = os.path.expanduser("~/.config/isidore.db")

def getIcon(name, style="white", size=24):
	assert size in [16, 24, 32, 48]
	path = os.path.join(os.path.dirname(__file__), "icons/%s/png/%s_icon&%d.png" % (style, name, size))
	return path