#!/usr/bin/env python

import subprocess
from struct import unpack
from binascii import unhexlify

# Page 53
# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
codes = {
        0x4:  ['a','A'],
        0x5:  ['b','B'],
        0x6:  ['c','C'],
        0x7:  ['d','D'],
        0x8:  ['e','E'],
        0x9:  ['f','F'],
        0xa:  ['g','G'],
        0xb:  ['h','H'],
        0xc:  ['i','I'],
        0xd:  ['j','J'],
        0xe:  ['k','K'],
        0xf:  ['l','L'],
        0x10: ['m','M'],
        0x11: ['n','N'],
        0x12: ['o','O'],
        0x13: ['p','P'],
        0x14: ['q','Q'],
        0x15: ['r','R'],
        0x16: ['s','S'],
        0x17: ['t','T'],
        0x18: ['u','U'],
        0x19: ['v','V'],
        0x1a: ['w','W'],
        0x1b: ['x','X'],
        0x1c: ['y','Y'],
        0x1d: ['z','Z'],
        0x1e: ['1','!'],
        0x1f: ['2','@'],
        0x20: ['3','#'],
        0x21: ['4','$'],
        0x22: ['5','%'],
        0x23: ['6','^'],
        0x24: ['7','&'],
        0x25: ['8','*'],
        0x26: ['9','('],
        0x27: ['0',')'],

        0x2d: ['-','_'],

        0x2f: ['[','{'],
        0x30: [']','}'],
        

}

# TODO: Filter down further on what packets to look at.
def dumpData(fileName):
    return subprocess.check_output(["tshark","-r",fileName,"-T","fields","-e","usb.capdata"]).strip(b"\n").split(b"\n")


def parseData(data):
    out = ""

    for line in data:
        a,b,c,d = unpack("<HHHH",unhexlify(line.replace(b':',b'')))

        # We don't have a key stroke here
        if b == 0:
            continue

        if a not in [0,0x20]:
            print("Not sure what this ctrl value is ({0}), skipping.".format(a))
            continue

        # Shift
        shift = a == 0x20

        # Add in the char
        out += codes[b][shift]

    return out
