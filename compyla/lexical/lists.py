#!/usr/bin/python

class LexemObject(object):  
  def __init__(self,lex_id,lex_code, line_no=None):
    self.lex_id   = lex_id
    self.lex_code = lex_code
    self.line_no = line_no
    
  def __repr__(self):
    return self.lex_id
    
class TokenObject(object):  
  def __init__(self,token_id, token_lex, token_code):
    self.token_code = token_code
    self.token_id   = token_id
    self.token_lex  = token_lex
  
  def __repr__(self):
    return self.token_id
