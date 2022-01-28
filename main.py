import json
from myparser import Parser

def getLangInfo(filename):
    f = open(filename)
    res = json.load(f)
    f.close()
    return res


a = Parser(
    {
        "tokens":[
            ("INT", "(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*"),
            ("PLUS","+"),
            ("MINUS", "-"),
            ("LPAREN", "["),
            ("RPAREN", "]")
        ],
        "grammar":[
            ("E", ["T","E2"]),
            ("E2", ["PLUS", "T","E2"]),
            ("E2", [""]),
            ("T", ["F", "T2"]),
            ("T2", ["MINUS", "F", "T2"]),
            ("T2", [""]),
            ("F", ["LPAREN", "E", "RPAREN"]),
            ("F", ["INT"])
        ]
    }
)
tree = a.parse("5+2")
