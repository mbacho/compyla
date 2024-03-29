#!/usr/bin/env python

"""A compiler for the language function"""

from os.path import exists
from os.path import split
from os.path import realpath
from os.path import isabs
from os import getcwd
from os import mkdir
from os import chdir
from shutil import copy2

from sys import exit
from sys import argv

from lexical import lex_analyser as lex
from lexical.fomata import PreProcessor
from synt_an import FxnFSM
from synt_an import fxn_lang_load

DEBUG_FOLDER = "debug/"


def enter_debug(fpath):
  """enter debug folder for the source file"""
  print "entering debug folder : chdir'ing to {0}".format(DEBUG_FOLDER)
  dir,name = split(fpath)
  chdir(dir)
  if not exists(DEBUG_FOLDER):
    mkdir(DEBUG_FOLDER)
  
  copy2(fpath, DEBUG_FOLDER)
  chdir(DEBUG_FOLDER)
  return name
 
 
def main(fpath):
  """Needs the file's absolute path"""
  if not isabs(fpath):
    print "',",fpath, "' is not an absolute file path"
    exit(1)
  fname = enter_debug(fpath)
  
  print "formating src..."
  pre = PreProcessor()
  a,b=split(fpath)
  src_fyl = pre.format_file(b,a)
  print "Done..."
  
  #print "Lexical analysis"
  #la = lex.LexAnalyser()
  #output = la.analyse(src_fyl)
  #if not output:
  #  print "lexial error"
  #  exit(1)
    
  #print "Parsing..."
  #fsm = FxnFSM()
  #fxn_lang_load(fsm)
  #fsm.parse_lexemes(output[0])
  


def usage():
  print "usage\n\t{0} [source_file]"  .format(argv[0])


if __name__=='__main__':
  if len(argv) != 2:
    usage()
    exit(1)

  if not exists(argv[1]):
    print '\n\tHiyo file iko MIA. Ebu isake.'
    exit(1)

  main(realpath(argv[1]))
  
