from ursina import Entity, Pipe


class Edge(Entity):
    def __init__(self, parent_a, parent_b, **kwargs):
        super().__init__(**kwargs)

        self.parent_a = parent_a
        self.parent_b = parent_b

        self.model = Pipe(path=(self.parent_a.position, self.parent_b.position), thicknesses=(0.1, 0.1))
        self.color = self.parent_a.color
