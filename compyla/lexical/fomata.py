#!/usr/bin/env python

"""Source code formatter for the language function"""
from os.path import exists
from os.path import split
from os.path import join
from os import remove
from os import rename
from os import chdir
from os import mkdir

from shutil import copy2

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
  """  
  MACROS   = {}#key - value dictionary
  PRE_FOLDER = 'pre/' #preformatted code stored here
  CUR_LINE = None
  IN_BLOCK_COMM = False
  
  def include(self, line, base_dir,f_obj):
    """Process included file then insert file's contents"""
    name = line.strip().split('<')
    if len(name) != 2:
      raise PreProcException("Invalid include in line {0}".format(self.CUR_LINE))
    inc, nm = name
    inc = inc.strip()
    nm = nm.strip()
    if inc!='#include':
      raise PreProcException("Invalid include in line {0}".format(self.CUR_LINE))
      
    pos = nm.find('>')
    if pos < 0:
      raise PreProcException("Invalid include in line {0}".format(self.CUR_LINE))
    extra = nm[pos+1:]
    extra = extra.strip()
    if extra !='':
      inline = extra.startswith('//')
      multiline = extra.startswith('/*')
      if (not inline) and (not multiline):
        raise PreProcException("Invalid tokens '{1}' after include in line {0} {2},{3}".format(self.CUR_LINE,extra,inline,multiline))
      if multiline:
        self.IN_BLOCK_COMM = True
        
    nm = nm[:pos]
    fullnm = join(base_dir,nm)
    if not exists(fullnm):
      raise PreProcException("Include file not found. Line {0}".format(self.CUR_LINE))
    
    copy2(fullnm,'.')
    frmt = PreProcessor()
    fname = frmt.format_file(nm,base_dir)
    f = open(fname,'r')
    for i in f:
      f_obj.write(i)
    f_obj.write('\n')
    f.close()
    
    
  def define(self,line):
    """
    Process macros in source.
    If a macros exists it's not replaced
    """
    define = line[len('#define'):].strip()
    
    ind = define.find(" ")
    if ind == -1:
      raise PreProcException("Invalid macros definition. Line {0}".format(self.CUR_LINE))
    key = define[:ind].strip()
    val = define[ind+1:].strip()
    if len(val) < 1:
      raise PreProcException("Invalid macros definition. Line {0}".format(self.CUR_LINE))
    if not key in self.MACROS:
      self.MACROS[key]=val
  
  
  def macros(self,line,fobj):  
    vals = line.strip().split()
    key = vals[0][1:]
    #TODO check whether there are values
    if key not in self.MACROS:
      raise PreProcException("Undefined macros '{1}. Line {0}".format(self.CUR_LINE,key))
    fobj.write(self.MACROS[key])
    fobj.write('\n')
    
    
  def format_file(self, name, base_dir, use_cwd = True):
    if not use_cwd:
      chdir(base_dir)
    #if not exists(self.PRE_FOLDER):
    #  mkdir(self.PRE_FOLDER)
    
    src = open(name, 'r+')
    lines = src.readlines() #potential memory hogger
    #chdir(self.PRE_FOLDER)
    des = open(name+'.src','w+')
    self.IN_BLOCK_COMM = False
    self.CUR_LINE = 0
    for line in lines:
      self.CUR_LINE += 1
      if self.IN_BLOCK_COMM:
        pos =  line.find('*/')
        if pos > -1:          
          des.write(line[pos+2:])
          self.IN_BLOCK_COMM = False
        continue
     
      if line.startswith('#include'):
        self.include(line,base_dir,des)
        continue

      if line.startswith('#define'):
        self.define(line)
        continue
        
      if line.startswith('#'):
        self.macros(line,des)
        continue
        
      pos = line.find('//')
      if pos > -1:
        des.write(line[:pos])
        des.write('\n')
        continue
        
      pos = line.find('/*')
      if pos > -1:
        des.write(line[:pos])
        des.write('\n')
        self.IN_BLOCK_COMM = True
        continue
      
      des.write(line)
      
    src.close()
    des.close()
    #if exists(name): remove(name)    
    #rename(des.name,name)
    return des.name
    
