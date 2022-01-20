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
        self.currentToken = None
        self.lookAhead = None
        self.nextToken()

    
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


class RELexer(AbstractLexer):
    def __init__(self, str, tokensDict):
        super().__init__(str, tokensDict)
    
    def nextToken(self):
        self.currentToken = self.lookAhead
        if self.currentChar in self.tokensDict:
            self.lookAhead = Token(self.tokensDict[self.currentChar], self.currentChar)
        elif self.currentChar != None:
            self.lookAhead = Token("CHAR", self.currentChar)
        else:
            self.lookAhead = None
    
            
        