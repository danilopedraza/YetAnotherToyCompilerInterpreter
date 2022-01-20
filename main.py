import json 

def getLangInfo(filename):
    f = open(filename)
    res = json.load(f)
    f.close()
    return res

