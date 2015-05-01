#!/usr/bin/python
from __future__ import print_function
import argparse
from pprint import pprint as pp
import Box

parser = argparse.ArgumentParser()
parser.add_argument("folder_name")
args = parser.parse_args()
folder_name = args.folder_name

folder_info = Box._folder_info(folder_name)
pp(folder_info)
