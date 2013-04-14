#!/usr/bin/python

"""Lexical analyser for the language function"""

from lists import TokenObject
from lists import LexemObject


class LexAnalyser(object):
    READING_WORD = False
    READING_SPEC = False
    READING_NUM = False
    READING_FLT = False
    READING_STR = False
    READING_CHR = False

    CUR_LINE_NO = None

    CHAR_TYPE_UNKNOWN = -1
    CHAR_TYPE_ALPHA = 1
    CHAR_TYPE_SPEC = 2
    CHAR_TYPE_SPEC_FOLLOW = 3
    CHAR_TYPE_WHITE_SPACE = 4
    CHAR_TYPE_NUMBER = 5
    CHAR_TYPE_QUOTE = 6

    #recognize signed integers
    #TODO find out why spaces are needed btn operators 
    # e.g. a=b+c 
    #      gives id id plus id omitting the assign
    #     a = b + c
    #      gives id assign id plus id
    #
    
    LEXEME_LIST = []  #list of lexemes
    SYMBOL_TABLE = [
        TokenObject(token_code=1001, token_id='ifTok', token_lex='if'),
        TokenObject(token_code=1002, token_id='Lparen', token_lex='('),
        TokenObject(token_code=1003, token_id='Rparen', token_lex=')'),
        TokenObject(token_code=1004, token_id='equalsTok', token_lex='=='),
        TokenObject(token_code=1005, token_id='gtTok', token_lex='>'),
        TokenObject(token_code=1006, token_id='ltTok', token_lex='<'),
        TokenObject(token_code=1007, token_id='lBrace', token_lex='{'),
        TokenObject(token_code=1008, token_id='rBrace', token_lex='}'),
        TokenObject(token_code=1009, token_id='semicTok', token_lex=';'),
        TokenObject(token_code=1010, token_id='assignTok', token_lex='='),
        TokenObject(token_code=1011, token_id='elseTok', token_lex='else'),
        TokenObject(token_code=1012, token_id='plusTok', token_lex='+'),
        TokenObject(token_code=1013, token_id='minusTok', token_lex='-'),
        TokenObject(token_code=1014, token_id='multTok', token_lex='*'),
        TokenObject(token_code=1015, token_id='divTok', token_lex='/'),
        TokenObject(token_code=1016, token_id='grTok', token_lex='>='),
        TokenObject(token_code=1017, token_id='leTok', token_lex='<='),
        TokenObject(token_code=1018, token_id='pipeTok', token_lex='|'),
        TokenObject(token_code=1019, token_id='periodTok', token_lex='.'),
        TokenObject(token_code=1020, token_id='commaTok', token_lex=','),
        TokenObject(token_code=1021, token_id='neTok', token_lex='!='),
        TokenObject(token_code=1022, token_id='modTok', token_lex='%'),
    ] #list of tokens

    ALPHAS = ['_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
              'u', 'v', 'w', 'x', 'y', 'z']
    SPECS = ['+', '-', '*', '/', '(', ')', '}', '{', ';', '.', '%']
    SPEC_FOLLOW = ['=', '!', '<', '>'] #cater for '==','<=','>=','!='
    WHITE_SPACE = [' ', '\n', '\t']
    NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    QUOTES = ['"', '\'']

    def char_type(self, c):
        #check in symbols
        if c in self.ALPHAS:
            return self.CHAR_TYPE_ALPHA
        elif c in self.SPEC_FOLLOW:
            return self.CHAR_TYPE_SPEC_FOLLOW
        elif c in self.SPECS:
            return self.CHAR_TYPE_SPEC
        elif c in self.WHITE_SPACE:
            return self.CHAR_TYPE_WHITE_SPACE
        elif c in self.NUMBERS:
            return self.CHAR_TYPE_NUMBER
        elif c in self.QUOTES:
            return self.CHAR_TYPE_QUOTE
        else:
            return self.CHAR_TYPE_UNKNOWN

    def append_token(self, token):
        """token add to lexemes list"""
        self.LEXEME_LIST.append(LexemObject(lex_id=token.token_id, lex_code=token.token_code, line_no=self.CUR_LINE_NO))

    def process_inpt(self, inpt, name=None):
        """check symbols table get token object or append if not present"""
        found = None
        for i in self.SYMBOL_TABLE:
            if i.token_lex == inpt:
              if (name is None):
                found = i
                break
              elif i.token_id == name or name == 'idTok': #since identifiers keywords have similar representations
                found = i
                break
                
        if (found is None) and (name is not None): #if not found, it's and identifier
            last_token_code = self.SYMBOL_TABLE[-1].token_code
            last_token_code += 1
            found = TokenObject(token_lex=inpt, token_code=last_token_code, token_id=name)
            self.SYMBOL_TABLE.append(found)

        print 'process_inpt("',inpt,'",',name,')=',found
        return found

    def process_identifier(self, word):
        token = self.process_inpt(word, 'idTok')
        self.append_token(token)

    def process_num(self, num):#TODO process signed & unsigned integers
        token = self.process_inpt(num, 'numTok')
        self.append_token(token)

    def process_str(self, str):
        token = self.process_inpt(str, 'strTok')
        self.append_token(token)

    def process_chr(self, ch):
        token = self.process_inpt(ch, 'chrTok')
        self.append_token(token)
        
    def process_flt(self, flt):#TODO process signed & unsigned floats
        token = self.process_inpt(flt, 'floatTok')
        self.append_token(token)

    def process_spec(self, spec):
        token = self.process_inpt(spec)
        self.append_token(token)

    def set_read_spec(self, a):
        self.READING_SPEC = a

    def get_read_spec(self):
        return self.READING_SPEC

    def analyse(self, filename):
        """Analyse the source file and come up with a lexeme list and symbol list"""
        fyl = None
        iko_poa = True
        try:
            fyl = open(filename, 'r')
        except:
            print "error opening file '{0}'".format(filename)
            iko_poa = False
            return iko_poa

        ch = None
        cur_str = ""  #string & character buffer
        cur_num = ""  #number & floats buffer
        cur_word = "" #identifier buffer
        cur_spec = ""

        ch = fyl.read(1)
        self.CUR_LINE_NO = 1

        while len(ch) != 0:
            ch = ch.lower()
            ch_type = self.char_type(ch)

            if ch_type == self.CHAR_TYPE_WHITE_SPACE:
                if ch == "\n": self.CUR_LINE_NO += 1

                if self.READING_WORD:
                    self.process_identifier(cur_word)
                    self.READING_WORD = False
                    cur_word = ''
                elif self.get_read_spec():
                    self.process_spec(cur_spec)
                    self.set_read_spec(False)
                    cur_spec = ''
                elif self.READING_NUM:
                    self.process_num(cur_num)
                    self.READING_NUM = False
                    cur_num = ''
                elif self.READING_FLT:
                    self.process_flt(cur_num)
                    self.READING_FLT = False
                    cur_num = ''
                elif self.READING_STR or self.READING_CHR:
                    cur_str += ch

            elif ch_type == self.CHAR_TYPE_ALPHA:
                if self.get_read_spec():
                    self.process_spec(cur_spec)
                    self.set_read_spec(False)
                    cur_spec = ''
                if self.READING_NUM:
                    self.process_num(cur_num)
                    self.READING_NUM = False
                    cur_num = ''
                elif self.READING_FLT:
                    self.process_flt(cur_num)
                    self.READING_FLT = False
                    cur_num = ''
                elif self.READING_STR or self.READING_CHR:
                    cur_str += ch
                else:
                    self.READING_WORD = True
                    cur_word += ch

            elif ch_type == self.CHAR_TYPE_SPEC:
                if self.READING_WORD:
                    self.process_identifier(cur_word)
                    self.READING_WORD = False
                    cur_word = ''
                elif self.get_read_spec():
                    self.process_spec(cur_spec)
                    self.set_read_spec(False)
                    cur_spec = ''
                elif self.READING_NUM:
                    if ch == '.':
                      self.READING_FLT = True
                      cur_num += ch
                    else:
                      self.process_num(cur_num)
                      cur_num = ''
                    self.READING_NUM = False
                elif self.READING_FLT:
                    self.process_flt(cur_num)
                    self.READING_FLT = False
                    cur_num = ''
                elif self.READING_STR or self.READING_CHR:
                    cur_str += ch
                elif ch == '.':
                    cur_num = ch
                    self.READING_FLT = True

                if ch != '.': self.process_spec(ch)

            elif ch_type == self.CHAR_TYPE_SPEC_FOLLOW:
                #print "spec = '{0}' cur_spec='{1}'".format(ch,cur_spec)
                if self.READING_WORD:
                    self.process_identifier(cur_word)
                    self.READING_WORD = False
                    cur_word = ''
                elif self.READING_STR or self.READING_CHR:
                    cur_str += ch
                elif self.get_read_spec() and ch == '=' and len(cur_spec) == 1:
                    cur_spec += '='
                    self.process_spec(cur_spec)
                    self.set_read_spec(False)
                    cur_spec = ''
                elif self.get_read_spec():
                    self.process_spec(cur_spec)
                    self.process_spec(ch)
                    self.set_read_spec(False)
                    cur_spec = ''
                elif self.READING_NUM:
                    self.process_num(cur_num)
                    self.READING_NUM = False
                    cur_num = ''
                elif self.READING_FLT:
                    self.process_flt(cur_num)
                    self.READING_FLT = False
                    cur_num = ''
                else:
                    cur_spec += ch
                    self.set_read_spec(True)

            elif ch_type == self.CHAR_TYPE_NUMBER:
                if self.READING_WORD:
                    cur_word += ch
                elif self.READING_STR or self.READING_CHR:
                    cur_str += ch
                elif self.get_read_spec():
                    self.process_spec(ch)
                    self.set_read_spec(False)
                elif self.READING_NUM or self.READING_FLT:
                  cur_num += ch                
                else:
                    self.READING_NUM = True
                    cur_num += ch

            elif ch_type == self.CHAR_TYPE_QUOTE:
                if self.READING_WORD:
                    self.process_identifier(cur_word)
                    self.READING_WORD = False
                    cur_word = ''
                elif self.READING_NUM:
                    self.process_num(cur_num)
                    self.READING_NUM = False
                    cur_num = ''
                elif self.READING_FLT:
                    self.process_flt(cur_num)
                    self.READING_FLT = False
                    cur_num = ''
                elif self.READING_STR and ch == '"': #closing string literal
                    if cur_str[-1]== '\\':  #escaped quote
                        cur_str = cur_str[:-1]+ch
                    else:  
                        self.process_str(cur_str)
                        self.READING_STR = False
                        cur_str = ''
                elif self.READING_CHR and ch=="'": #closing character literal
                    if cur_str[-1] == '\\':#escaped quote
                        cur_str = cur_str[:-1]+ch
                    elif (len(cur_str) == 1):
                        self.process_chr(cur_str)
                        self.READING_CHR = False
                        cur_str = ''
                    else:
                        print "Invalid character literal '{0}' in line {1}".format(cur_str,self.CUR_LINE_NO)
                        break
                elif self.READING_STR and ch == "'":
                    cur_str += ch
                elif self.READING_CHR and ch == '"':
                    cur_str += ch
                else:
                    if ch == '"':
                        self.READING_STR = True
                    else:
                        self.READING_CHR = True
                        
            elif ch_type == self.CHAR_TYPE_UNKNOWN:
                if self.READING_STR or self.READING_CHR:
                    cur_str += ch
                else:
                    print "Error : Unexpected character '{0}' in line {1}".format(ch,self.CUR_LINE_NO)
                    print "buffers : cur_num[n={0},f={1}] = {2},cur_str[s={3},c={4}]={5},cur_word[{6}]={7},cur_spec_fol[{8}]={9}".format(
                            self.READING_NUM,self.READING_FLT,cur_num,
                            self.READING_STR,self.READING_CHR,cur_str,
                            self.READING_WORD,cur_word,
                            self.READING_SPEC,cur_spec
                            )
                    iko_poa = False
                    break
            ch = fyl.read(1)

        fyl.close()
        if iko_poa:
            lexemes = self.write_lexemes(self.LEXEME_LIST, filename)
            symbols = self.write_symbols(self.SYMBOL_TABLE, filename)
            return (lexemes, symbols)
        else:
            return iko_poa

    def write_lexemes(self, l, f_src='a'):
        fname = f_src + ".tok"
        fyl = open(fname, 'w')
        for i in l:
            fyl.write("{0} {1} {2}".format(i.lex_id, i.lex_code, i.line_no))
            #if i.line_no is not None:
            #  fyl.write(" {0}".format(i.line_no))
            fyl.write("\n")
        fyl.close()
        return fname

    def write_symbols(self, l, f_src='a'):
        fname = f_src + ".sym"
        fyl = open(fname, 'w')
        for i in l:
            fyl.write("{0} {1} {2}\n".format(i.token_id, i.token_code, i.token_lex))
        fyl.close()
        return fname
