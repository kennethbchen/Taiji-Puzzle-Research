from vedo import show, Spheres, Lines, Plotter, Sphere, Line
from Node import Node
from Edge import Edge
from puzzles import puzzles
from functools import partial
import pandas

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

selected_puzzle = "set_cover"
boards = puzzles[selected_puzzle]["boards"]

render_diagonals = puzzles[selected_puzzle]["diagonals"] if "diagonals" in puzzles[selected_puzzle] else False

layer_colors = ["red", "green", "blue", "cyan", "magenta", "yellow", "orange", "purple", "white"]

dimensions = {
    "rows": len(boards[0]),
    "cols": len(boards[0][0]),
    "boards": len(boards)
}

node_data = {}
edge_data = []
symbol_data = []


# ----- Setup Boards -----
for layer_i, layer in enumerate(boards):

    # Create node objects
    for row in range(0, len(layer)):
        for col in range(0, len(layer[row])):
            node_data[(col, layer_i, row)] = Node(col=col, row=row, region=layer[row][col], layer=layer_i)


# ----- Add neighbors -----
for i, (key, tile) in enumerate(node_data.items()):


    neighbors = [
        # Cardinals
        (tile.col - 1, tile.layer, tile.row),
        (tile.col + 1,  tile.layer, tile.row),
        (tile.col, tile.layer, tile.row - 1),
        (tile.col, tile.layer, tile.row + 1),
    ]

    if render_diagonals:
        neighbors.extend([
        (tile.col - 1, tile.layer, tile.row - 1),
        (tile.col + 1, tile.layer, tile.row + 1),
        (tile.col - 1, tile.layer, tile.row + 1),
        (tile.col + 1, tile.layer, tile.row - 1)])

    # Create edges between neighbors
    for neighbor in neighbors:
        if neighbor in node_data:
            tile.add_neighbor(node_data[neighbor])


            if tile.should_have_edge(node_data[neighbor]):
                edge_data.append(Edge(tile, node_data[neighbor]))

# ----- Visualize -----

plot = Plotter(axes=1, bg="gray")


def on_opacity_slider(layer_index, widget, event):
    for node in nodes[layer_index]:
        node.alpha(widget.value)

    edges[layer_index].alpha(widget.value)


def on_mouse_click(event):
    mesh = event.actor

    if not mesh or not mesh.pickable:
        return

    if not add_symbol(mesh.pos()[0], mesh.pos()[2]):
        remove_symbol(mesh.pos()[0], mesh.pos()[2])

    plot.render()


def on_mouse_move(event):
    mesh = event.actor

    if not mesh or not mesh.pickable:
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

n_centers = [[] for x in range(dimensions["boards"])]
n_colors = [[] for x in range(dimensions["boards"])]

for i in range(dimensions["boards"]):
    n_centers[i] = []
    n_colors[i] = []

for node in node_data.values():

    n_centers[node.layer].append(node.coordinates())
    n_colors[node.layer].append(layer_colors[node.layer])

e_endpoints = [[] for x in range(dimensions["boards"])]
e_colors = [[] for x in range(dimensions["boards"])]

for edge in edge_data:
    board_idx = edge.parent_a.layer
    e_endpoints[board_idx].append(edge.endpoints())
    e_colors[board_idx].append(layer_colors[board_idx])


edges = [[] for x in range(dimensions["boards"])]


for board_idx in range(dimensions["boards"]):

    edges[board_idx] = Lines(start_pts=e_endpoints[board_idx], res=0, lw=5, c=layer_colors[board_idx], alpha=1)
    edges[board_idx].pickable = False


nodes = [[] for x in range(len(n_centers))]

for board_idx in range(len(n_centers)):
    for i in range(len(n_centers[board_idx])):
        s = Sphere(r=0.1, alpha=1).pos(n_centers[board_idx][i]).color(n_colors[board_idx][i])
        s.name = f"sphere at {n_centers[board_idx][i]}"
        nodes[board_idx].append(s)

plot.add_callback('mouse move', on_mouse_move)
plot.add_callback("mouse click", on_mouse_click)

slider_origin = (0.05, 0.1)
slider_size = (0.1, 0.1)

for board_idx in range(len(n_centers)):
    plot.add_slider(
        partial(on_opacity_slider, board_idx),
        xmin=0.0,
        xmax=1.0,
        value=1.0,
        pos=[[slider_origin[0], slider_origin[1] * (board_idx + 1)],[slider_origin[0] + slider_size[0], slider_origin[1] * (board_idx + 1)]],
        title=f"Lyr {board_idx+1} Alpha",
        show_value=False
    )





plot.show(edges, nodes, list(symbols.values()), at=0).interactive().close()
exit()