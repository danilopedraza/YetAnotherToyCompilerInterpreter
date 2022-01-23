from enum import IntEnum

from lexer import (
    AbstractLexer,
    Token
)
from parser import ASTNode

class RELexer(AbstractLexer):
    def __init__(self, str, tokensDict):
        super().__init__(str, tokensDict)
        
    
    def nextToken(self):
        if self.currentChar in self.tokensDict:
            token = Token(self.tokensDict[self.currentChar], self.currentChar)
        elif self.currentChar != None:
            token = Token("CHAR", self.currentChar)
        else:
            return Token("EOF", "")
        self.nextChar()
        return token


class REParser:
    class Precedences(IntEnum):
        LOWEST = 0
        UNION = 1,
        CONCAT = 2


    def __init__(self):
        self.tokensDict = {
            "(" : "LPAREN",
            ")" : "RPAREN",
            "|" :  "UNION",
            "*" :   "STAR" 
        }

        self.currentToken = None
        self.lookAhead = None
    
    def currentPrecedence(self):
        if self.currentToken.type in ["CHAR","LPAREN"]:
            return self.Precedences.CONCAT
        elif self.currentToken.type == "UNION":
            return self.Precedences.UNION
        else:
            return self.Precedences.LOWEST
    
    def advanceTokens(self):
        self.currentToken = self.lookAhead
        self.lookAhead = self.lexer.nextToken()

    def parse(self, expr):
        self.lexer = RELexer(expr, self.tokensDict)
        self.advanceTokens()
        self.advanceTokens()

        return self.parseExpression(self.Precedences.LOWEST)

    def parseExpression(self, precedence):
        # first expression section
        node = None
        if self.currentToken.type == "LPAREN":
            node = self.parseParenthesis()
        elif self.currentToken.type == "CHAR":
            node = self.parseChar()
        else:
            return None # expected a prefix
        
        if node == None:
            return None
        
        # postfix verification
        if self.currentToken.type == "STAR":
            node = self.parseStar(node)
            
            if node == None:
                return None
        
        #infix verification
        while self.currentToken.type in ["CHAR", "LPAREN", "UNION"] and precedence < self.currentPrecedence():
            node = self.parseInfix(node)
            if node == None:
                return None
        
        return node



    def parseParenthesis(self):
        self.advanceTokens()
        node = self.parseExpression(self.Precedences.LOWEST)
        if (self.currentToken.type == "RPAREN"):
            self.advanceTokens()
            return node
        else:
            return None

    def parseChar(self):
        node = ASTNode("CHAR", self.currentToken.literal)
        self.advanceTokens()
        return node
    
    def parseStar(self, node):
        newNode = ASTNode("STAR")
        newNode.children.append(node)
        self.advanceTokens()
        return newNode
    
    def parseInfix(self, left):
        prec = self.currentPrecedence()
        if self.currentToken.type == "UNION":
            self.advanceTokens()
            right = self.parseExpression(prec)
            infix = ASTNode("UNION")
        else:
            right = self.parseExpression(prec)
            infix = ASTNode("CONCAT")
        
        if right == None:
            return None
        
        infix.children = [left, right]
        return infix
