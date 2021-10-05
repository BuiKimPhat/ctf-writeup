#!/usr/bin/env python3
from random import choice
from string import *
import signal
from os import system,environ
import sys

def handler(x, y):
    sys.exit(1)

TIMEOUT = 60
if "HASHCASH_TIMEOUT" in environ:
    TIMEOUT = int(environ["HASHCASH_TIMEOUT"])

signal.signal(signal.SIGALRM, handler)
signal.alarm(TIMEOUT)

LENGTH = 9
STRENGTH = 26
if "HASHCASH_LENGTH" in environ:
    LENGTH = int(environ["HASHCASH_LENGTH"])
if "HASHCASH_STRENGTH" in environ:
    STRENGTH = int(environ["HASHCASH_STRENGTH"])

def gen_randstr(length=LENGTH):
    return ''.join((choice(ascii_lowercase) for i in range(length)))

def main():
    s = gen_randstr()
    print("[Proof of Work]")
    print("Submit the token generated by `hashcash -mb{} {}`".format(STRENGTH, s))
    ans = input()
    ans_chrs = ascii_letters + digits + ":/+"
    l = list(filter(lambda c: c not in ans_chrs, ans))
    if len(l) != 0:
        exit(1)
    r = system("hashcash -cdb{} -f /hashcash/hashdb -r {} {}".format(STRENGTH, s, ans))
    exit(0 if r == 0 else 1)

if "DEBUG" in environ:
    pass
else:
    main()
