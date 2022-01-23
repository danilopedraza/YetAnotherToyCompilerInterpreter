# El parser debería recibir un objeto con atríbutos currentToken y
# lookAhead, y un método nextToken(), junto a una gramática.

class ASTNode:
    def __init__(self, type, literal = None):
        self.type = type
        self.literal = literal
        self.children = []

