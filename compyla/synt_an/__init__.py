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
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos=None, replacements=(a, ['Function'])))
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='Function', replacements=(a, ['idtok', 'lparen', 'rparen', 'lbrace', 'Statement', 'rbrace'])))
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='Statement', replacements=(a, ['Condition', 'True', 'False'])))

    a.add_fxn(Fxn(token='iftok', tos='Condition', replacements=(a, ['iftok', 'lparen', 'ConditionExpr', 'rparen', 'thentok'])))

    a.add_fxn(Fxn(token='lbrace', tos='True', replacements=(a, ['lbrace', 'AssignmentStmt', 'rbrace'])))

    a.add_fxn(Fxn(token='elsetok', tos='False', replacements=(a, ['elsetok','False'])))
    a.add_fxn(Fxn(token='lbrace', tos='False', replacements=(a, ['lbrace', 'AssignmentStmt', 'rbrace'])))
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='False', replacements=(a, [])))

    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='ConditionExpr', replacements=(a, ['Exprtok', 'Lop', 'Exprtok'])))
    a.add_fxn(Fxn(token='idtok', tos='Exprtok', replacements=(a, ['idtok'])))
    a.add_fxn(Fxn(token='strtok', tos='Exprtok', replacements=(a, ['strtok'])))
    a.add_fxn(Fxn(token='chrtok', tos='Exprtok', replacements=(a, ['chrtok'])))
    a.add_fxn(Fxn(token='numtok', tos='Exprtok', replacements=(a, ['numtok'])))
    a.add_fxn(Fxn(token='floattok', tos='Exprtok', replacements=(a, ['floattok'])))
    a.add_fxn(Fxn(token='idtok', tos='AssignmentStmt', replacements=(a, ['idtok', 'assigntok', 'Expr', 'semictok'])))

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

    #a.add_fxn(Fxn(token='idtok', tos='Expr', replacements=(a, ['idtok','Aop','idtok'])))
    a.add_fxn(Fxn(token='idtok', tos='Expr', replacements=(a, ['idtok','Aop','exprtok'])))
    a.add_fxn(Fxn(token='floattok', tos='Expr', replacements=(a, ['floattok','Aop','exprtok'])))
    a.add_fxn(Fxn(token='strtok', tos='Expr', replacements=(a, ['strtok','Aop','exprtok'])))
    a.add_fxn(Fxn(token='chrtok', tos='Expr', replacements=(a, ['chrtok','Aop','exprtok'])))
    a.add_fxn(Fxn(token='numtok', tos='Expr', replacements=(a, ['numtok','Aop','exprtok'])))
    a.add_fxn(Fxn(token='lparen', tos='Expr', replacements=(a, ['lparen', 'Expr', 'rparen'])))

    #a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='Expr', replacements=(a, ['Expr'])))
    a.add_fxn(Fxn(token='assigntok', tos='Aop', replacements=(a, ['assigntok'])))
    a.add_fxn(Fxn(token='minustok', tos='Aop', replacements=(a, ['minustok'])))
    a.add_fxn(Fxn(token='modtok', tos='Aop', replacements=(a, ['modtok'])))
    a.add_fxn(Fxn(token='divtok', tos='Aop', replacements=(a, ['divtok'])))
    a.add_fxn(Fxn(token='multtok', tos='Aop', replacements=(a, ['multtok'])))
    a.add_fxn(Fxn(token='chrtok', tos='chrtok', replacements=(a, [])))

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
    a.add_fxn(Fxn(token='floattok', tos='floattok', replacements=(a, [])))
    pda.set_start_state(a)

    
