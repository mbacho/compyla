#!/usr/bin/env python

from sys import argv
from sys import exit

from fsm import FSM
from fsm import ParseException
from fsm import State
from fsm import Fxn

from lexical.lists import TokenObject
from lexical.lists import LexemObject

class FxnFSM(FSM):
  """An fsm for the language function"""
  
  def parse_lexemes(self,fname):
    fyl = open(fname,'r')
    buf = []
    for line in fyl:
      a,b,c=line.strip().split()
      buf.append(LexemObject(a,b,c))
    fyl.close()
    self.parse_string(buf)
  

def fxn_lang_load(fsm):
    #the states
    a=State('A'); b=State('B'); c=State('C'); d=State('D'); e=State('E')
    f=State('F'); g=State('G'); h=State('H'); i=State('I'); j=State('J')
    k=State('K'); l=State('L'); m=State('M'); n=State('N'); o=State('O')
    p=State('P'); q=State('Q'); r=State('R'); s=State('S'); t=State('T')
    u=State('U'); v=State('V'); w=State('W', True); x=State('X'); y=State('Y')
    z=State('Z'); a2=State('A2'); b2=State('B2'); 
    c2=State('C2'); d2=State('D2'); e2=State('E2'); f2=State('F2')

    #transition functions
    a.add_fxn('idtok',b)
    b.add_fxn('Lparen',c)
    c.add_fxn('idtok',d)
    c.add_fxn('rparen',f)
    d.add_fxn('commatok',e)
    d.add_fxn('rparen',f)
    e.add_fxn('idtok',d)
    f.add_fxn('lbrace',g)
    g.add_fxn('iftok',h)
    g.add_fxn('rbrace',w)
    h.add_fxn('Lparen',i)
    i.add_fxn('idtok',j)
    i.add_fxn('numtok',j)
    i.add_fxn('strtok',j)
    j.add_fxn('equalsTok',k)
    j.add_fxn('gtTok',k)
    j.add_fxn('ltTok',k)
    j.add_fxn('grTok',k)
    j.add_fxn('leTok',k)
    k.add_fxn('idtok',l)
    k.add_fxn('strtok',l)
    k.add_fxn('numtok',l)
    l.add_fxn('rparen',m)
    m.add_fxn('thentok',n)
    n.add_fxn('lbrace',o)
    o.add_fxn('idtok',p)
    p.add_fxn('assigntok',q)
    q.add_fxn('idtok',r)
    q.add_fxn('numtok',r)
    q.add_fxn('strtok',r)
    r.add_fxn('plustok',s)
    r.add_fxn('minustok',s)
    r.add_fxn('divtok',s)
    r.add_fxn('multtok',s)
    s.add_fxn('idtok',t)
    s.add_fxn('numtok',t)
    s.add_fxn('strtok',t)
    t.add_fxn('semictok',u)
    u.add_fxn('rbrace',v)
    u.add_fxn('idtok',p)
    v.add_fxn('rbrace',u)
    v.add_fxn('elsetok',x)
    x.add_fxn('iftok',h)
    x.add_fxn('lbrace',y)
    y.add_fxn('idtok',z)
    z.add_fxn('assigntok',a2)
    a2.add_fxn('idtok',b2)
    a2.add_fxn('strtok',b2)
    b2.add_fxn('plustok',c2)
    b2.add_fxn('minustok',c2)
    b2.add_fxn('divtok',c2)
    b2.add_fxn('multtok',c2)
    c2.add_fxn('strtok',d2)
    c2.add_fxn('idtok',d2)
    d2.add_fxn('semictok',e2)
    e2.add_fxn('idtok',z)
    e2.add_fxn('rbrace',f2)
    f2.add_fxn('rbrace',w)
    f2.add_fxn('iftok',h)
    
    fsm.set_start_state(a)

  
#if __name__=='__main__':
#  if len(argv) != 2:
#    print "usage : {0} [string]".format(argv[0])
#    exit(1)

#  f = FSM()
#  main(f)
#  try:
#    f.parse_string(argv[1])
#  except ParseException, e:
#    print "error : ",e.message
