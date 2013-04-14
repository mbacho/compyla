#!/usr/bin/env python


from fsm import Pda
from fsm import ParseException
from fsm import State
from fsm import Fxn

import lexical.lists as ls


class FxnPda(Pda):
    """An fsm for the language function"""

    def parse_lexemes(self, fname):
        fyl = open(fname, 'r')
        buf = []
        for line in fyl:
            a, b, c = line.strip().split()
            buf.append(ls.LexemObject(a, b, c))
        fyl.close()
        self.parse_string(buf)


def fxn_lang_load(pda):
#the states
    a = State('A')

    #transition functions
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='Function',
                  replacements=(a, ['idtok', 'lparen', 'rparen', 'lbrace', 'Statement', 'rbrace'])))
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='Statement', replacements=(a, ['Condition', 'True', 'False'])))

    a.add_fxn(Fxn(token='iftok', tos='Condition',
                  replacements=(a, ['iftok', 'lparen', 'ConditionExpr', 'rparen', 'thentok'])))

    a.add_fxn(Fxn(token='lbrace', tos='True', replacements=(a, ['lbrace', 'AssignmentStmt', 'rbrace'])))

    a.add_fxn(Fxn(token='elsetok', tos='False', replacements=(a, ['elsetok','False'])))
    a.add_fxn(Fxn(token='lbrace', tos='False', replacements=(a, ['lbrace', 'AssignmentStmt', 'rbrace'])))
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='False', replacements=(a, [])))

    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='ConditionExpr',
                  replacements=(a, ['Exprtok', 'Lop', 'Exprtok'])))
    a.add_fxn(Fxn(token='idtok', tos='Exprtok', replacements=(a, ['idtok'])))
    a.add_fxn(Fxn(token='strtok', tos='Exprtok', replacements=(a, ['strtok'])))
    a.add_fxn(Fxn(token='chrtok', tos='Exprtok', replacements=(a, ['chrtok'])))
    a.add_fxn(Fxn(token='numtok', tos='Exprtok', replacements=(a, ['numtok'])))
    a.add_fxn(Fxn(token='idtok', tos='AssignmentStmt',
                  replacements=(a, ['idtok', 'assigntok', 'Expr', 'semictok'])))

    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='AssignmentStmt', replacements=(a, ['idtok','Exprtok','Aop','Exprtok'])))

    a.add_fxn(Fxn(token='plustok', tos='Aop', replacements=(a, ['plustok'])))
    a.add_fxn(Fxn(token='minustok', tos='Aop', replacements=(a, ['minustok'])))
    a.add_fxn(Fxn(token='multtok', tos='Aop', replacements=(a, ['multtok'])))
    a.add_fxn(Fxn(token='divtok', tos='Aop', replacements=(a, ['divtok'])))
    a.add_fxn(Fxn(token='modtok', tos='Aop', replacements=(a, ['modtok'])))

    a.add_fxn(Fxn(token='equalstok', tos='Lop', replacements=(a, ['equalstok'])))
    a.add_fxn(Fxn(token='lttok', tos='Lop', replacements=(a, ['lttok'])))
    a.add_fxn(Fxn(token='letok', tos='Lop', replacements=(a, ['letok'])))
    a.add_fxn(Fxn(token='gttok', tos='Lop', replacements=(a, ['gttok'])))
    a.add_fxn(Fxn(token='getok', tos='Lop', replacements=(a, ['getok'])))
    a.add_fxn(Fxn(token='netok', tos='Lop', replacements=(a, ['netok'])))

    a.add_fxn(Fxn(token='idtok', tos='Expr', replacements=(a, ['idtok','Aop','idtok'])))
    #a.add_fxn(Fxn(token='idtok', tos='Expr', replacements=(a, ['idtok','Aop','exprtok'])))
    #a.add_fxn(Fxn(token='strtok', tos='Expr', replacements=(a, ['strtok','Aop','exprtok'])))
    #a.add_fxn(Fxn(token='chrtok', tos='Expr', replacements=(a, ['chrtok','Aop','exprtok'])))
    #a.add_fxn(Fxn(token='numtok', tos='Expr', replacements=(a, ['numtok','Aop','exprtok'])))
    a.add_fxn(Fxn(token='lparen', tos='Expr', replacements=(a, ['lparen', 'Expr', 'rparen'])))

    #a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='Expr', replacements=(a, ['Expr'])))
    a.add_fxn(Fxn(token='assigntok', tos='Aop', replacements=(a, ['assigntok'])))
    a.add_fxn(Fxn(token='minustok', tos='Aop', replacements=(a, ['minustok'])))
    a.add_fxn(Fxn(token='modtok', tos='Aop', replacements=(a, ['modtok'])))
    a.add_fxn(Fxn(token='divtok', tos='Aop', replacements=(a, ['divtok'])))
    a.add_fxn(Fxn(token='multtok', tos='Aop', replacements=(a, ['multtok'])))
    a.add_fxn(Fxn(token='chrtok', tos='chrtok', replacements=(a, ['chrtok'])))

    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='Floattok', replacements=(a, ['numtok', 'periodtok', 'numtok'])))
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='periodtok', replacements=(a, ['periodtok', 'numtok'])))

    a.add_fxn(Fxn(token='idtok', tos='idtok', replacements=(a, [])))
    a.add_fxn(Fxn(token='iftok', tos='iftok', replacements=(a, [])))
    a.add_fxn(Fxn(token='lparen', tos='lparen', replacements=(a, [])))
    a.add_fxn(Fxn(token='rparen', tos='rparen', replacements=(a, [])))
    a.add_fxn(Fxn(token='equalstok', tos='equalstok', replacements=(a, [])))
    a.add_fxn(Fxn(token='gttok', tos='gttok', replacements=(a, [])))
    a.add_fxn(Fxn(token='lttok', tos='lttok', replacements=(a, [])))
    a.add_fxn(Fxn(token='thentok', tos='thentok', replacements=(a, [])))
    a.add_fxn(Fxn(token='lbrace', tos='lbrace', replacements=(a, [])))
    a.add_fxn(Fxn(token='rbrace', tos='rbrace', replacements=(a, [])))
    a.add_fxn(Fxn(token='semictok', tos='semictok', replacements=(a, [])))
    a.add_fxn(Fxn(token='assigntok', tos='assigntok', replacements=(a, [])))
    a.add_fxn(Fxn(token='elsetok', tos='elsetok', replacements=(a, [])))
    a.add_fxn(Fxn(token='plustok', tos='plustok', replacements=(a, [])))
    a.add_fxn(Fxn(token='minustok', tos='minustok', replacements=(a, [])))
    a.add_fxn(Fxn(token='multtok', tos='multtok', replacements=(a, [])))
    a.add_fxn(Fxn(token='divtok', tos='divtok', replacements=(a, [])))
    a.add_fxn(Fxn(token='grtok', tos='grtok', replacements=(a, [])))
    a.add_fxn(Fxn(token='letok', tos='letok', replacements=(a, [])))
    a.add_fxn(Fxn(token='pipetok', tos='pipetok', replacements=(a, [])))
    a.add_fxn(Fxn(token='periodtok', tos='periodtok', replacements=(a, [])))
    a.add_fxn(Fxn(token='commatok', tos='commatok', replacements=(a, [])))
    a.add_fxn(Fxn(token='netok', tos='netok', replacements=(a, [])))
    a.add_fxn(Fxn(token='modtok', tos='modtok', replacements=(a, [])))
    a.add_fxn(Fxn(token='strtok', tos='strtok', replacements=(a, [])))
    a.add_fxn(Fxn(token='chrtok', tos='chrtok', replacements=(a, [])))
    a.add_fxn(Fxn(token='numtok', tos='numtok', replacements=(a, [])))

    pda.set_start_state(a)


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
