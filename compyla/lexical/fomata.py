#!/usr/bin/env python

"""Source code formatter for the language function"""
from os.path import exists
from os.path import split
from os.path import join
from os import remove
from os import rename
from os import chdir
from os import mkdir
from re import findall
from re import IGNORECASE
from shutil import copy2


#TODO multiline comment on single line
#TODO inline macros expansion 

class PreProcException (BaseException):
  pass
  
class PreProcessor(object):
  """
    Does pre-processor formatting
    Formats the following directives : 
      #include<filename>
      #define KEY VAL
    Remove comments denoted by : 
       //....\n or /*  ... */
    Replace hexadecimal numbers with integers   
  """  
  MACROS   = {}#key - value dictionary
  PRE_FOLDER = 'pre/' #preformatted code stored here
  CUR_LINE = None
  CUR_SRC = None
  IN_BLOCK_COMM = False
  
  def hex_to_dec(self,line):
    ln = line
    hx = findall(r'(0x\d+)',ln,IGNORECASE)
    for i in hx:
      s = str(int(i,16))
      ln = ln.replace(i,s)
    return ln 
    
  def include(self, line, base_dir):
    """Process included file then return formated filename"""
    name = line.strip().split('<')
    if len(name) != 2:
      raise PreProcException("Invalid include in line {0} in {1}".format(self.CUR_LINE,self.CUR_SRC))
    inc, nm = name
    inc = inc.strip()
    nm = nm.strip()
    if inc!='#include':
      raise PreProcException("Invalid include in line {0} in {1}".format(self.CUR_LINE,self.CUR_SRC))
      
    pos = nm.find('>')
    if pos < 0:
      raise PreProcException("Invalid include in line {0} in {1}".format(self.CUR_LINE,self.CUR_SRC))
    extra = nm[pos+1:]
    extra = extra.strip()
    if extra !='':
      inline = extra.startswith('//')
      multiline = extra.startswith('/*')
      if (not inline) and (not multiline):
        raise PreProcException("Invalid tokens '{1}' after include in line {0} {2},{3} in {4}".format(self.CUR_LINE,extra,inline,multiline,self.CUR_SRC))
      if multiline:
        self.IN_BLOCK_COMM = True
        
    nm = nm[:pos]
    fullnm = join(base_dir,nm)
    if not exists(fullnm):
      raise PreProcException("Include file not found. Line {0} in {1}".format(self.CUR_LINE,self.CUR_SRC))
    
    copy2(fullnm,'.')
    frmt = PreProcessor()
    fname = frmt.format_file(nm,base_dir)
    return fname
        
  def define(self,line):
    """
    Process macros in source.
    If a macros exists it's not replaced
    """
    define = line[len('#define'):].strip()
    
    ind = define.find(" ")
    if ind == -1:
      raise PreProcException("Invalid macros definition. Line {0} in {1}".format(self.CUR_LINE,self.CUR_SRC))
    key = define[:ind].strip()
    val = define[ind+1:].strip()
    if len(val) < 1:
      raise PreProcException("Invalid macros definition. Line {0} in {1}".format(self.CUR_LINE,self.CUR_SRC))
    if not key in self.MACROS:
      self.MACROS[key]=val  
  
  def macros(self,line):  
    vals = line.strip().split()
    key = vals[0][1:]
    #TODO check whether there are values
    if key not in self.MACROS:    
      raise PreProcException("Undefined macros '{0}' in Line {1} in {2}".format(key,self.CUR_LINE,self.CUR_SRC))
    return self.MACROS[key]
    
  def format_file(self, name, base_dir, use_cwd = True):
    if not use_cwd:
      chdir(base_dir)
      
    src = open(name, 'r+')
    self.CUR_SRC = name
    lines = src.readlines() #potential memory hogger

    des = open(name+'.src','w+')
    self.IN_BLOCK_COMM = False
    self.CUR_LINE = 0
    for line in lines:
      self.CUR_LINE += 1
      line = line.strip()
      write_line = ''
      pos = line.find('/*')
      if pos > -1:
        line = line[:pos]
        self.IN_BLOCK_COMM = True
          
      if self.IN_BLOCK_COMM:
        pos =  line.find('*/')
        if pos > -1:          
          line = line[pos+2:]
          self.IN_BLOCK_COMM = False
        else:
          continue
      
      pos = line.find('//')
      if pos > -1:
        line = line[:pos]

      if line.startswith('#include'):
        fname = self.include(line,base_dir)
        f = open(fname,'r')
        for i in f:
          des.write(i)
        des.write('\n')
        f.close()
        continue
      elif line.startswith('#define'):
        self.define(line)
        continue
      elif line.startswith('#'):
        write_line = self.macros(line)
      
      if write_line == '':
        write_line = line
      if write_line != '':
        write_line = self.hex_to_dec(write_line)
        des.write(write_line)
        des.write('\n')
      
    src.close()
    des.close()
    #if exists(name): remove(name)    
    #rename(des.name,name)
    return des.name
    
