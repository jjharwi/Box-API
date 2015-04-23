#!/usr/bin/python

import Box_File
import argparse
from ConfigParser import SafeConfigParser

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

file_info = Box_File._file_download(filename)
