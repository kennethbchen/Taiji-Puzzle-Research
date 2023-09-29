class Edge():
    def __init__(self, parent_a, parent_b):

        self.parent_a = parent_a
        self.parent_b = parent_b

    def endpoints(self):
        return [self.parent_a.coordinates(), self.parent_b.coordinates()]
