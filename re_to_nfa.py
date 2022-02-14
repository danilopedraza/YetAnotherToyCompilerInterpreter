from enum import IntEnum


class Token:
    def __init__(self, type, literal):
        self.type = type
        self.literal = literal


class AbstractLexer:
    def __init__(self, tokens):
        self.tokens = tokens
    
    def set(self, str):
        self.str = str
        self.index = 0
        self.nextChar()

    def nextChar(self):
        if self.index + 1 < len(self.str):
            self.index += 1
            self.currentChar = self.str[self.index - 1]
            self.lookAheadChar = self.str[self.index]
        elif self.index + 1 == len(self.str):
            self.index += 1
            self.currentChar = self.str[self.index - 1]
            self.lookAheadChar = None
            
        else:
            self.currentChar = None
            self.lookAheadChar = None

    def nextToken(self):
        raise NotImplementedError()


class ASTNode:
    def __init__(self, type, literal = None):
        self.type = type
        self.literal = literal
        self.children = []


class RELexer(AbstractLexer):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.tokensDict = {pair[1]:pair[0] for pair in tokens}
        
    
    def nextToken(self):
        if self.currentChar == "\\":
            self.nextChar()
            token = Token("CHAR", self.currentChar)
        elif self.currentChar in self.tokensDict:
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
        self.tokens = [
            ("LPAREN", "("),
            ("RPAREN", ")"),
            ("UNION" , "|"),
            ("STAR"  , "*"),
        ]
        self.lexer = RELexer(self.tokens)

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
        self.lexer.set(expr)
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


class NFA:
    def __init__(self, graph = [], initial = None, accepting = None):
            self.graph = graph
            self.initial = initial
            self.accepting = accepting
    
    def epsilonClosure(self, states):
        stack = states + []

        while len(stack) > 0:
            t = stack.pop()
            if "" in self.graph[t]:
                for u in self.graph[t][""]:
                    if u not in states:
                        states.append(u)
                        stack.append(u)
        
        return states
    
    def move(self, states, symbol):
        res = []
        for state in states:
            if symbol in self.graph[state]:
                res += self.graph[state][symbol]
        
        return res
        

def getNFA(root):
    if root.type == "CHAR":
        return NFA(
            [
                {root.literal:[1]},
                {}
            ],
            0,
            1
        )
    elif root.type == "CONCAT":
        left = getNFA(root.children[0])
        right = getNFA(root.children[1])
        
        left.graph.pop()
        newStart = len(left.graph)

        for i in range(len(right.graph)):
            for key in right.graph[i]:
                for j in range(len(right.graph[i][key])):
                    right.graph[i][key][j] += newStart
            
        return NFA(
            left.graph + right.graph,
            left.initial,
            right.accepting + newStart
        )
    elif root.type == "UNION":
        left = getNFA(root.children[0])
        right = getNFA(root.children[1])

        res = NFA(
            [
                {"":[1, 1 + len(left.graph)]}
            ],
            0,
            1 + len(left.graph) + len(right.graph)
        )

        if "" in left.graph[left.accepting]:
            left.graph[left.accepting][""].append(len(left.graph) + len(right.graph))
        else:
            left.graph[left.accepting][""] = [len(left.graph) + len(right.graph)]

        newStart = 1        
        for i in range(len(left.graph)):
            for key in left.graph[i]:
                for j in range(len(left.graph[i][key])):
                    left.graph[i][key][j] += newStart
        
        res.graph += left.graph
        
        if "" in right.graph[right.accepting]:
            right.graph[right.accepting][""].append(len(right.graph))
        else:
            right.graph[right.accepting][""] = [len(right.graph)]

        newStart += len(left.graph)
        for i in range(len(right.graph)):
            for key in right.graph[i]:
                for j in range(len(right.graph[i][key])):
                    right.graph[i][key][j] += newStart
        
        res.graph += right.graph
        res.graph.append({})

        return res
    elif root.type == "STAR":
        exp = getNFA(root.children[0])
        res = NFA(
            [
                {"":[1, len(exp.graph)]}
            ],
            0,
            len(exp.graph)
        )

        if "" in exp.graph[exp.accepting]:
            exp.graph[exp.accepting][""] += [exp.initial,res.accepting]
        else:
            exp.graph[exp.accepting][""] = [exp.initial,res.accepting]


        for i in range(len(exp.graph)):
            for key in exp.graph[i]:
                for j in range(len(exp.graph[i][key])):
                    exp.graph[i][key][j] += 1
        
        res.graph += exp.graph
        res.graph.append({})
        res.accepting += 1
    
        return res
    else:
        return None


def NFAUnionFromREs(tokens):
    if len(tokens) == 0:
        return None
    
    parser = REParser()

    res = NFA(
        [{"":[]}],
        0,
        {}
    )

    for i in range(len(tokens)):
        temp = getNFA(parser.parse(tokens[i][1]))
        
        res.graph[res.initial][""].append(temp.initial + len(res.graph))
        res.accepting[temp.accepting + len(res.graph)] = tokens[i][0]
        

        for j in range(len(temp.graph)):
            for key in temp.graph[j]:
                for k in range(len(temp.graph[j][key])):
                    temp.graph[j][key][k] += len(res.graph)
        
        res.graph += temp.graph
    
    return res
