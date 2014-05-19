import os
from pyon.lib.io.formats import RE_SCIENTIFIC
from pyon.lib.io.parsers import Parser
import re
from meas24c.models import PionLEC


PION_LEC_REGEX = {
    'filename': '(?P<config_number>\d+)',
    'data': '^LS=(?P<LS>{res})\n'
            '^B0=(?P<B0>{res})\n'
            '^F0/sqrt\(2\)=(?P<F0>{res})\n'
            '^L64=(?P<L64>{res})\n'
            '^L85=(?P<L85>{res})\n'
            '^L4=(?P<L4>{res})\n'
            '^L5=(?P<L5>{res})\n'
            '^MRES=(?P<MRES>{res})\n'
            '^miu=(?P<miu>{res})\n'.format(res=RE_SCIENTIFIC)
}

LEC_COMPILED_REGEX = re.compile(PION_LEC_REGEX['data'], re.MULTILINE)


class PionLECParser(Parser):
    def get_from_file(self, fp):
        raw_data = fp.read()
        fname = os.path.basename(fp.name)
        m = re.match(PION_LEC_REGEX['filename'], fname)
        if m:
            config_number = int(m.group('config_number'))
        else:
            raise re.error("Cannot match filename")
        r = LEC_COMPILED_REGEX
        m = re.match(r, raw_data)
        if m:
            dic = {
                'config_number': config_number,
                'LS': float(m.group('LS')),
                'B0': float(m.group('B0')),
                'F0': float(m.group('F0')),
                'L64': float(m.group('L64')),
                'L85': float(m.group('L85')),
                'L4': float(m.group('L4')),
                'L5': float(m.group('L5')),
                'm_res': float(m.group('MRES')),
                'miu': float(m.group('miu')),
            }
        else:
            raise re.error("Cannot match file")
        return dic

    def get_from_files(self, list_of_files):
        raw_data = []
        for ff in list_of_files:
                with open(ff, 'r') as f:
                    raw_data.append(self.get_from_file(f))
        return raw_data


def parse_lecs_from_folder(folder):
    all_data = PionLECParser().get_from_folder(folder)
    bulk_list = [PionLEC(**d) for d in all_data]
    PionLEC.objects.bulk_create(bulk_list)
