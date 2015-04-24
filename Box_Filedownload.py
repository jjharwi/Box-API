#!/usr/bin/python

import argparse

import Box_File

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename
Box_File._file_download(filename)
