import json
import networkx as nx
import matplotlib.pyplot as plt


def visualize():
    data = load_data()

    G = nx.Graph()
    for user, followers in data.items():
        for follower in followers:
            G.add_edge(user, follower)

    pos = nx.spring_layout(G, k=0.5)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=40, node_color="skyblue", font_size=4, font_color="black", edge_color="gray", width=0.1)
    x_values, y_values = zip(*pos.values())
    x_margin = (max(x_values) - min(x_values)) * 0.1
    y_margin = (max(y_values) - min(y_values)) * 0.1

    plt.xlim(min(x_values) - x_margin, max(x_values) + x_margin)
    plt.ylim(min(y_values) - y_margin, max(y_values) + y_margin)
    plt.title('Social Network')
    plt.savefig("vars/visualization.png")
    plt.show()


def load_data(filename="vars/connections.json"):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
if __name__=="__main__":
    visualize()
