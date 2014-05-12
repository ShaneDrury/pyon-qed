"""
Inspired heavily by Django.
"""
import os
from parsers import Iwasaki32cCharged
from settings import DUMP_DIR, LOGGING_LEVEL, MEASUREMENTS
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import logging
logging.basicConfig(level=LOGGING_LEVEL)  # Put this first to make global
from delmsq.models import TimeSlice, Iwasaki32cChargedMeson
from pyon.runner.project import Project
import sys


def start_runner(*args):
    project = Project(name='QED',
                      dump_dir=DUMP_DIR)
    for measurement in MEASUREMENTS:
        project.register_measurement(measurement)
    project.main()


def populate_db(*args):
    parse_from_folder(os.path.join('data', '32c', 'IWASAKI+DSDR', 'ms0.045',
                                   'mu0.0042'))


def parse_from_folder(folder):
    all_data = Iwasaki32cCharged().get_from_folder(folder)
    for d in all_data:
        if not (d['source'] == 'GAM_5' and d['sink'] == 'GAM_5'):
            continue
        logging.debug("Processing {} {} {}".format((d['mass_1'], d['mass_2']),
                                                   (d['charge_1'],
                                                    d['charge_2']),
                                                   d['config_number']))
        re_dat = d.pop('data')
        im_dat = d.pop('im_data')
        time_slices = d.pop('time_slices')
        mes = Iwasaki32cChargedMeson(**d)
        mes.save()
        for t, re, im in zip(time_slices, re_dat, im_dat):
            time_slice = TimeSlice(t=t, re=re, im=im)
            mes.data.add(time_slice)
    logging.debug("Done!")


command_dict = {
    'start': start_runner,
    'populatedb': populate_db,
    }

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Parameter must be one of {}".format(list(command_dict.keys())))
        exit()
    command = sys.argv[1]
    args = sys.argv[2:]
    if command in command_dict:
        command_dict[command](*args)
    else:
        print("Parameter must be one of {}".format(list(command_dict.keys())))
        exit()
