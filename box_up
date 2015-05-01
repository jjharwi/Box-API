#!/usr/bin/python

from __future__ import print_function
import argparse

from ConfigParser import SafeConfigParser

import Box

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

Box._file_update(filename)
