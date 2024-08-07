import plotly.express as px
import networkx as nx
import plotly.graph_objs as go
try:
    from . import utils
except ImportError:
    import utils

def cluster(seed=0, k=100):
    data = utils.load_connections()

    G = nx.Graph()
    for user, followers in data.items():
        for follower in followers:
            G.add_edge(user, follower)

    connected_components = list(nx.connected_components(G))

    cluster_colors = px.colors.qualitative.Plotly
    node_colors = {}
    for i, component in enumerate(connected_components):
        for node in component:
            node_colors[node] = cluster_colors[i % len(cluster_colors)]

    pos = nx.spring_layout(G, k=k, iterations=10000, seed=seed)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []
    hover_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        hover_text.append(f"{node}")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        hovertext=hover_text,
        textfont=dict(size=10),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Social Clusters",
            titlefont_size=32,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=40, l=40, r=40, t=80),
            annotations=[
                dict(
                    text="Hover over a node to see username",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=0.002,
                )
            ],
            xaxis=dict(
                showgrid=False, zeroline=False, showticklabels=False, showline=False
            ),
            yaxis=dict(
                showgrid=False, zeroline=False, showticklabels=False, showline=False
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        ),
    )

    for i, component in enumerate(connected_components):
        cluster_nodes = list(component)
        cluster_x = [pos[node][0] for node in cluster_nodes]
        cluster_y = [pos[node][1] for node in cluster_nodes]
        min_x, max_x = min(cluster_x), max(cluster_x)
        min_y, max_y = min(cluster_y), max(cluster_y)

        fig.add_shape(
            type="rect",
            x0=min_x,
            y0=min_y,
            x1=max_x,
            y1=max_y,
            line=dict(color=cluster_colors[i % len(cluster_colors)], width=2),
        )

    utils.save(fig, "cluster")
    fig.show()


if __name__ == "__main__":
    cluster()
