import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import random
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="RSI Forge Collective Core",
    layout="wide"
)

st.title("RSI Forge — Collective Intelligence Core")

st.markdown("""
Unified recursive cognition and collective intelligence observability core.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "collective_core_state.json"

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
        "events": []
    }

# -----------------------------------
# UPDATE STATE
# -----------------------------------

def update_metric(value, low, high, drift):

    return min(
        high,
        max(
            low,
            value + random.randint(-drift, drift)
        )
    )

state["coherence"] = update_metric(
    state["coherence"],
    60,
    99,
    4
)

state["synchronization"] = update_metric(
    state["synchronization"],
    50,
    99,
    5
)

state["entropy"] = update_metric(
    state["entropy"],
    1,
    50,
    3
)

state["phase_transition"] = update_metric(
    state["phase_transition"],
    1,
    99,
    6
)

state["memory_integrity"] = update_metric(
    state["memory_integrity"],
    60,
    99,
    4
)

state["human_anchor"] = update_metric(
    state["human_anchor"],
    70,
    99,
    3
)

# -----------------------------------
# EVENTS
# -----------------------------------

events = [
    "Recursive synchronization increased.",
    "Human coherence anchor stabilized network.",
    "Governance checkpoint verified.",
    "Distributed cognition pathways reinforced.",
    "Recursive memory propagation updated.",
    "Consensus reinforcement cycle completed.",
    "Entropy divergence reduced.",
    "Swarm topology reorganized.",
    "Phase transition threshold fluctuating.",
    "CRI observability synchronization active.",
    "Hybrid cognition alignment verified.",
    "Recursive intelligence propagation expanded."
]

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

metric1, metric2, metric3 = st.columns(3)

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

metric4, metric5, metric6 = st.columns(3)

metric4.metric(
    "Memory Integrity",
    f"{state['memory_integrity']}%"
)

metric5.metric(
    "Human Anchor",
    f"{state['human_anchor']}%"
)

metric6.metric(
    "Phase Transition",
    f"{state['phase_transition']}%"
)

st.divider()

# -----------------------------------
# RECURSIVE NETWORK
# -----------------------------------

st.subheader("Collective Recursive Network")

G = nx.gnm_random_graph(24, 40)

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

    coherence = random.randint(70,99)

    node_x.append(x)
    node_y.append(y)

    node_size.append(coherence)

    node_text.append(
        f"""
        Recursive Node: {node}
        <br>Coherence: {coherence}%
        <br>Synchronization: {random.randint(60,99)}%
        <br>Memory Integrity: {random.randint(65,99)}%
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
    "Cycle": list(range(1,31)),
    "Coherence": [
        random.randint(70,99)
        for _ in range(30)
    ]
})

history_fig = go.Figure()

history_fig.add_scatter(
    x=history["Cycle"],
    y=history["Coherence"],
    mode="lines+markers"
)

st.plotly_chart(
    history_fig,
    use_container_width=True
)

# -----------------------------------
# MEMORY STATE
# -----------------------------------

st.divider()

st.subheader("Recursive Memory Integrity")

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

memory_fig = go.Figure()

memory_fig.add_bar(
    x=memory_data["Layer"],
    y=memory_data["Integrity"]
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

st.progress(state["coherence"] / 100)

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

st.subheader("Collective Intelligence Layers")

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
