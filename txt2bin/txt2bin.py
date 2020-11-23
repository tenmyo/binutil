#!/usr/bin/python
import argparse
import os
from struct import Struct
import sys

def evalute(in_fp, out_fp, byteorder):
    int_fmt = {
        'native': {
            'i8': Struct('=b'),
            'u8': Struct('=B'),
            'i16': Struct('=h'),
            'u16': Struct('=H'),
            'i32': Struct('=l'),
            'u32': Struct('=L'),
            'i64': Struct('=q'),
            'u64': Struct('=Q'),
        },
        'big': {
            'i8': Struct('>b'),
            'u8': Struct('>B'),
            'i16': Struct('>h'),
            'u16': Struct('>H'),
            'i32': Struct('>l'),
            'u32': Struct('>L'),
            'i64': Struct('>q'),
            'u64': Struct('>Q'),
        },
        'little': {
            'i8': Struct('<b'),
            'u8': Struct('<B'),
            'i16': Struct('<h'),
            'u16': Struct('<H'),
            'i32': Struct('<l'),
            'u32': Struct('<L'),
            'i64': Struct('<q'),
            'u64': Struct('<Q'),
        },
    }
    float_fmt = {
        'native': {
            'f32': Struct('=f'),
            'f64': Struct('=d'),
        },
        'big': {
            'f32': Struct('>f'),
            'f64': Struct('>d'),
        },
        'little': {
            'f32': Struct('<f'),
            'f64': Struct('<d'),
        },
    }
    for line in in_fp:
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        cmd, args = line.split(None, 1)
        if cmd in int_fmt[byteorder]:
            for arg in args.split():
                buf = int_fmt[byteorder][cmd].pack(int(arg, base=0))
                out_fp.write(buf)
        elif cmd in float_fmt[byteorder]:
            for arg in args.split():
                buf = float_fmt[byteorder][cmd].pack(float(arg))
                out_fp.write(buf)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('text_file', help='text file')
    parser.add_argument('-o', '--out',
                        metavar='out_file',
                        help='binary output file')
    parser.add_argument('--byteorder',
                        help='default byte order',
                        default='native',
                        choices=('native', 'big', 'little', ))
    args = parser.parse_args(argv)

    out_fpath = args.out
    if not out_fpath:
        out_fpath = os.path.splitext(args.text_file)[0] + '.bin'
    
    with open(args.text_file, 'r') as in_fp:
        with open(out_fpath, 'wb') as out_fp:
            evalute(in_fp, out_fp, args.byteorder)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
