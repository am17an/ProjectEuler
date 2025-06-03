import matplotlib.pyplot as plt
import networkx as nx
import os

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def get_largest_child(self):
        if not self.children:
            return None
        return max(self.children, key=lambda x: x.value)

def construct_tree(n):
    if n == 1:
        return Node(1)
    
    prev_tree = construct_tree(n-1)
    
    # Trace path from root to leaf following largest child
    path = []
    current = prev_tree
    while current:
        path.append(current)
        current = current.get_largest_child()
    
    # Create new root
    new_root = Node(n)
    
    # Disconnect nodes in path from their parents and connect to new root
    for node in path:
        # If it's not the root of the previous tree, disconnect from parent
        if node.parent:
            node.parent.children.remove(node)
            node.parent = None
        # Connect to new root
        new_root.add_child(node)
    
    return new_root

def find_path_to_node(root, k):
    # BFS to find node k
    queue = [(root, [root])]
    while queue:
        node, path = queue.pop(0)
        if node.value == k:
            return path
        for child in node.children:
            queue.append((child, path + [child]))
    return None

def f(n, k):
    tree = construct_tree(n)
    path = find_path_to_node(tree, k)
    return sum(node.value for node in path)

def visualize_tree(n):
    tree = construct_tree(n)
    G = nx.DiGraph()
    
    # Add all nodes to the graph
    def add_nodes_and_edges(node):
        G.add_node(node.value)
        for child in node.children:
            G.add_node(child.value)
            G.add_edge(node.value, child.value)
            add_nodes_and_edges(child)
    
    add_nodes_and_edges(tree)
    
    plt.figure(figsize=(15, 12))
    
    # Create a hierarchical tree layout function
    def hierarchy_pos(G, root, width=1., height=1., xcenter=0.5):
        """
        If the graph is a tree this will return the positions to plot this in a 
        hierarchical layout.
        
        Based on Joel's answer at https://stackoverflow.com/a/29597209/2966723,
        but with some modifications.
        
        We include this function directly in the code to avoid external dependencies.
        """
        def _hierarchy_pos(G, root, width, height, xcenter, pos, parent=None, vert=0):
            children = list(G.neighbors(root))
            if parent is not None:
                children.remove(parent)
            if not children:
                pos[root] = (xcenter, vert)
                return pos
                
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, dx, height, nextx, pos, root, vert-height)
            
            pos[root] = (xcenter, vert)
            return pos
            
        pos = {}
        return _hierarchy_pos(G, root, width, height, xcenter, pos)
    
    # Use our hierarchical layout with the tree root at the top
    pos = hierarchy_pos(G, tree.value, width=1.5, height=0.2)
    
    # Draw nodes with larger spacing
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightblue')
    
    # Draw edges with larger arrows
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15, width=1.5)
    
    # Draw labels with larger font
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')
    
    plt.axis('off')
    plt.title(f'Tree T_{n}')
    
    # Add more margins
    plt.tight_layout(pad=3.0)
    
    # Save the figure
    plt.savefig(f'tree_T_{n}.png', dpi=150)
    plt.close()
    print(f"Tree T_{n} visualization saved as tree_T_{n}.png")

# Example tests
# for i in range(1, 20):
#     print(f"f(20, {i}) = {f(20, i)}")

# Visualize T_20
visualize_tree(10)
