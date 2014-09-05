import logging
import os
import re

from pyon.lib.io.formats import RE_SCIENTIFIC
from pyon.lib.io.parsers import Parser


log = logging.getLogger(__name__)

KAON_LEC_REGEX = {
    'filename': '(?P<config_number>\d+)',
    'data': '^LS=(?P<LS>{res})\n'
            '^B0=(?P<B0>{res})\n'
            '^F0/sqrt\(2\)=(?P<F0>{res})\n'
            '^L64=(?P<L64>{res})\n'
            '^L85=(?P<L85>{res})\n'
            '^L4=(?P<L4>{res})\n'
            '^L5=(?P<L5>{res})\n'
            '^MRES=(?P<MRES>{res})\n'
            '^miu=(?P<miu>{res})\n'
            '^M2=(?P<M2>{res})\n'
            '^A3=(?P<A3>{res})\n'
            '^A4=(?P<A4>{res})\n'
            '^DMRES=(?P<DMRES>{res})\n'.format(res=RE_SCIENTIFIC)
}

LEC_COMPILED_REGEX = re.compile(KAON_LEC_REGEX['data'], re.MULTILINE)


class KaonLECParser(Parser):
    def get_from_file(self, fp):
        raw_data = fp.read()
        fname = os.path.basename(fp.name)
        m = re.match(KAON_LEC_REGEX['filename'], fname)
        if m:
            config_number = int(m.group('config_number'))
        else:
            raise re.error("Cannot match filename")
        r = LEC_COMPILED_REGEX
        m = re.match(r, raw_data)
        if m:
            dic = {
                'config_number': config_number,
                'M2': float(m.group('M2')),
                'A_3': float(m.group('A3')),
                'A_4': float(m.group('A4')),
            }
            log.debug(dic)
        else:
            raise re.error("Cannot match file")
        return dic

    def get_from_files(self, list_of_files):
        raw_data = []
        for ff in list_of_files:
                with open(ff, 'r') as f:
                    raw_data.append(self.get_from_file(f))
        return raw_data
