import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_1(self):
        md = "# This is a Title   "
        title = extract_title(md)
        self.assertEqual("This is a Title", title)
    
    def test_extract_title_exception(self):
        md = "This is a not Title   "
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_multiple_lines(self):
        md = "This is a not Title\n this is also not a title\n# Here Title\n hello there"
        title = extract_title(md)
        self.assertEqual("Here Title", title)

    def test_extract_title_leading_spaces_in_title(self):
        md = "#   My Awesome Title"
        title = extract_title(md)
        self.assertEqual("My Awesome Title", title)
    
if __name__ == "__main__":
    unittest.main()
