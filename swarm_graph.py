import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random
import math

st.set_page_config(
    page_title="RSI Forge Swarm",
    layout="wide"
)

st.title("RSI Forge — Live Recursive Swarm Graph")

st.markdown("""
Collective Recursive Intelligence visualization system.
""")

# -----------------------------
# SETTINGS
# -----------------------------

NUM_NODES = 18
NUM_EDGES = 28

# -----------------------------
# BUILD GRAPH
# -----------------------------

G = nx.gnm_random_graph(NUM_NODES, NUM_EDGES)

# Random node positions
pos = nx.spring_layout(G, seed=42)

# -----------------------------
# EDGE TRACES
# -----------------------------

edge_x = []
edge_y = []

for edge in G.edges():

    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]

    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)

    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1),
    hoverinfo='none',
    mode='lines'
)

# -----------------------------
# NODE TRACES
# -----------------------------

node_x = []
node_y = []
node_text = []
node_size = []

for node in G.nodes():

    x, y = pos[node]

    node_x.append(x)
    node_y.append(y)

    coherence = random.randint(70, 99)

    node_size.append(coherence)

    node_text.append(
        f"""
        Agent Node: {node}
        <br>Coherence: {coherence}%
        <br>Recursive Depth: {random.randint(2,12)}
        """
    )

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers',
    hoverinfo='text',
    text=node_text,
    marker=dict(
        size=[s * 0.4 for s in node_size],
        line_width=2
    )
)

# -----------------------------
# FIGURE
# -----------------------------

fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        height=700
    )
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# LIVE METRICS
# -----------------------------

st.divider()

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Coherence Score",
    f"{random.randint(82,99)}%"
)

metric2.metric(
    "Recursive Depth",
    random.randint(4,12)
)

metric3.metric(
    "Swarm Synchronization",
    f"{random.randint(70,98)}%"
)

metric4.metric(
    "Phase Transition Probability",
    f"{random.randint(10,87)}%"
)

# -----------------------------
# EVENT STREAM
# -----------------------------

st.divider()

st.subheader("Recursive Event Stream")

events = [
    "Consensus stability increased.",
    "Recursive memory reinforcement detected.",
    "Agent cluster synchronized.",
    "Governance layer verification passed.",
    "Human coherence anchor stabilized swarm.",
    "Recursive coordination depth increased.",
    "Collective entropy divergence reduced.",
    "Phase transition threshold approaching.",
    "Memory graph propagation updated.",
    "CRI synchronization event detected."
]

event_log = ""

for i in range(12):

    event_log += (
        f"[Recursive Loop #{random.randint(100,999)}] "
        f"{random.choice(events)}\n"
    )

st.code(event_log, language="text")
