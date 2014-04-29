"""
Inspired heavily by Django.
"""
from pyon.runner.app import App
import logging
from jinja2 import Environment, PackageLoader
import sys
from pyon.runner.db import main
from settings import APP_FOLDER, APP_NAME, DUMP_DIR, DB_PATH


def start_runner():
    env = Environment(loader=PackageLoader('qed', 'templates'))
    template = env.get_template('qed/index.html')
    logging.basicConfig(level=logging.DEBUG)
    app = App(APP_FOLDER, name=APP_NAME,
              dump_dir=DUMP_DIR,
              template=template,
              db_path=DB_PATH)
    app.main()


def populate_db():
    main()
    # with Database(db_name=DB_NAME, username=DB_USERNAME) as db:
    #     pass

command_dict = {
    'start': start_runner,
    'populatedb': populate_db,
}

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Parameter must be one of {}".format(list(command_dict.keys())))
        exit()
    command = sys.argv[1]
    try:
        command_dict[command]()
    except KeyError:
        print("Parameter must be one of {}".format(list(command_dict.keys())))
        exit()
    #start_runner()
