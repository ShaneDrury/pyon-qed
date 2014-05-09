"""
Define your data sources here.
"""
# import os
# from pyon.runner.sources import FileSource, DBSource


# @register.source('32c_mu0.0042')
# def charged_mesons():
#     folder = os.path.join('data', '32c', 'IWASAKI+DSDR', 'ms0.045',
#                           'mu0.0042')
#     data_format = 'iwasaki_32c'
#     parser = registered_parsers[data_format]()
#     raw_data = parser.get_from_folder(folder)
#     return QuerySet(raw_data)


# class MesonSource(FileSource):
#     folder = os.path.join('data', '32c', 'IWASAKI+DSDR', 'ms0.045',
#                           'mu0.0042')
#     data_format = 'iwasaki_32c'
#
#
# class MesonDBSource(DBSource):
#     db_path = 'qed.db'
#     table_name = 'qed'
