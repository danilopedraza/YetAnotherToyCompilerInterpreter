from myparser import Parser

def treeToTeX(tree):
    if (tree.literal != None):
        if tree.type == "EPSILON":
            return '$\\epsilon$'
        return "$"+tree.literal+"$"
    
    res = "[.$"+tree.type+"$ "
    for subtree in tree.children:
        res+=treeToTeX(subtree)+" "
    
    return res+"]"


tokens = [
    ("INT", "(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*"),
    ("PLUS","+"),
    ("MINUS", "-"),
    ("LPAREN", "["),
    ("RPAREN", "]")
]

grammar = [
    ("E", ["T","E2"]),
    ("E2", ["PLUS", "T","E2"]),
    ("E2", [""]),
    ("T", ["F", "T2"]),
    ("T2", ["MINUS", "F", "T2"]),
    ("T2", [""]),
    ("F", ["LPAREN", "E", "RPAREN"]),
    ("F", ["INT"])
]

a = Parser(tokens, grammar)
tree = a.parse("5-2+7")
print("\\Tree "+treeToTeX(tree))
