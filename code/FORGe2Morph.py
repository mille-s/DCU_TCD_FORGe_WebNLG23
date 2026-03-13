#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import codecs
import re
import os
import sys

language = sys.argv[1]
temp_input_folder_morph = sys.argv[2]
morph_input_folder = sys.argv[3]

def process_FORGe(filepath, count_strs_all):
  filename = filepath.rsplit('/', 1)[1]
  print('Processing '+filename)
  lines = codecs.open(filepath, 'r', 'utf-8').readlines()
  fo = codecs.open(os.path.join(morph_input_folder, filename), 'w', 'utf-8')
  for line in lines:
    # Replace apostrophes/parentheses by something else, they make morph break
    line = re.subn(r"'", r'_APSTR_', line)[0]
    line = re.subn(r"\(", r'_OBRKT_', line)[0]
    line = re.subn(r"\)", r'_CBRKT_', line)[0]
    line = re.subn(r"&", r'_AMPRS_', line)[0]
    line = re.subn(r";", r'_SEMICOL_', line)[0]
    line = re.subn(r"\$", r'_DOLLSIGN_', line)[0]
    # The next line was not activated for the WebNLG submission
    # line = re.subn(r"\+", r'_PLUSSIGN_', line)[0]
    line = re.subn(r'\"', r'_DBLQUOT_', line)[0]
    # clean quotes that MATE can’t take care of
    line = re.subn(r'\\\\"([^\\\\]+)\\\\', r'\\"\g<1>\\"', line)[0]
    # In FORGe I use % as separator, we need +
    line = re.subn(r'%', r'+', line)[0]
    # Insert linebreak after each final sentence to separate texts from each other (one text can have several sentences)
    line = re.subn(r' \.$', r' .\n', line)[0]
    # Put each word on one line
    line = re.subn(r' ', r'\n', line)[0]
    # Copy to morph gen input folder
    fo.write(line)
  fo.close()
  count_strs_all.append(len(lines))

if language == 'GA':
  # list_filepaths = glob.glob(os.path.join(folder_name, 'FORGe-out', '*conll_out.txt'))
  list_filepaths = glob.glob(os.path.join(temp_input_folder_morph, '*.txt'))

  # To store how many texts we have in each file (used to )
  count_strs_all_FORGe = []

  for filepath in sorted(list_filepaths):
    process_FORGe(filepath, count_strs_all_FORGe)

  # Check
  print('\nThere are '+str(sum(count_strs_all_FORGe))+' texts.')
  print('Texts per file: '+str(count_strs_all_FORGe))
