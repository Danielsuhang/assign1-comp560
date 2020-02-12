class Node():
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.color = ""

    def __repr__(self):
        return self.name
