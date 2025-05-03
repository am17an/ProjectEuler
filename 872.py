import networkx as nx
import matplotlib.pyplot as plt

def build_tree(n):
    parent = {}
    root = 1
    for i in range(2, n + 1):
        path = []
        node = root
        while node in parent:
            children = [k for k, v in parent.items() if v == node]
            if not children:
                break
            node = max(children)
            path.append(node)
        for p in path:
            parent.pop(p, None)
        for p in path:
            parent[p] = i
        root = i
    return parent

def draw_tree(parent):
    G = nx.DiGraph()
    for child, par in parent.items():
        G.add_edge(par, child)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True)
    plt.show()

# Example usage:
n = 7
parent = build_tree(n)
draw_tree(parent)
