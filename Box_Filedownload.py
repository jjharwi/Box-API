#!/usr/bin/python

import Box_File
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename
Box_File._file_download(filename)
