from re_to_nfa import ASTNode

class Parser:
    def __init__(self, lexer, tokens, grammar):
        self.tokens, self.grammar = tokens, grammar
        self.lexer = lexer

        self.currentToken = None
        self.lookAhead = None

        self.terminals    = {pair[0] for pair in self.tokens}
        self.terminals.add("EOF")
        self.nonTerminals = {pair[0] for pair in self.grammar}

        self.firstCache = {}
        self.followCache = {}
        self.table = {}
        self.computeFirst()
        self.computeFollow()
        self.computeTable()
    
    def advanceTokens(self):
        self.currentToken = self.lookAhead
        self.lookAhead = self.lexer.nextToken()
    
    def parse(self, expr):
        self.lexer.set(expr)
        self.advanceTokens()
        self.advanceTokens()

        root = ASTNode(self.grammar[0][0])
        nodeStack = [root]
        
        stack = [self.grammar[0][0]]
        while stack != []:
            if stack[-1] in self.terminals:
                if stack[-1] == self.currentToken.type:
                    nodeStack[-1].literal = self.currentToken.literal
                    nodeStack.pop()
                    
                    self.advanceTokens()
                    stack.pop()
                else:
                    return None
            else:
                rule = self.table[stack[-1]][self.currentToken.type]
                if rule == None:
                    return None
                
                stack.pop()

                temp = nodeStack[-1]
                nodeStack.pop()

                if rule[1] != [""]:
                    stack += rule[1][::-1]

                    temp.children = [ASTNode(type) for type in rule[1]]
                    nodeStack += temp.children[::-1]
                else:
                    temp.children = [ASTNode("EPSILON", "")]
        
        return root

    def computeTable(self):
        for nonTerminal in self.nonTerminals:
            self.table[nonTerminal] = {}
        
        for nonTerminal, rule in self.grammar:
            for terminal in self.first(rule):
                if terminal != "":
                    self.table[nonTerminal][terminal] = (nonTerminal,rule)
            if "" in self.first(rule):
                for terminal in self.follow(nonTerminal):
                        self.table[nonTerminal][terminal] = (nonTerminal,rule)
        
            if "" in self.first(rule) and "EOF" in self.follow(nonTerminal):
                self.table[nonTerminal]["EOF"] = (nonTerminal,rule)

    def follow(self, variable):
        if variable not in self.nonTerminals:
            raise Exception()
        else:
            return self.followCache[variable]

    def first(self, symbols):
        conc = " ".join(symbols)

        if conc in self.firstCache:
            return self.firstCache[conc]
        else:
            self.firstCache[conc] = set()
            epsilonInAll = True
            for i in range(len(symbols)):
                if epsilonInAll:
                    self.firstCache[conc].update(self.firstCache[symbols[i]])
                    epsilonInAll = ("" in self.firstCache[symbols[i]])
                else:
                    break
            
            #if not epsilonInAll:
            #    self.firstCache[conc].discard("")
        
            return self.firstCache[conc]

    def computeFollow(self, initial=True):
        if initial:
            for variable in self.nonTerminals:
                self.followCache[variable] = set()
            
            self.followCache[self.grammar[0][0]] = set(["EOF"])
        
        repeated = True
        
        for variable in self.nonTerminals:
            for _, rule in self.grammar:
                for i in range(1, len(rule)):
                    if variable == rule[i - 1]:
                        temp = set(self.first(rule[i:]))
                        temp.discard("")
                        if not temp.issubset(self.followCache[variable]):
                            repeated = False
                        self.followCache[variable].update(temp)
                        
        
        for variable in self.nonTerminals:
            for nonTerminal, rule in self.grammar:
                if variable == rule[-1]:
                    if not self.followCache[nonTerminal].issubset(self.followCache[variable]):
                        repeated = False
                    self.followCache[variable].update(self.followCache[nonTerminal])
                    continue
                
                for i in range(1, len(rule)):
                    if variable == rule[i - 1] and "" in self.first(rule[i:]):
                        self.followCache[variable].update(self.followCache[nonTerminal])
                        break
        
        if not repeated:
            self.computeFollow(initial=False)
    
    def computeFirst(self, initial=True):
        if initial:
            self.firstCache[""] = set([""])
            for terminal in self.terminals:
                self.firstCache[terminal] = set([terminal])
            
            for variable, rule in self.grammar:
                a = (rule == [""])
                b = (variable in self.firstCache)
                if a and b:
                    self.firstCache[variable] = set([""])
                elif a and not b:
                    self.firstCache[variable] = set([""])
                elif not a and b:
                    pass
                else:
                    self.firstCache[variable] = set()


        repeated = True

        for variable, rule in self.grammar:
            epsilonInAll = True
            for i in range(len(rule)):
                if epsilonInAll:
                    if not self.firstCache[rule[i]].issubset(self.firstCache[variable]):
                        repeated = False
                    self.firstCache[variable].update(self.firstCache[rule[i]])
                    epsilonInAll = ("" in self.firstCache[rule[i]])
                else:
                    break
            
            #if not epsilonInAll:
            #    self.firstCache[variable].discard("")
        
        for variable, rule in self.grammar:
            conc = " ".join(rule)
            if conc not in self.firstCache:
                self.firstCache[conc] = set()
            epsilonInAll = True
            for i in range(len(rule)):
                if epsilonInAll:
                    if not self.firstCache[rule[i]].issubset(self.firstCache[conc]):
                        repeated = False
                    self.firstCache[conc].update(self.firstCache[rule[i]])
                    epsilonInAll = ("" in self.firstCache[rule[i]])
                else:
                    break
            
            if not repeated:
                self.computeFirst(initial=False)
