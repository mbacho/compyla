#!/usr/bin/env python


class Fxn(object):
  def __init__(self,token='', nxt_state=None):
    self.token = token
    self.nxt_state = nxt_state


class State(object):
  def __init__(self, name, is_final = False):
    self.name = name
    self.is_final = is_final
    self.fxns = []

  def add_fxn(self,token,state):
    self.fxns.append(Fxn(token,state))
  
  def state_for(self,token):
    for i in self.fxns:
      if i.token.lower() == token.lower():
        return i.nxt_state
    return None

  def __str__(self):
    return self.name


class ParseException(BaseException):
  pass


class FSM(object):
#  states = []
  start_state = None

#  def add_state(self,state):
#    states.append(state)
  
  def set_start_state(self, state):
    if isinstance(state,State) or isinstance(state,None):
      self.start_state = state
    else:
      raise ParseException("Invalid state provided")
      
  def parse_string(self,s):
    cur_state = self.start_state
    if cur_state is None:
      raise ParseException("No start state provided")
    
    for i in s:
      nxt_state = cur_state.state_for(i.lex_id)
      if nxt_state is None:
        raise ParseException("FSM crash on input '{0}' in state {1} in line {2}".format(i.lex_id,cur_state,i.line_no))
      cur_state = nxt_state
    if not cur_state.is_final:
      raise ParseException("FSM terminated on non-final state {0}".format(cur_state))
    print "parse ok"

  def load_fsm(fname):
    """
    Loads an fsm from a text file
    
    The file is structured as follows
    
    #states
    state_one_name
    state_two_name
    #fxns
    state_one_name, token, state_two_name
    state_two_name, token, state_two_name
    """
    
    pass
    
