#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import codecs
import re
import os
import subprocess

def clear_files(folder):
  """Function to clear files from a folder."""
  if os.path.exists(folder) and os.path.isdir(folder):
    for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
          os.unlink(file_path)
        elif os.path.isdir(file_path):
          shutil.rmtree(file_path)
      except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
        
def run_GA_morphGen(root_folder, morph_folder_name, morph_input_folder, morph_output_folder, count_strs_all_FORGe, show_input):
  # Call morph generator
  # v3 (fast, ~2sec/450 texts)
  clear_files(morph_output_folder)
  # To store how many texts we have in each file (used to )
  count_strs_all_Morph = []
  for filepath in sorted(glob.glob(os.path.join(morph_input_folder, '*.*'))):
    count_strs_all = 0
    head, tail = os.path.split(filepath)
    filename_out = tail.rsplit('.')[0]
    print('Processing '+filename_out)
    fo = codecs.open(morph_output_folder+'/'+filename_out+'_out.txt', 'w', 'utf-8')
    # Next line: how it can work if the code is used directly on Colab
    # list_inflected_words = ! cat {filepath} | {morph_folder_name}'/flookup' -a {morph_folder_name}'/allgen.fst'
    # Next lines: module version of the line above; it returns bytes instead of strings, and additional linebreak delimiters
    list_inflected_words_raw = subprocess.Popen("cat "+filepath+" | "+morph_folder_name+"'/flookup' -a "+morph_folder_name+"'/allgen.fst'", shell=True, stdout=subprocess.PIPE).stdout.readlines()
    # I changed the way to make the shell call above, hence I received a different output; I'm not a mathematician but with the next line I reduce to problem to one that was already solved.
    list_inflected_words = [str(raw_word, encoding='utf-8').replace('\n', '') for raw_word in list_inflected_words_raw]
    # print(list_inflected_words)

    # Create a variable to store the outputs
    text = ''
    # morph returns this as list_inflected_words: ['imir+Verb+Vow+PresInd\timríonn', '', 'Agremiação_Sportiva_Arapiraquense+Noun+Masc+Com+Pl\t+?', '', ',\t+?',...]
    for word in list_inflected_words:
      empty = 'yes'
      input_string = ''
      morph_returned = ''
      morph_backup = ''
      if re.search('\t', word):
        # for every space an empty string is returned; we'll ignore them later. Between two consecutive texts there is a simple "\t" with nothing around. I use this to introduce linebreaks later.
        empty = 'no'
        input_string = word.split('\t')[0]
        morph_returned = word.split('\t')[1]
        if re.search('\+', word):
          morph_backup = input_string.split('+', 1)[0]
        else:
          morph_backup = input_string
      out_line = ''
      # Create each output line with the required contents
      if show_input == True:
        if empty == 'no':
          if morph_returned == '':
            if input_string == '':
              out_line = out_line + '\n'
              count_strs_all += 1
          else:
            out_line = out_line + input_string + ': ' +'\x1b[5;30;47m'+morph_returned+'\x1b[0m'+'\n'
      else:
        if empty == 'no':
          if morph_returned == '+?':
            out_line = out_line + morph_backup + ' '
          # If the line is empty, add a line break (empty lines separate different texts in the input)
          elif morph_returned == '':
            if input_string == '':
              out_line = out_line + '\n'
              count_strs_all += 1
          else:
            out_line = out_line + morph_returned + ' '
      # add line to the other lines of the same file
      text = text + out_line

    # print('\n----------------------\n'+text+'\n')
    count_strs_all_Morph.append(count_strs_all)
    fo.write(text+'\n')
    fo.close()

  # Check
  with codecs.open(os.path.join(root_folder, 'FORGe', 'log', 'summary.txt'), 'a', 'utf-8') as fo:
    fo.write('\nMorphology debug\n==================\n\n')
    if not sum(count_strs_all_Morph) == count_strs_all_FORGe:
      print('\nERROR! Mismatch with FORGe outputs!')
      fo.write('ERROR! Mismatch with FORGe outputs!\n')
    print('\nThere are '+str(sum(count_strs_all_Morph))+' texts.')
    fo.write('There are '+str(sum(count_strs_all_Morph))+' texts.\n')
    print('Texts per file: '+str(count_strs_all_Morph))
    fo.write('Texts per file: '+str(count_strs_all_Morph)+'\n')
    fo.write('---------------------------------\n')
  clear_files(morph_input_folder)
