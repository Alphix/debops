#!/usr/bin/python

import binascii
from ansible.module_utils._text import to_bytes, to_text

def to_hexstr(a, encoding='utf-8', errors='strict', nonstring='strict'):
    return to_text(binascii.hexlify(to_bytes(a, encoding, errors, nonstring)))

class FilterModule(object):
    def filters(self):
        return {'to_hexstr': to_hexstr}


