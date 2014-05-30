from collections import defaultdict
import logging
import os
import re
from django.db.models import Max
from pyon.lib.io.formats import RE_SCIENTIFIC
from pyon.lib.io.parsers import Parser
from meas24c.models import ChargedMeson24c, TimeSlice, Correlator

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

    def get_from_file(self, fp):
        """
        Parse all the data from an Iwasaki 24c Charged Meson file e.g. \
        emspect.data.1020
        """
        data = []
        already_done = set()
        raw_data = fp.read()
        fname = os.path.basename(fp.name)
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


def parse_correlators_from_folder(folder, m_l):
    logging.debug("Parsing from file")
    all_data = Iwasaki24cCharged(pseudo=True).get_from_folder(folder)
    logging.debug("Creating objects")
    mesons = defaultdict(list)
    for d in all_data:
        if not (d['source'] == 'GFWALL' and d['sink'] == 'GAM_5'):
            continue
        logging.debug("Processing {} {} {}".format((d['mass_1'], d['mass_2']),
                                                   (d['charge_1'],
                                                    d['charge_2']),
                                                   d['config_number']))

        re_dat = d.pop('data')
        d.pop('im_data')

        time_slices = d.pop('time_slices')
        d['m_l'] = m_l

        time_slices = [TimeSlice(t=t, re=real)
                       for t, real in zip(time_slices, re_dat)]
        key = (m_l, d['source'], d['sink'], d['mass_1'],
               d['mass_2'], d['charge_1'], d['charge_2'])
        mesons[key].append({'config_number': d['config_number'],
                            'data': time_slices})

    for k, v in mesons.items():
        m_l, source, sink, mass_1, mass_2, charge_1, charge_2 = k
        correlators = [Correlator(**t) for t in v]
        mes = ChargedMeson24c(source=source, sink=sink, m_l=m_l,
                              mass_1=mass_1, mass_2=mass_2,
                              charge_1=charge_1, charge_2=charge_2,
                              correlators=correlators)
        mes.save()
