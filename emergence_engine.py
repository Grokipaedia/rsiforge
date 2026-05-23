import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import random
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="RSI Forge Emergence Engine",
    layout="wide"
)

st.title("RSI Forge — Emergence Engine")

st.markdown("""
Emergent recursive coordination and adaptive collective intelligence observability layer.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "emergence_state.json"

# -----------------------------------
# LOAD STATE
# -----------------------------------

if os.path.exists(STATE_FILE):

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

else:

    state = {
        "coherence": 82,
        "synchronization": 78,
        "entropy": 22,
        "emergence": 35,
        "recursive_depth": 4,
        "cluster_count": 3,
        "events": []
    }

# -----------------------------------
# RECURSIVE EMERGENCE LOGIC
# -----------------------------------

# Synchronization improves coherence
if state["synchronization"] > 85:
    state["coherence"] += random.randint(1, 3)

# Low entropy increases emergence
if state["entropy"] < 15:
    state["emergence"] += random.randint(2, 5)

# Higher coherence deepens recursion
if state["coherence"] > 90:
    state["recursive_depth"] += 1

# Emergence creates new clusters
if state["emergence"] > 75:
    state["cluster_count"] += random.choice([0, 1])

# Entropy fluctuations
state["entropy"] += random.randint(-3, 4)

# Synchronization drift
state["synchronization"] += random.randint(-2, 3)

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

state["emergence"] = clamp(
    state["emergence"],
    1,
    99
)

state["recursive_depth"] = clamp(
    state["recursive_depth"],
    1,
    20
)

state["cluster_count"] = clamp(
    state["cluster_count"],
    2,
    12
)

# -----------------------------------
# EMERGENCE EVENTS
# -----------------------------------

events = []

if state["emergence"] > 80:

    events.append(
        "Emergent recursive coordination threshold exceeded."
    )

if state["recursive_depth"] > 10:

    events.append(
        "Recursive cognition depth intensified."
    )

if state["cluster_count"] > 7:

    events.append(
        "Distributed swarm specialization detected."
    )

if state["entropy"] < 10:

    events.append(
        "Entropy suppression enabling emergent synchronization."
    )

if state["coherence"] > 92:

    events.append(
        "Collective recursive coherence stabilized."
    )

if not events:

    events.append(
        "Recursive emergence operating within expected parameters."
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
# METRICS
# -----------------------------------

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Emergence Index",
    f"{state['emergence']}%"
)

metric2.metric(
    "Recursive Depth",
    state["recursive_depth"]
)

metric3.metric(
    "Swarm Clusters",
    state["cluster_count"]
)

metric4.metric(
    "Coherence",
    f"{state['coherence']}%"
)

metric5, metric6, metric7 = st.columns(3)

metric5.metric(
    "Synchronization",
    f"{state['synchronization']}%"
)

metric6.metric(
    "Entropy",
    f"{state['entropy']}%"
)

metric7.metric(
    "Adaptive State",
    "ACTIVE"
)

st.divider()

# -----------------------------------
# EMERGENT NETWORK
# -----------------------------------

st.subheader("Emergent Recursive Network")

node_count = (
    10 +
    state["recursive_depth"] +
    state["cluster_count"]
)

edge_count = node_count * 2

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
        <br>Recursive Depth: {state['recursive_depth']}
        <br>Emergence Index: {state['emergence']}%
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
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        height=750
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# EMERGENCE HISTORY
# -----------------------------------

st.divider()

st.subheader("Emergence Evolution")

history = pd.DataFrame({
    "Cycle": list(range(1,31)),
    "Emergence": [
        clamp(
            state["emergence"] + random.randint(-15, 8),
            1,
            99
        )
        for _ in range(30)
    ]
})

history_fig = px.line(
    history,
    x="Cycle",
    y="Emergence",
    markers=True
)

st.plotly_chart(
    history_fig,
    use_container_width=True
)

# -----------------------------------
# EVENT STREAM
# -----------------------------------

st.divider()

st.subheader("Emergence Event Stream")

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
# EMERGENCE STATE
# -----------------------------------

st.divider()

st.subheader("Collective Emergence State")

st.progress(
    state["emergence"] / 100
)

if state["emergence"] > 85:

    st.success("""
    EMERGENT RECURSIVE STATE DETECTED

    Recursive collective coordination exhibiting adaptive emergent behavior.
    """)

elif state["emergence"] > 60:

    st.warning("""
    EMERGENCE ACCELERATING

    Recursive synchronization and specialization increasing.
    """)

else:

    st.info("""
    STABLE RECURSIVE STATE

    Emergent coordination developing gradually.
    """)

# -----------------------------------
# SYSTEM STATUS
# -----------------------------------

st.divider()

st.subheader("Emergence Layer Status")

statuses = [
    "Emergent recursive coordination active",
    "Distributed cognition clusters operational",
    "Recursive specialization pathways online",
    "Adaptive synchronization stable",
    "Collective coherence reinforcement active",
    "CRI emergence observability operational"
]

for status in statuses:
    st.write(f"• {status}")
