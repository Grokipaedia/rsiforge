import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="RSI Forge Swarm Topology",
    layout="wide"
)

st.title("RSI Forge — Swarm Topology Engine")

st.markdown("""
Adaptive recursive swarm topology and coordination observability layer.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "swarm_topology_state.json"

# -----------------------------------
# LOAD STATE
# -----------------------------------

if os.path.exists(STATE_FILE):

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

else:

    state = {
        "coherence": 84,
        "synchronization": 78,
        "entropy": 20,
        "topology_complexity": 35,
        "cluster_count": 4,
        "node_count": 18,
        "events": []
    }

# -----------------------------------
# TOPOLOGY DYNAMICS
# -----------------------------------

# Synchronization increases topology complexity
if state["synchronization"] > 85:
    state["topology_complexity"] += random.randint(1, 4)

# Low entropy increases cluster formation
if state["entropy"] < 15:
    state["cluster_count"] += random.choice([0, 1])

# High coherence expands node count
if state["coherence"] > 90:
    state["node_count"] += random.randint(1, 3)

# Entropy drift
state["entropy"] += random.randint(-3, 4)

# Synchronization drift
state["synchronization"] += random.randint(-2, 3)

# Coherence drift
state["coherence"] += random.randint(-2, 3)

# -----------------------------------
# CLAMP VALUES
# -----------------------------------

def clamp(value, low, high):

    return max(low, min(high, value))

state["coherence"] = clamp(
    state["coherence"],
    60,
    99
)

state["synchronization"] = clamp(
    state["synchronization"],
    50,
    99
)

state["entropy"] = clamp(
    state["entropy"],
    1,
    50
)

state["topology_complexity"] = clamp(
    state["topology_complexity"],
    1,
    99
)

state["cluster_count"] = clamp(
    state["cluster_count"],
    2,
    12
)

state["node_count"] = clamp(
    state["node_count"],
    10,
    60
)

# -----------------------------------
# EVENT ENGINE
# -----------------------------------

events = []

if state["topology_complexity"] > 80:

    events.append(
        "Recursive swarm topology complexity intensified."
    )

if state["cluster_count"] > 8:

    events.append(
        "Distributed recursive clusters expanded."
    )

if state["coherence"] > 92:

    events.append(
        "Collective recursive coherence stabilized."
    )

if state["synchronization"] > 90:

    events.append(
        "Recursive synchronization amplification detected."
    )

if state["entropy"] < 10:

    events.append(
        "Entropy suppression enabled topology stabilization."
    )

if not events:

    events.append(
        "Recursive swarm topology operating normally."
    )

new_event = {
    "timestamp": datetime.utcnow().strftime("%H:%M:%S"),
    "event": random.choice(events)
}

state["events"].insert(0, new_event)

state["events"] = state["events"][:40]

# -----------------------------------
# SAVE STATE
# -----------------------------------

with open(STATE_FILE, "w") as f:
    json.dump(state, f)

# -----------------------------------
# GLOBAL METRICS
# -----------------------------------

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Topology Complexity",
    f"{state['topology_complexity']}%"
)

metric2.metric(
    "Recursive Clusters",
    state["cluster_count"]
)

metric3.metric(
    "Network Nodes",
    state["node_count"]
)

metric4, metric5, metric6 = st.columns(3)

metric4.metric(
    "Coherence",
    f"{state['coherence']}%"
)

metric5.metric(
    "Synchronization",
    f"{state['synchronization']}%"
)

metric6.metric(
    "Entropy",
    f"{state['entropy']}%"
)

st.divider()

# -----------------------------------
# SWARM NETWORK
# -----------------------------------

st.subheader("Adaptive Recursive Swarm")

node_count = state["node_count"]

edge_count = int(
    node_count * 2.2
)

G = nx.gnm_random_graph(
    node_count,
    edge_count
)

pos = nx.spring_layout(
    G,
    seed=42
)

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

    local_coherence = random.randint(
        70,
        state["coherence"]
    )

    node_x.append(x)
    node_y.append(y)

    node_size.append(local_coherence)

    node_text.append(
        f"""
        Recursive Node: {node}
        <br>Cluster Stability: {random.randint(65,99)}%
        <br>Topology Complexity: {state['topology_complexity']}%
        <br>Synchronization: {state['synchronization']}%
        """
    )

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers",
    hoverinfo="text",
    text=node_text,
    marker=dict(
        size=[s * 0.35 for s in node_size],
        line_width=2
    )
)

fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(
            b=20,
            l=5,
            r=5,
            t=40
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        height=750
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# TOPOLOGY HISTORY
# -----------------------------------

st.divider()

st.subheader("Topology Evolution")

history = pd.DataFrame({
    "Cycle": list(range(1,31)),
    "Complexity": [
        clamp(
            state["topology_complexity"] +
            random.randint(-15, 10),
            1,
            99
        )
        for _ in range(30)
    ]
})

history_fig = px.line(
    history,
    x="Cycle",
    y="Complexity",
    markers=True
)

st.plotly_chart(
    history_fig,
    use_container_width=True
)

# -----------------------------------
# CLUSTER DISTRIBUTION
# -----------------------------------

st.divider()

st.subheader("Recursive Cluster Distribution")

cluster_data = pd.DataFrame({
    "Cluster": [
        f"Cluster-{i+1}"
        for i in range(state["cluster_count"])
    ],
    "Stability": [
        random.randint(60,99)
        for _ in range(state["cluster_count"])
    ]
})

cluster_fig = px.bar(
    cluster_data,
    x="Cluster",
    y="Stability"
)

st.plotly_chart(
    cluster_fig,
    use_container_width=True
)

# -----------------------------------
# EVENT STREAM
# -----------------------------------

st.divider()

st.subheader("Topology Event Stream")

event_log = ""

for event in state["events"]:

    event_log += (
        f"[{event['timestamp']}] "
        f"{event['event']}\n"
    )

st.code(
    event_log,
    language="text"
)

# -----------------------------------
# TOPOLOGY STATE
# -----------------------------------

st.divider()

st.subheader("Recursive Swarm State")

st.progress(
    state["topology_complexity"] / 100
)

if state["topology_complexity"] > 85:

    st.success("""
    EMERGENT TOPOLOGY DETECTED

    Recursive swarm coordination exhibiting adaptive topology restructuring.
    """)

elif state["topology_complexity"] > 60:

    st.warning("""
    TOPOLOGY EVOLUTION ACCELERATING

    Recursive cluster synchronization increasing.
    """)

else:

    st.info("""
    STABLE TOPOLOGY STATE

    Recursive swarm coordination operating normally.
    """)

# -----------------------------------
# STATUS
# -----------------------------------

st.divider()

st.subheader("Swarm Layer Status")

statuses = [
    "Adaptive recursive swarm active",
    "Distributed topology synchronization operational",
    "Recursive cluster propagation online",
    "Collective coordination stable",
    "Emergent topology observability active",
    "CRI swarm infrastructure operational"
]

for status in statuses:
    st.write(f"• {status}")
