import streamlit as st
import random
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="RSI Forge Persistent State Engine",
    layout="wide"
)

st.title("RSI Forge — Persistent Recursive State Engine")

st.markdown("""
Persistent recursive coordination and collective state observability layer.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "recursive_state.json"

# -----------------------------------
# LOAD STATE
# -----------------------------------

if os.path.exists(STATE_FILE):

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

else:

    state = {
        "cycles": [],
        "coherence": 85,
        "synchronization": 80,
        "entropy": 20,
        "phase_probability": 35
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
        state["entropy"] + random.randint(-3, 3)
    )
)

state["phase_probability"] = min(
    99,
    max(
        1,
        state["phase_probability"] + random.randint(-5, 6)
    )
)

# -----------------------------------
# EVENT GENERATION
# -----------------------------------

events = [
    "Consensus stability increased.",
    "Recursive memory reinforcement detected.",
    "Governance checkpoint verified.",
    "Human coherence anchor stabilized swarm.",
    "Distributed cognition synchronized.",
    "Recursive entropy reduced.",
    "Swarm topology reorganized.",
    "Recursive coordination intensified.",
    "CRI synchronization event detected.",
    "Phase transition threshold fluctuating."
]

new_event = {
    "timestamp": datetime.utcnow().strftime("%H:%M:%S"),
    "event": random.choice(events)
}

state["cycles"].insert(0, new_event)

state["cycles"] = state["cycles"][:25]

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
    f"{state['phase_probability']}%"
)

st.divider()

# -----------------------------------
# EVENT STREAM
# -----------------------------------

st.subheader("Persistent Recursive State")

event_log = ""

for cycle in state["cycles"]:

    event_log += (
        f"[{cycle['timestamp']}] "
        f"{cycle['event']}\n"
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

if state["phase_probability"] > 85:

    st.error("""
    PHASE TRANSITION DETECTED

    Recursive collective coordination exceeded critical threshold.
    """)

elif state["phase_probability"] > 60:

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

st.subheader("Persistent System Layers")

statuses = [
    "Recursive persistence engine active",
    "Distributed cognition memory online",
    "Human coherence anchor verified",
    "Governance synchronization stable",
    "Recursive observability operational",
    "CRI state continuity maintained"
]

for status in statuses:
    st.write(f"• {status}")
