from vedo import show, Spheres, Lines


from Node import Node
from Edge import Edge

layers = [
    [
        [1, 1, 1, 1, 1, 4],
        [2, 2, 2, 2, 1, 4],
        [2, 3, 3, 2, 1, 4],
        [2, 3, 4, 1, 1, 4],
        [2, 3, 4, 4, 4, 4],
        [2, 3, 3, 3, 3, 3],
    ],
    [
        [1, 1, 1, 1, 1, 2],
        [3, 3, 3, 3, 1, 2],
        [3, 3, 3, 4, 2, 2],
        [5, 3, 4, 4, 4, 2],
        [5, 3, 3, 3, 3, 6],
        [5, 5, 3, 3, 7, 8],
    ],
    [
        [1, 1, 1, 2, 2, 7],
        [1, 2, 2, 2, 8, 9],
        [1, 2, 3, 3, 10, 11],
        [1, 1, 4, 4, 1, 6],
        [5, 1, 4, 1, 1, 6],
        [5, 1, 1, 1, 6, 6],
    ],

]

layerss = [
    [
        [1, 2, 2, 2],
        [1, 1, 2, 3],
    ],
    [
        [1, 1, 2, 2],
        [1, 2, 2, 2],
    ],
    [
        [1, 1, 1, 1],
        [2, 2, 2, 1],
    ],

]

layer_colors = ["red", "green", "blue"]

node_data = {}
edge_data = []
symbol_data = [(0, 1), (1, 1)]

spacing = 1.5

# Setup
for layer_i, layer in enumerate(layers):

    # Create node objects
    for row in range(0, len(layer)):
        for col in range(0, len(layer[row])):
            node_data[(col, layer_i, row)] = Node(col=col, row=row, region=layer[row][col], layer=layer_i)


# Add neighbors
for i, (key, tile) in enumerate(node_data.items()):

    neighbors = [
        (tile.col - 1, tile.layer, tile.row),
        (tile.col + 1,  tile.layer, tile.row),
        (tile.col, tile.layer, tile.row - 1),
        (tile.col, tile.layer, tile.row + 1),
    ]

    for neighbor in neighbors:

        if neighbor in node_data:

            tile.add_neighbor(node_data[neighbor])

            if tile.should_have_edge(node_data[neighbor]):
                edge_data.append(Edge(tile, node_data[neighbor]))


# Visualize

n_centers = []
n_colors = []

for node in node_data.values():
    n_centers.append(node.coordinates())
    n_colors.append(layer_colors[node.layer])

e_endpoints = []
e_colors = []
for edge in edge_data:
    e_endpoints.append(edge.endpoints())
    e_colors.append('white')

edges = Lines(start_pts=e_endpoints, res=0, lw=5, c="black", alpha=1)
nodes = Spheres(centers=n_centers, r=0.2, c=n_colors, alpha=1)

show(edges, nodes, at=0, axes=1, bg="gray").interactive().close()
exit()