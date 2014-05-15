"""
Inspired heavily by Django.
"""
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qed.settings")
# from django.conf import settings
# #from parsers import Iwasaki32cCharged
# from delmsq.models import TimeSlice, ChargedMeson
# from pyon.runner.project import Project
# import sys
# import logging
# # logging.basicConfig(level=settings.LOGGING_LEVEL)  # Put this first to make global
# #
# #
# # def start_runner():
# #     project = Project(name=settings.PROJECT_NAME,
# #                       dump_dir=settings.DUMP_DIR)
# #     project.main()
#
#
#
#
#
# command_dict = {
#     'populatedb': populate_db,
# }
#
# if __name__ == '__main__':
#     if len(sys.argv) == 1:
#         print("Parameter must be one of {}".format(list(command_dict.keys())))
#         exit()
#     command = sys.argv[1]
#     args = sys.argv[2:]
#     if command in command_dict:
#         command_dict[command](*args)
#     else:
#         print("Parameter must be one of {}".format(list(command_dict.keys())))
#         exit()
