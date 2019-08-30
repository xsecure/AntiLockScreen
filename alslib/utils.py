#!/usr/bin/env pythonw3
#-*- coding=utf-8 -*-

def make_str(value, prefer_encodeings=None):
    if prefer_encodeings is None:
        prefer_encodeings = ['utf-8', 'utf16', 'gbk', 'gbk?']

    if isinstance(value, str) or isinstance(value, bool) or value is None:
        return value

    for enc in prefer_encodeings:
        try:
            if enc.endswith('!'):
                return value.decode(enc[:-1], 'ignore')
            elif enc.endswith('?'):
                return value.decode(enc[:-1], 'replace')
            elif enc.endswith('&'):
                return value.decode(enc[:-1], 'xmlcharrefreplace')
            elif enc.endswith('\\'):
                return value.decode(enc[:-1], 'backslashreplace')
            else:
                return value.decode(enc)
        except UnicodeError:
            pass
    else:
        raise

def make_bytes(value, encoding_type=None, prefer_encodeings=None):
    uv = make_str(value, prefer_encodeings)
    if uv is None:
        return None
    if encoding_type is None:
        encoding_type = 'utf-8'
    return uv.encode(encoding_type, 'xmlcharrefreplace')