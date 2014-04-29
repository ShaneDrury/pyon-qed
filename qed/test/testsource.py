import os
import unittest
from pyon.runner import register
from pyon.runner.register import registered_sources
from pyon.runner.sources import FileSource

# def my_source():
#     folder = os.path.join('testfiles', 'correlators', 'f1')
#     data_format = 'iwasaki_32c'
#     parser = registered_parsers[data_format]()
#     raw_data = parser.get_from_folder(folder)
#     return QuerySet(raw_data)


@register.source('my_source')
class MySource(FileSource):
    folder = os.path.join('testfiles', 'correlators', 'f1')
    data_format = 'iwasaki_32c'


class TestSource(unittest.TestCase):
    def setUp(self):
        self.my_source = registered_sources['my_source']()

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
