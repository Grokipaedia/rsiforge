import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import random
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="RSI Forge Network Observatory",
    layout="wide"
)

st.title("RSI Forge — Recursive Network Observatory")

st.markdown("""
Distributed Collective Recursive Intelligence network observability system.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "network_state.json"

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
        "events": []
    }

# -----------------------------------
# UPDATE STATE
# -----------------------------------

state["coherence"] = min(
    99,
    max(
        60,
        state["coherence"] + random.randint(-3, 4)
    )
)

state["synchronization"] = min(
    99,
    max(
        50,
        state["synchronization"] + random.randint(-4, 5)
    )
)

state["entropy"] = min(
    50,
    max(
        1,
        state["entropy"] + random.randint(-2, 3)
    )
)

state["phase_transition"] = min(
    99,
    max(
        1,
        state["phase_transition"] + random.randint(-5, 6)
    )
)

# -----------------------------------
# SAVE EVENT
# -----------------------------------

events = [
    "Recursive synchronization updated.",
    "Distributed cognition pathway reinforced.",
    "Human coherence anchor stabilized network.",
    "Governance checkpoint verified.",
    "Entropy divergence reduced.",
    "Recursive memory propagation increased.",
    "Swarm topology reorganized.",
    "Consensus reinforcement detected.",
    "Phase transition threshold fluctuating.",
    "CRI observability synchronization active."
]

new_event = {
    "timestamp": datetime.utcnow().strftime("%H:%M:%S"),
    "event": random.choice(events)
}

state["events"].insert(0, new_event)

state["events"] = state["events"][:25]

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

st.divider()

# -----------------------------------
# NETWORK GRAPH
# -----------------------------------

st.subheader("Recursive Intelligence Network")

G = nx.gnm_random_graph(20, 32)

pos = nx.spring_layout(G, seed=42)

# -----------------------------------
# EDGE TRACE
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
# NODE TRACE
# -----------------------------------

node_x = []
node_y = []
node_text = []
node_size = []

for node in G.nodes():

    x, y = pos[node]

    node_x.append(x)
    node_y.append(y)

    coherence = random.randint(70,99)

    node_size.append(coherence)

    node_text.append(
        f"""
        Recursive Node: {node}
        <br>Coherence: {coherence}%
        <br>Synchronization: {random.randint(60,99)}%
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
    "Cycle": list(range(1,21)),
    "Coherence": [
        random.randint(70,99)
        for _ in range(20)
    ]
})

history_chart = go.Figure()

history_chart.add_scatter(
    x=history["Cycle"],
    y=history["Coherence"],
    mode="lines+markers"
)

st.plotly_chart(
    history_chart,
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

    Distributed recursive coordination operating normally.
    """)

# -----------------------------------
# NETWORK STATUS
# -----------------------------------

st.divider()

st.subheader("Recursive Network Layers")

statuses = [
    "Distributed cognition active",
    "Recursive memory synchronization online",
    "Human coherence anchor verified",
    "Governance observability stable",
    "Recursive intelligence propagation operational",
    "CRI network continuity maintained"
]

for status in statuses:
    st.write(f"• {status}")
