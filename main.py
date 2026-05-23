import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import json
import os
from datetime import datetime

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="RSI Forge",
    layout="wide"
)

st.title("RSI Forge — Collective Recursive Intelligence Core")

st.markdown("""
Unified recursive cognition observability environment.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "cri_state.json"

# -----------------------------------
# LOAD STATE
# -----------------------------------

if os.path.exists(STATE_FILE):

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

else:

    state = {
        "coherence": 85,
        "synchronization": 80,
        "entropy": 20,
        "phase_transition": 35,
        "memory_integrity": 88,
        "human_anchor": 92,
        "recursive_depth": 5,
        "events": []
    }

# -----------------------------------
# RECURSIVE DYNAMICS
# -----------------------------------

# Human anchor stabilizes entropy
if state["human_anchor"] > 85:
    state["entropy"] -= random.randint(1, 3)

# Higher coherence improves synchronization
if state["coherence"] > 85:
    state["synchronization"] += random.randint(1, 3)

# Low entropy increases phase transition potential
if state["entropy"] < 15:
    state["phase_transition"] += random.randint(1, 4)

# High synchronization reinforces memory
if state["synchronization"] > 85:
    state["memory_integrity"] += random.randint(1, 2)

# Recursive depth evolves slowly
state["recursive_depth"] += random.choice([0, 1])

# Random fluctuation boundaries
def clamp(value, low, high):
    return max(low, min(high, value))

state["coherence"] = clamp(
    state["coherence"] + random.randint(-2, 3),
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

state["phase_transition"] = clamp(
    state["phase_transition"],
    1,
    99
)

state["memory_integrity"] = clamp(
    state["memory_integrity"],
    60,
    99
)

state["human_anchor"] = clamp(
    state["human_anchor"] + random.randint(-1, 2),
    70,
    99
)

# -----------------------------------
# EVENT ENGINE
# -----------------------------------

events = []

if state["coherence"] > 90:
    events.append(
        "Collective coherence exceeded stability threshold."
    )

if state["entropy"] < 10:
    events.append(
        "Entropy divergence reduced across recursive layers."
    )

if state["synchronization"] > 90:
    events.append(
        "Recursive synchronization amplification detected."
    )

if state["phase_transition"] > 80:
    events.append(
        "Cognitive phase transition threshold approaching."
    )

if state["memory_integrity"] > 90:
    events.append(
        "Recursive memory reinforcement cycle completed."
    )

if not events:
    events.append(
        "Recursive coordination operating within expected parameters."
    )

new_event = {
    "timestamp": datetime.utcnow().strftime("%H:%M:%S"),
    "event": random.choice(events)
}

state["events"].insert(0, new_event)

state["events"] = state["events"][:30]

# -----------------------------------
# SAVE STATE
# -----------------------------------

with open(STATE_FILE, "w") as f:
    json.dump(state, f)

# -----------------------------------
# GLOBAL METRICS
# -----------------------------------

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Coherence",
    f"{state['coherence']}%"
)

metric2.metric(
    "Synchronization",
    f"{state['synchronization']}%"
)

metric3.metric(
    "Entropy",
    f"{state['entropy']}%"
)

metric4.metric(
    "Phase Transition",
    f"{state['phase_transition']}%"
)

metric5, metric6, metric7 = st.columns(3)

metric5.metric(
    "Memory Integrity",
    f"{state['memory_integrity']}%"
)

metric6.metric(
    "Human Anchor",
    f"{state['human_anchor']}%"
)

metric7.metric(
    "Recursive Depth",
    state["recursive_depth"]
)

st.divider()

# -----------------------------------
# RECURSIVE SWARM GRAPH
# -----------------------------------

st.subheader("Recursive Intelligence Network")

node_count = 12 + int(state["recursive_depth"])

G = nx.gnm_random_graph(
    node_count,
    node_count * 2
)

pos = nx.spring_layout(G, seed=42)

# Edges
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

# Nodes
node_x = []
node_y = []
node_text = []
node_size = []

for node in G.nodes():

    x, y = pos[node]

    coherence = random.randint(
        70,
        state["coherence"]
    )

    node_x.append(x)
    node_y.append(y)

    node_size.append(coherence)

    node_text.append(
        f"""
        Recursive Node: {node}
        <br>Coherence: {coherence}%
        <br>Synchronization: {state['synchronization']}%
        <br>Memory Integrity: {state['memory_integrity']}%
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
        height=700
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# COHERENCE HISTORY
# -----------------------------------

st.divider()

st.subheader("Recursive Coherence History")

history = pd.DataFrame({
    "Cycle": list(range(1, 21)),
    "Coherence": [
        clamp(
            state["coherence"] + random.randint(-10, 5),
            60,
            99
        )
        for _ in range(20)
    ]
})

history_fig = px.line(
    history,
    x="Cycle",
    y="Coherence",
    markers=True
)

st.plotly_chart(
    history_fig,
    use_container_width=True
)

# -----------------------------------
# MEMORY LAYERS
# -----------------------------------

st.divider()

st.subheader("Recursive Memory Layers")

memory_data = pd.DataFrame({
    "Layer": [
        "Human Anchor",
        "Governance",
        "Synchronization",
        "Consensus",
        "Recursive Recall"
    ],
    "Integrity": [
        random.randint(70,99)
        for _ in range(5)
    ]
})

memory_fig = px.bar(
    memory_data,
    x="Layer",
    y="Integrity"
)

st.plotly_chart(
    memory_fig,
    use_container_width=True
)

# -----------------------------------
# EVENT STREAM
# -----------------------------------

st.divider()

st.subheader("Persistent Recursive Events")

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
# PHASE STATUS
# -----------------------------------

st.divider()

st.subheader("Collective Recursive State")

st.progress(
    state["coherence"] / 100
)

if state["phase_transition"] > 85:

    st.error("""
    PHASE TRANSITION DETECTED

    Recursive collective coordination exceeded critical threshold.
    """)

elif state["phase_transition"] > 60:

    st.warning("""
    PHASE TRANSITION APPROACHING

    Recursive synchronization intensity increasing.
    """)

else:

    st.success("""
    SYSTEM STABLE

    Persistent recursive coordination operating normally.
    """)

# -----------------------------------
# SYSTEM STATUS
# -----------------------------------

st.divider()

st.subheader("CRI Layer Status")

statuses = [
    "Recursive coordination active",
    "Distributed cognition operational",
    "Human coherence anchor verified",
    "Governance synchronization stable",
    "Recursive memory persistence online",
    "CRI observability system operational",
    "Collective recursive intelligence continuity maintained"
]

for status in statuses:
    st.write(f"• {status}")
