"""
Define your data sources here.
"""
import os
from pyon import register, registered_parsers, registered_sources
from pyon.runner.query import QuerySet
from pyon.runner.sources import Source, FileSource


# @register.source('32c_mu0.0042')
# def charged_mesons():
#     folder = os.path.join('data', '32c', 'IWASAKI+DSDR', 'ms0.045',
#                           'mu0.0042')
#     data_format = 'iwasaki_32c'
#     parser = registered_parsers[data_format]()
#     raw_data = parser.get_from_folder(folder)
#     return QuerySet(raw_data)

@register.source('32c_mu0.0042')
class MesonSource(FileSource):
    folder = os.path.join('data', '32c', 'IWASAKI+DSDR', 'ms0.045',
                          'mu0.0042')
    data_format = 'iwasaki_32c'