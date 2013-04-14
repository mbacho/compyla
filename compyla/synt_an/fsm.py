#!/usr/bin/env python


class Fxn(object):
    ANY_INPT = '$A'
    EMPTY = '$E'

    def __init__(self, token=ANY_INPT, tos=None, replacements=()):
        """Create a transition function"""
        self.token = token
        self.tos = tos
        self.replacements = replacements

    def __repr__(self):
        return "({0},{1},{2})-->({3},{4})".format('cur state', self.token, self.tos, 'nxt state', self.replacements.__repr__())

    def __str__(self):
        return self.__repr__()


class State(object):
    def __init__(self, name, is_final=False):
        self.name = name
        self.is_final = is_final
        self.fxns = []

    def add_fxn(self, fxn):
        """Add transition function"""
        self.fxns.append(fxn)

    def trans_for(self, token, tos):
        print 'match (', token, ',', tos, ')'
        for i in self.fxns:
            if (i.token.lower() == token.lower() or i.token == Fxn.ANY_INPT) and i.tos == tos:
                print i.__repr__()
                return i
        return None

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class ParseException(BaseException):
    def __init__(self,msg,lexeme=None):
        self.lexeme = lexeme
        super(ParseException, self).__init__(msg)

        
class Stack():
    """Simple stack implementation"""
    STACK_INIT = '$'

    def __init__(self):
        self.stack = list(self.STACK_INIT)

    def __len__(self):
        return len(self.stack) - 1

    def __repr__(self):
        return self.stack.__repr__() + ' (tos)'

    def __str__(self):
        return self.__repr__()

    def pop(self):
        """Remove element from tos and return it"""
        if self.__len__() > 0:
            i = self.stack.pop()
            return i
        else:
            return None

    def push(self, c):
        """Add element c to tos and then return this Stack instance to enable method chaining
           e.g. s = Stack()
                s.push('a').push('b')
        """
        self.stack.append(c)
        return self

    def tos(self):
        """Returns element on tos"""
        if self.__len__() > 0:
            return self.stack[-1]
        else:
            return None

    def is_empty(self):
        return self.__len__() <= 0

        
class Pda(object):
    def __init__(self):
        self.stack = Stack()
        self.start_state = None

    def set_start_state(self, state):
        if isinstance(state, State) or isinstance(state, None):
            self.start_state = state
        else:
            raise ParseException("Invalid state provided")

    def parse_string(self, s):
        """Parse token string list"""
        cur_state = self.start_state
        if cur_state is None:
            raise ParseException("No start state provided")

        size = len(s)
        cur_tok = 0
        while cur_tok < size:
            i = s[cur_tok]
            print '\n', self.stack
            tos = self.stack.pop()
            trans = cur_state.trans_for(i.lex_id, tos)
            if trans is None:
                raise ParseException("No transition found for {0} in state {1}".format(i.lex_id, cur_state.name),i)

            nxt_state, pushes = trans.replacements
            if len(pushes) == 0:
                cur_tok += 1

            rev = reversed(pushes) #list.reverse mutates the list :(
            for j in rev:
                self.stack.push(j)
            cur_state = nxt_state

        if not self.stack.is_empty():
            raise ParseException("PDA terminated with non-empty stack")

        print "parse ok"

    def load_fsm(self, fname):
        """
        Loads an fsm from a text file

        The file is structured as follows

        #states
        state_one_name
        state_two_name
        #fxns
        state_one_name, token, state_two_name, push_char
        state_two_name, token, state_two_name, push_char
        """
        pass
    
