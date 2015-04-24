#!/usr/bin/python

import argparse

import Box

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename
Box._file_download(filename)
