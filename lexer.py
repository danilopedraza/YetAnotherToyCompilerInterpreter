import json 

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
    def __init__(self, str, tokensDict):
        self.str = str
        self.index = 1
        self.nextChar()

        self.tokensDict = tokensDict

    
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
