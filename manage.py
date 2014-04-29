"""
Inspired heavily by Django.
"""
import os
from pyon.runner.app import App
import logging
from jinja2 import Environment, PackageLoader
import sys
#from pyon.runner.db import Database
import qed.lib.fitting


APP_NAME = 'delta_m_squared'
APP_FOLDER = 'qed'
DB_NAME = 'qed'
DB_USERNAME = 'srd1g10'


def start_runner():
    env = Environment(loader=PackageLoader('qed', 'templates'))
    template = env.get_template('qed/index.html')
    logging.basicConfig(level=logging.DEBUG)
    app = App(APP_FOLDER, name=APP_NAME,
              dump_dir=os.path.join(os.getcwd(), 'results'),
              template=template)
    app.main()


def populate_db():
    with Database(db_name=DB_NAME, username=DB_USERNAME) as db:
        pass

command_dict = {
    'start': start_runner,
    'populatedb': populate_db,
}

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Parameter must be one of {}".format(list(command_dict.keys())))
        exit()
    command = sys.argv[1]

    command_dict[command]()
    #start_runner()
