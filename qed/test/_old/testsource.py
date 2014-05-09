import os
import unittest
from pyon.lib.io.parsers import Iwasaki32c
from pyon.runner.sources import FileSource


# def my_source():  # can use this
#     folder = os.path.join('testfiles', 'correlators', 'f1')
#     parser = Iwasaki32c()
#     raw_data = parser.get_from_folder(folder)
#     return QuerySet(raw_data)


class MySource(FileSource):  # easier?
    folder = os.path.join('../testfiles', 'correlators', 'f1')
    parser = Iwasaki32c()


class TestSource(unittest.TestCase):
    def setUp(self):
        self.my_source = MySource()

    def test_create_source(self):
        self.assertTrue(self.my_source)

    def test_parse_source(self):
        qs = self.my_source
        filtered = qs.filter(masses=(0.03, 0.03), charges=(-1, -1))
        filtered.sort('config_number')
        fd = filtered[0]
        self.assertEqual(fd['config_number'], 510)

    def test_fail_parse_source(self):
        qs = self.my_source
        self.assertRaises(ValueError, qs.filter, masses=(-5, 132), charges=(9, 3))
