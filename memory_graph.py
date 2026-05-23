import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random

st.set_page_config(
    page_title="RSI Forge Memory Graph",
    layout="wide"
)

st.title("RSI Forge — Recursive Memory Graph")

st.markdown("""
Recursive memory propagation and reinforcement visualization.
""")

# -----------------------------------
# MEMORY NODES
# -----------------------------------

memory_nodes = [
    "Human Anchor",
    "Recursive Loop",
    "Governance Layer",
    "Swarm Cluster",
    "Memory Reinforcement",
    "Consensus Engine",
    "Phase Transition",
    "Coordination Layer",
    "Entropy Reduction",
    "CRI Synchronization"
]

# -----------------------------------
# BUILD GRAPH
# -----------------------------------

G = nx.Graph()

for node in memory_nodes:
    G.add_node(node)

for i in range(len(memory_nodes) * 2):

    a = random.choice(memory_nodes)
    b = random.choice(memory_nodes)

    if a != b:
        G.add_edge(a, b)

# -----------------------------------
# LAYOUT
# -----------------------------------

pos = nx.spring_layout(G, seed=42)

# -----------------------------------
# EDGES
# -----------------------------------

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
    mode="lines",
    hoverinfo="none"
)

# -----------------------------------
# NODES
# -----------------------------------

node_x = []
node_y = []
node_text = []
node_size = []

for node in G.nodes():

    x, y = pos[node]

    reinforcement = random.randint(60, 99)

    node_x.append(x)
    node_y.append(y)

    node_size.append(reinforcement)

    node_text.append(
        f"""
        {node}
        <br>Memory Reinforcement: {reinforcement}%
        """
    )

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=list(G.nodes()),
    textposition="top center",
    hoverinfo="text",
    hovertext=node_text,
    marker=dict(
        size=[s * 0.45 for s in node_size],
        line_width=2
    )
)

# -----------------------------------
# FIGURE
# -----------------------------------

fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        height=700
    )
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# METRICS
# -----------------------------------

st.divider()

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Memory Reinforcement",
    f"{random.randint(72,99)}%"
)

metric2.metric(
    "Recursive Recall Depth",
    random.randint(3,11)
)

metric3.metric(
    "Synchronization Stability",
    f"{random.randint(68,97)}%"
)

# -----------------------------------
# EVENT STREAM
# -----------------------------------

st.divider()

st.subheader("Memory Propagation Events")

events = [
    "Recursive memory reinforced.",
    "Swarm synchronization updated.",
    "Human anchor stabilized recall path.",
    "Consensus memory cluster formed.",
    "Governance memory checkpoint verified.",
    "Entropy divergence reduced.",
    "Phase transition memory threshold approaching.",
    "Recursive memory propagation increased."
]

event_log = ""

for i in range(12):

    event_log += (
        f"[Memory Event #{random.randint(100,999)}] "
        f"{random.choice(events)}\n"
    )

st.code(event_log, language="text")