def load_simple(pda):
    #the states
    a = State('A')
    #transition functions
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos=None, replacements=(a, ['FXN'])))
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='FXN', replacements=(a, ['idtok', 'lparen', 'rparen', 'lbrace', 'STMT', 'rbrace'])))
    
    a.add_fxn(Fxn(token='iftok', tos='STMT', replacements=(a, ['iftok','lparen','COND','rparen', 'thentok','TRUE', 'FALSE_EXPR'])))
    
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='COND', replacements=(a, ['LO_EXPR', 'LOP', 'LO_EXPR'])))
    a.add_fxn(Fxn(token='lparen', tos='COND', replacements=(a, ['lparen', 'COND', 'rparen'])))
    a.add_fxn(Fxn(token='lbrace', tos='TRUE', replacements=(a, ['lbrace','ASS_STMT','rbrace'])))
    a.add_fxn(Fxn(token='elsetok', tos='FALSE_EXPR', replacements=(a, ['elsetok','FALSE'])))
    a.add_fxn(Fxn(token=Fxn.ANY_INPT, tos='FALSE_EXPR', replacements=(a, [])))
    a.add_fxn(Fxn(token='iftok', tos='FALSE', replacements=(a, ['iftok','lparen','COND','rparen','thentok','TRUE','FALSE_EXPR'])))
    a.add_fxn(Fxn(token='lbrace', tos='FALSE', replacements=(a, ['lbrace','ASS_STMT','rbrace'])))
    a.add_fxn(Fxn(token='idtok', tos='ASS_STMT', replacements=(a, ['idtok','assigntok','A_EXPR','AOP','A_EXPR','semictok'])))
    
    a.add_fxn(Fxn(token='idtok', tos='LO_EXPR', replacements=(a, ['idtok'])))
    a.add_fxn(Fxn(token='strtok', tos='LO_EXPR', replacements=(a, ['strtok'])))
    a.add_fxn(Fxn(token='chrtok', tos='LO_EXPR', replacements=(a, ['chrtok'])))
    a.add_fxn(Fxn(token='numtok', tos='LO_EXPR', replacements=(a, ['numtok'])))
    a.add_fxn(Fxn(token='floattok', tos='LO_EXPR', replacements=(a, ['floattok'])))
    a.add_fxn(Fxn(token='lparen', tos='LO_EXPR', replacements=(a, ['lparen','LO_EXPR','LOP','LO_EXPR','rparen'])))
    
    a.add_fxn(Fxn(token='idtok', tos='A_EXPR', replacements=(a, ['idtok'])))
    a.add_fxn(Fxn(token='strtok', tos='A_EXPR', replacements=(a, ['strtok'])))
    a.add_fxn(Fxn(token='chrtok', tos='A_EXPR', replacements=(a, ['chrtok'])))
    a.add_fxn(Fxn(token='numtok', tos='A_EXPR', replacements=(a, ['numtok'])))
    a.add_fxn(Fxn(token='floattok', tos='A_EXPR', replacements=(a, ['floattok'])))
    a.add_fxn(Fxn(token='lparen', tos='A_EXPR', replacements=(a, ['lparen','A_EXPR','AOP','A_EXPR','rparen'])))
    
    a.add_fxn(Fxn(token='equalstok', tos='LOP', replacements=(a, ['equalstok'])))
    a.add_fxn(Fxn(token='lttok', tos='LOP', replacements=(a, ['lttok'])))
    a.add_fxn(Fxn(token='letok', tos='LOP', replacements=(a, ['letok'])))
    a.add_fxn(Fxn(token='gttok', tos='LOP', replacements=(a, ['gttok'])))
    a.add_fxn(Fxn(token='getok', tos='LOP', replacements=(a, ['getok'])))
    a.add_fxn(Fxn(token='netok', tos='LOP', replacements=(a, ['netok'])))
    
    a.add_fxn(Fxn(token='minustok', tos='AOP', replacements=(a, ['minustok'])))
    a.add_fxn(Fxn(token='plustok', tos='AOP', replacements=(a, ['plustok'])))
    a.add_fxn(Fxn(token='modtok', tos='AOP', replacements=(a, ['modtok'])))
    a.add_fxn(Fxn(token='divtok', tos='AOP', replacements=(a, ['divtok'])))
    a.add_fxn(Fxn(token='multtok', tos='AOP', replacements=(a, ['multtok'])))
    
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
    a.add_fxn(Fxn(token='floattok', tos='floattok', replacements=(a, [])))
    a.add_fxn(Fxn(token='idtok', tos='idtok', replacements=(a, [])))
    
    pda.set_start_state(a)