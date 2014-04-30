"""
Inspired heavily by Django.
"""
from pyon.runner.app import App
import logging
from jinja2 import Environment, PackageLoader
import sys
from pyon.runner.db import main
from settings import APP_FOLDER, APP_NAME, DUMP_DIR, DB_PATH


def start_runner(*args):
    env = Environment(loader=PackageLoader('qed', 'templates'))
    template = env.get_template('qed/index.html')
    logging.basicConfig(level=logging.DEBUG)
    app = App(APP_FOLDER, name=APP_NAME,
              dump_dir=DUMP_DIR,
              template=template,
              db_path=DB_PATH)
    app.main()


def populate_db(*args):
    main()
    # with Database(db_name=DB_NAME, username=DB_USERNAME) as db:
    #     pass


def create_report(result_path):
    env = Environment(loader=PackageLoader('qed', 'templates'))
    template = env.get_template('qed/index.html')
    logging.basicConfig(level=logging.DEBUG)
    app = App(APP_FOLDER, name=APP_NAME,
              dump_dir=DUMP_DIR,
              template=template,
              db_path=DB_PATH)

    logging.debug("Reading {}".format(result_path[0]))
    report = app.read_result(result_path[0])
    date = report.pop('date')
    sim_name = report.pop('sim_name')
    app.write_report(sim_name, date, report)


command_dict = {
    'start': start_runner,
    'populatedb': populate_db,
    'createreport': create_report,
}

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Parameter must be one of {}".format(list(command_dict.keys())))
        exit()
    command = sys.argv[1]
    args = sys.argv[2:]
    try:
        command_dict[command](args)
    except KeyError:
        print("Parameter must be one of {}".format(list(command_dict.keys())))
        exit()
    #start_runner()
