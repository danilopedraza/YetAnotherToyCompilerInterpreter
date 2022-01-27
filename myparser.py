from mylexer import Lexer

class Parser:
    def __init__(self, lang):
        self.lexer = Lexer(lang["tokens"])

        self.currentToken = None
        self.lookAhead = None

        self.terminals    = {key[0] for key in lang["tokens"]}
        self.nonTerminals = {key[0] for key in lang["grammar"]}

        self.first = {}
        self.follow = {}
        self.computeFirst()
        self.computeFollow()

        self.table = {} 
        self.computeTable()
        
    
    def advanceTokens(self):
        self.currentToken = self.lookAhead
        self.lookAhead = self.lexer.nextToken()
    
    def parse(self, expr):
        pass # TODO

    def computeFirst(self):
        pass # TODO

    def computeFollow(self):
        pass # TODO
