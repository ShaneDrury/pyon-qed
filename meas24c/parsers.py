import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qed.settings")
from django.conf import settings
from django.db.models import Max
from meas24c.models import ChargedMeson24c, TimeSlice
import logging
logging.basicConfig(level=settings.LOGGING_LEVEL)
import re
from pyon.lib.io.formats import RE_SCIENTIFIC
from pyon.lib.io.parsers import Parser

__author__ = 'srd1g10'

IWASAKI_24C_REGEX = {
    'filename': "emspect\.dat\.(?P<config_number>\d+)",
    'data': (
        "^STARTPROP\n"
        "^MASSES:\s\s(?P<m1>{res})\s{{3}}(?P<m2>{res})".format(res=RE_SCIENTIFIC) + "\n"
        "^CHARGES:\s\s(?P<q1>{res})\s{{3}}(?P<q2>{res})\n"
        "(meson\stotal\scharge:\s{res})".format(res=RE_SCIENTIFIC) + "\n"
        "^SOURCE:\s(?P<source>\w+)\n"
        "^SINKS:\s(?P<sink>\w+)\n"
        "(?P<data>" + "(^\d+\s\s{res}\s\s{res}".format(res=RE_SCIENTIFIC)
        + "\n)+)"
          "^ENDPROP"),
}

EM_CHARGE = 1.0095398470766666e-01
IWASAKI_24C_PSEUDO = (
    "^STARTPROP\n"
    "^MASSES:\s\s(?P<m1>{res})\s{{3}}(?P<m2>{res})".format(res=RE_SCIENTIFIC) + "\n"
    "^CHARGES:\s\s(?P<q1>{res})\s{{3}}(?P<q2>{res})".format(res=RE_SCIENTIFIC) + "\n"
    ".*\n"
    "^SOURCE:\sGFWALL\n"
    "^SINKS:\sGAM_5\n"
    "(?P<data>" + "(^\d+\s\s{res}\s\s{res}".format(res=RE_SCIENTIFIC)
    + "\n)+)"
      "^ENDPROP")

IWASAKI_COMPILED_REGEX = re.compile(IWASAKI_24C_REGEX['data'], re.MULTILINE)
IWASAKI_COMPILED_REGEX_PSEUDO = re.compile(IWASAKI_24C_PSEUDO, re.MULTILINE)


class Iwasaki24cCharged(Parser):
    def __init__(self, pseudo=True):
        self.pseudo = pseudo

    def get_from_file(self, file_name):
        """
        Parse all the data from an Iwasaki 24c Charged Meson file e.g. \
        emspect.data.1020
        """
        data = []
        already_done = set()
        raw_data = file_name.read()
        fname = os.path.basename(file_name.name)
        m = re.match(IWASAKI_24C_REGEX['filename'], fname)
        if m:
            config_number = int(m.group('config_number'))
        else:
            raise re.error("Cannot match filename")
        if self.pseudo:
            r = IWASAKI_COMPILED_REGEX_PSEUDO
        else:
            r = IWASAKI_COMPILED_REGEX
        matched = [m.groupdict() for m in r.finditer(raw_data)]
        if not matched:
            raise ValueError("No matches")
        for match in matched:
            if self.pseudo:
                source = 'GFWALL'
                sink = 'GAM_5'
            else:
                source = match['source']
                sink = match['sink']

            charge_1 = int(round(float(match['q1']) / EM_CHARGE, 1))
            charge_2 = int(round(float(match['q2']) / EM_CHARGE, 1))
            mass_1 = float(match['m1'])
            mass_2 = float(match['m2'])
            re_data = []
            im_data = []
            time_slices = []
            for line in match['data'].split('\n'):
                try:
                    n, re_c, im_c = line.split()
                    re_c = float(re_c)
                    im_c = float(im_c)
                    n = int(n)
                    re_data.append(re_c)
                    im_data.append(im_c)
                    time_slices.append(n)
                except ValueError:
                    pass
            dic = {'source': source,
                   'sink': sink,
                   'data': re_data,
                   'im_data': im_data,
                   'time_slices': time_slices,
                   'mass_1': mass_1,
                   'mass_2': mass_2,
                   'charge_1': charge_1,
                   'charge_2': charge_2,
                   'config_number': config_number}

            params = (source,
                      sink,
                      mass_1,
                      mass_2,
                      charge_1,
                      charge_2,
                      config_number)

            if params not in already_done:
                data.append(dic)
                already_done.add(params)
        return data


def populate_db():
    logging.debug("Adding 0.02")
    parse_from_folder(os.path.join('data', '24c', '0.02'), 0.02)
    logging.debug("Adding 0.005")
    parse_from_folder(os.path.join('data', '24c', '0.005'), 0.005)
    logging.debug("Adding 0.03")
    parse_from_folder(os.path.join('data', '24c', '0.03'), 0.03)
    logging.debug("Adding 0.001, 0.005")
    parse_from_folder(os.path.join('data', '24c', 'mv0.001-msea0.005'), 0.005)
    logging.debug("Adding 0.001, 0.01")
    parse_from_folder(os.path.join('data', '24c', 'mv0.001-msea0.01'), 0.01)
    logging.debug("Adding 0.01")
    parse_from_folder(os.path.join('data', '24c', '0.01-1-180'), 0.01)


def parse_from_folder(folder, m_l):
    all_data = Iwasaki24cCharged(pseudo=True).get_from_folder(folder)
    id_start = (ChargedMeson24c.objects.aggregate(Max('id'))['id__max'] or 0) + 1
    bulk_mesons = []
    for d in all_data:
        if not (d['source'] == 'GFWALL' and d['sink'] == 'GAM_5'):
            continue
        # logging.debug("Processing {} {} {} {}".format((d['mass_1'], d['mass_2']),
        #                                            (d['charge_1'],
        #                                             d['charge_2']),
        #                                            d['config_number'], id_start))
        re_dat = d.pop('data')
        im_dat = d.pop('im_data')
        time_slices = d.pop('time_slices')
        d['m_l'] = m_l
        d['id'] = id_start
        id_start += 1
        mes = ChargedMeson24c(**d)
        #mes.save()
        bulk_list = [TimeSlice(meson=mes, t=t, re=real, im=im)
                     for t, real, im in zip(time_slices, re_dat, im_dat)]
        TimeSlice.objects.bulk_create(bulk_list)
        bulk_mesons.append(mes)
    ChargedMeson24c.objects.bulk_create(bulk_mesons)

if __name__ == '__main__':
    populate_db()