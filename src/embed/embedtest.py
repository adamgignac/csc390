'''
Created on 2013-12-23

@author: Adam Gignac
'''
import unittest

import os, imp, sys

class Test(unittest.TestCase):

    def testRegisteringEmbedTypes(self):
        #Search embed module for embed types
        pluginpath = imp.find_module("embed")[1]
        ignore = ('test', 'init')
        pluginfiles = [fname[:-3] for fname in os.listdir(pluginpath) if fname.endswith(".py") and not any([i in fname for i in ignore])]
        if not pluginpath in sys.path:
            sys.path.append(pluginpath)
        imported_types = [__import__(fname) for fname in pluginfiles]
        for mod in imported_types:
            mod.register()

if __name__ == "__main__":
    unittest.main()
