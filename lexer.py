import json
from re_to_nfa import NFAUnionFromREs

def getLangInfo(filename):
    f = open(filename)
    res = json.load(f)
    f.close()
    return res


class Token:
    def __init__(self, type, literal):
        self.type = type
        self.literal = literal


class AbstractLexer:
    def __init__(self, tokensDict):
        self.tokensDict = tokensDict
    
    def set(self, str):
        self.str = str
        self.index = 1
        self.nextChar()

    def nextChar(self):
        if self.index < len(self.str):
            self.currentChar = self.str[self.index - 1]
            self.lookAheadChar = self.str[self.index]
            self.index += 1
        elif self.index == len(self.str):
            self.currentChar = self.str[self.index - 1]
            self.lookAheadChar = None
            self.index += 1
        else:
            self.currentChar = None
            self.lookAheadChar = None

    def nextToken(self):
        raise NotImplementedError()


class Lexer(AbstractLexer):
    def __init__(self, tokensDict):
        super().__init__(tokensDict)
        
        self.nfa = NFAUnionFromREs(
            [self.tokens[key] for key in self.tokens],
            [key for key in self.tokens]
        )
        
    def nextToken(self):
        pass # TODO
