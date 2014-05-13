import logging
import os
import re
from pyon.lib.io.formats import RE_SCIENTIFIC
from pyon.lib.io.parsers import Parser

__author__ = 'srd1g10'

IWASAKI_REGEX = {
    'filename': ("\w+\.src\d+\."
                 "ch1(?P<charge1>{res})\.ch2(?P<charge2>{res})\.".format(res=RE_SCIENTIFIC) +
                 "m1(?P<mass1>{res})\.m2(?P<mass2>{res})\.".format(res=RE_SCIENTIFIC) +
                 "dat\.(?P<config_number>\d+)"),
    'data': ("^STARTPROP\n"
             "^MASSES:\s\s(?P<m1>{res})\s{{3}}(?P<m2>{res})".format(res=RE_SCIENTIFIC) + "\n"
                                                                                         "^SOURCE:\s(?P<source>\w+)\n"
                                                                                         "^SINKS:\s(?P<sink>\w+)\n"
                                                                                         "(?P<data>" + "(^\d+\s\s{res}\s\s{res}".format(res=RE_SCIENTIFIC)
             + "\n)+)"
               "^ENDPROP"),
    }

IWASAKI_PSEUDO = ("^STARTPROP\n"
             "^MASSES:\s\s(?P<m1>{res})\s{{3}}(?P<m2>{res})".format(res=RE_SCIENTIFIC) + "\n"
                                                                                         "^SOURCE:\sGAM_5\n"
                                                                                         "^SINKS:\sGAM_5\n"
                                                                                         "(?P<data>" + "(^\d+\s\s{res}\s\s{res}".format(res=RE_SCIENTIFIC)
             + "\n)+)"
               "^ENDPROP")
IWASAKI_COMPILED_REGEX = re.compile(IWASAKI_REGEX['data'], re.MULTILINE)
IWASAKI_COMPILED_REGEX_PSEUDO = re.compile(IWASAKI_PSEUDO, re.MULTILINE)


def parse_iwasaki_32c_charged_meson_file(f):
    """
    This is just as slow as regex
    """
    data = []
    fname = os.path.basename(f.name)
    m = re.match(IWASAKI_REGEX['filename'], fname)
    if m:
        charge_1 = int(round(3 * float(m.group('charge1')), 1))
        charge_2 = int(round(3 * float(m.group('charge2')), 1))
        mass_1 = float(m.group('mass1'))
        mass_2 = float(m.group('mass2'))
        config_number = int(m.group('config_number'))
    else:
        raise re.error("Cannot match filename")

    for line in f:
        ls = line.strip()
        split_spaces = ls.split(' ')
        if ls == 'STARTPROP':
            re_data = []
            im_data = []
            time_slices = []
        elif split_spaces[0] == 'MASSES:':
            pass
        elif split_spaces[0] == 'SOURCE:':
            source = split_spaces[1]
        elif split_spaces[0] == 'SINKS:':
            sink = split_spaces[1]
        elif ls == 'ENDPROP':
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
            data.append(dic)
        else:
            t, real, im = ls.split()
            time_slices.append(int(t))
            re_data.append(float(real))
            im_data.append(float(im))
    return data


# class Iwasaki32cCharged(Parser):
#     def get_from_file(self, file_name):
#         return parse_iwasaki_32c_charged_meson_file_regex(file_name)


class Iwasaki32cCharged(Parser):
    def __init__(self, pseudo=True):
        self.pseudo = pseudo

    def get_from_file(self, file_name):
        """
        Parse all the data from an Iwasaki Charged Meson file e.g. \
        meson_BOX_RELOADED.src0.ch1-0.3333333333.ch2-0.3333333333.m10.03.m20.03.dat.510
        """
        data = []
        raw_data = file_name.read()
        fname = os.path.basename(file_name.name)
        m = re.match(IWASAKI_REGEX['filename'], fname)
        if m:
            charge_1 = int(round(3 * float(m.group('charge1')), 1))
            charge_2 = int(round(3 * float(m.group('charge2')), 1))
            mass_1 = float(m.group('mass1'))
            mass_2 = float(m.group('mass2'))
            config_number = int(m.group('config_number'))
        else:
            raise re.error("Cannot match filename")
        if self.pseudo:
            r = IWASAKI_COMPILED_REGEX_PSEUDO
        else:
            r = IWASAKI_COMPILED_REGEX
        matched = [m.groupdict() for m in r.finditer(raw_data)]
        for match in matched:
            if self.pseudo:
                source = 'GAM_5'
                sink = 'GAM_5'
            else:
                source = match['source']
                sink = match['sink']
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
            data.append(dic)
        return data


