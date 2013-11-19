from textnote import TextNote
import unittest

class TextNoteTestCase(unittest.TestCase):
    def setUp(self):
        self.note = TextNote()
    
    def test_contextToolbar(self):
        toolbarItems = self.note.getContextToolbarItems()
        assert toolbarItems is not None
        assert len(toolbarItems) >= 0

if __name__ == "__main__":
    unittest.main()
