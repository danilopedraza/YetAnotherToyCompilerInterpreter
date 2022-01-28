from mylexer import Lexer
from re_to_nfa import ASTNode

class Parser:
    def __init__(self, lang):
        self.tokens, self.grammar = lang["tokens"], lang["grammar"]
        self.lexer = Lexer(self.tokens)

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
        res = []

        self.lexer.set(expr)
        self.advanceTokens()
        self.advanceTokens()

        
        stack = ["EOF", self.grammar[0][0]]
        while stack[-1] != "EOF":
            if stack[-1] in self.terminals:
                if stack[-1] == self.currentToken.type:
                    self.advanceTokens()
                    stack.pop()
                else:
                    return None
            else:
                rule = self.table[stack[-1]][self.currentToken.type]
                if rule == None:
                    return None
                stack.pop()
                if rule[1] != [""]:
                    stack += rule[1][::-1]

                
                res.append(rule)
        
        return res

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
        conc = "".join(symbols)

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


            for _ in range(10):
                self.computeFollow(initial=False)
            
            
        


        for variable in self.nonTerminals:
            for _, rule in self.grammar:
                for i in range(1, len(rule)):
                    if variable == rule[i - 1]:
                        temp = self.first(rule[i:])
                        self.followCache[variable].update(temp)
                        if "" in self.followCache[variable]:
                            self.followCache[variable].discard("")
                        
        
        for variable in self.nonTerminals:
            for nonTerminal, rule in self.grammar:
                if variable == rule[-1]:
                    self.followCache[variable].update(self.followCache[nonTerminal])
                    continue
                
                for i in range(1, len(rule)):
                    if variable == rule[i - 1] and "" in self.first(rule[i:]):
                        self.followCache[variable].update(self.followCache[nonTerminal])
                        break
    
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

            
            for _ in range(4):
                self.computeFirst(initial=False)


        
        for variable, rule in self.grammar:
            epsilonInAll = True
            for i in range(len(rule)):
                if epsilonInAll:
                    self.firstCache[variable].update(self.firstCache[rule[i]])
                    epsilonInAll = ("" in self.firstCache[rule[i]])
                else:
                    break
            
            #if not epsilonInAll:
            #    self.firstCache[variable].discard("")
        
        for variable, rule in self.grammar:
            conc = "".join(rule)
            if conc not in self.firstCache:
                self.firstCache[conc] = set()
            epsilonInAll = True
            for i in range(len(rule)):
                if epsilonInAll:
                    self.firstCache[conc].update(self.firstCache[rule[i]])
                    epsilonInAll = ("" in self.firstCache[rule[i]])
                else:
                    break
            
            #if not epsilonInAll:
            #    self.firstCache[conc].discard("")
