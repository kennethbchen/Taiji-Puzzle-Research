from vedo import show, Spheres, Lines, Plotter, Sphere, Line
from Node import Node
from Edge import Edge
from puzzles import puzzles

"""
    Coordinate System:
    +x - right
    +y - up
    +z - backwards
    
    In relation to board data:
    x-axis: columns
    y-axis: boards
    z-axis: rows
    
    (x, y, z) -> (column, board, row)
"""

selected_puzzle = "taiji"
symbols = puzzles[selected_puzzle]["symbols"]
region_capacity = puzzles[selected_puzzle]["region_capacity"]
boards = puzzles[selected_puzzle]["boards"]

layer_colors = ["red", "green", "blue", "cyan", "magenta"]

dimensions = {
    "rows": len(boards[0]),
    "cols": len(boards[0][0]),
    "boards": len(boards)
}

node_data = {}
edge_data = []
symbol_data = [(3, 0), (4, 0), (2, 2), (3, 2), (0, 3), (2, 3), (2, 4), (1, 5)]



# Setup
for layer_i, layer in enumerate(boards):

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
plot = Plotter(axes=1, bg="gray")


def on_mouse_click(event):
    mesh = event.actor

    if not mesh:
        return

    if not add_symbol(mesh.pos()[0], mesh.pos()[2]):
        print("removed")
        remove_symbol(mesh.pos()[0], mesh.pos()[2])

    print(symbols)
    plot.render()

def on_mouse_move(event):
    mesh = event.actor

    if not mesh:
        plot.remove('silu')
        plot.render()
        return

    # Highlight selected
    sil = event.actor.silhouette().linewidth(6).c('white')
    sil.name = "silu"
    plot.remove('silu').add(sil)
    plot.render()

symbols = {}

def remove_symbol(row, col):

    if ((row, col)) not in symbols:
        return False

    symbol = symbols.pop((row, col))
    plot.remove(symbol)

def add_symbol(row, col):

    if ((row, col)) in symbols:
        return False

    line_start = (row, 0, col)
    line_end = (row, dimensions["boards"] - 0.5, col)

    l = Line(p0=line_start, p1=line_end, res=0, lw=5, c="white", alpha=1)
    symbols[(row, col)] = l

    plot.add(l)
    return True

for symbol_coord in symbol_data:
    add_symbol(symbol_coord[0], symbol_coord[1])

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

nodes = []

for i in range(len(n_centers)):
    s = Sphere(r=0.1, alpha=1).pos(n_centers[i]).color(n_colors[i])
    s.name = f"sphere nr.{i} at {n_centers[i]}"
    nodes.append(s)



plot.add_callback('mouse move', on_mouse_move)
plot.add_callback("mouse click", on_mouse_click)

plot.show(edges, nodes, list(symbols.values()), at=0).interactive().close()
exit()