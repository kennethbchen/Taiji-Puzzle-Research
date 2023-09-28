from ursina import Entity


class Node(Entity):
    def __init__(self, col, row, region, layer, **kwargs):
        super().__init__(**kwargs)
        self.col = col
        self.row = row
        self.layer = layer

        self.region = region

        self.neighbors = set()

    def add_neighbor(self, newNode):

        if newNode.region != self.region:
            return

        if newNode not in self.neighbors:
            self.neighbors.add(newNode)

        if self not in newNode.neighbors:
            newNode.add_neighbor(self)

    def coordinates(self):
        return (self.col, self.layer, self.row)

    def should_have_edge(self, node):
        return (self.col < node.col and self.row <= node.row) or (self.col <= node.col and self.row < node.row)

    def __str__(self):
        return "Node at ({col},{layer},{row}) in region {}"
        return "Node at (" + str(self.col) + ", " + str(self.row) + ") in region " + str(self.region)