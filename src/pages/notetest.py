from textnote import TextNote
from searchresult import SearchResult
import unittest

class AbstractTestCase():
    def test_contextToolbar(self):
        toolbarItems = self.page.getContextToolbarItems()
        assert toolbarItems is not None
        assert len(toolbarItems) >= 0

class TextNoteTestCase(AbstractTestCase, unittest.TestCase):
    def setUp(self):
        self.page = TextNote()

class SearchResultTestCase(AbstractTestCase, unittest.TestCase):
    def setUp(self):
        self.page = SearchResult("none")

if __name__ == "__main__":
    unittest.main()
