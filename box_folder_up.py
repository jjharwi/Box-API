#!/usr/bin/env python

import os
import argparse
import Box

parser = argparse.ArgumentParser()
parser.add_argument("folder_name")
args = parser.parse_args()
folder_name = args.folder_name

for file in os.listdir(folder_name):
    filename = folder_name + '/' + file
    Box._file_update(filename)
    os.remove(filename)
