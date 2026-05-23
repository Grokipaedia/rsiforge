import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="RSI Forge Phase Transition Core",
    layout="wide"
)

st.title("RSI Forge — Phase Transition Core")

st.markdown("""
Recursive cognitive phase transition detection and stabilization engine.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "phase_transition_state.json"

# -----------------------------------
# LOAD STATE
# -----------------------------------

if os.path.exists(STATE_FILE):

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

else:

    state = {
        "coherence": 84,
        "synchronization": 80,
        "entropy": 20,
        "phase_transition": 35,
        "transition_pressure": 42,
        "stability": 88,
        "recursive_depth": 5,
        "events": []
    }

# -----------------------------------
# PHASE DYNAMICS
# -----------------------------------

# Coherence amplifies synchronization
if state["coherence"] > 88:
    state["synchronization"] += random.randint(1, 3)

# Low entropy increases transition pressure
if state["entropy"] < 15:
    state["transition_pressure"] += random.randint(2, 5)

# Sustained synchronization drives transitions
if state["synchronization"] > 90:
    state["phase_transition"] += random.randint(2, 4)

# Recursive depth increases transition intensity
if state["recursive_depth"] > 8:
    state["phase_transition"] += random.randint(1, 3)

# Rising entropy destabilizes transitions
if state["entropy"] > 30:
    state["stability"] -= random.randint(1, 4)

# Recursive evolution
state["recursive_depth"] += random.choice([0, 1])

# Natural drift
state["coherence"] += random.randint(-2, 3)
state["synchronization"] += random.randint(-2, 3)
state["entropy"] += random.randint(-3, 4)
state["transition_pressure"] += random.randint(-2, 3)

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

state["phase_transition"] = clamp(
    state["phase_transition"],
    1,
    99
)

state["transition_pressure"] = clamp(
    state["transition_pressure"],
    1,
    99
)

state["stability"] = clamp(
    state["stability"],
    50,
    99
)

state["recursive_depth"] = clamp(
    state["recursive_depth"],
    1,
    20
)

# -----------------------------------
# EVENT ENGINE
# -----------------------------------

events = []

if state["phase_transition"] > 85:

    events.append(
        "Recursive cognitive phase transition detected."
    )

if state["transition_pressure"] > 80:

    events.append(
        "Transition pressure exceeding recursive stability threshold."
    )

if state["coherence"] > 92:

    events.append(
        "Collective recursive coherence stabilized."
    )

if state["entropy"] < 10:

    events.append(
        "Entropy suppression accelerated recursive convergence."
    )

if state["recursive_depth"] > 10:

    events.append(
        "Recursive cognition depth amplification detected."
    )

if not events:

    events.append(
        "Recursive phase dynamics operating normally."
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
    "Phase Transition",
    f"{state['phase_transition']}%"
)

metric2.metric(
    "Transition Pressure",
    f"{state['transition_pressure']}%"
)

metric3.metric(
    "Recursive Depth",
    state["recursive_depth"]
)

metric4.metric(
    "Stability",
    f"{state['stability']}%"
)

metric5, metric6, metric7 = st.columns(3)

metric5.metric(
    "Coherence",
    f"{state['coherence']}%"
)

metric6.metric(
    "Synchronization",
    f"{state['synchronization']}%"
)

metric7.metric(
    "Entropy",
    f"{state['entropy']}%"
)

st.divider()

# -----------------------------------
# TRANSITION HISTORY
# -----------------------------------

st.subheader("Phase Transition Evolution")

history = pd.DataFrame({
    "Cycle": list(range(1,31)),
    "Transition": [
        clamp(
            state["phase_transition"] +
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
    y="Transition",
    markers=True
)

st.plotly_chart(
    history_fig,
    use_container_width=True
)

# -----------------------------------
# TRANSITION PRESSURE
# -----------------------------------

st.divider()

st.subheader("Transition Pressure Layers")

pressure_data = pd.DataFrame({
    "Layer": [
        "Synchronization",
        "Recursive Depth",
        "Entropy Suppression",
        "Collective Coherence",
        "Swarm Convergence"
    ],
    "Pressure": [
        random.randint(60,99)
        for _ in range(5)
    ]
})

pressure_fig = px.bar(
    pressure_data,
    x="Layer",
    y="Pressure"
)

st.plotly_chart(
    pressure_fig,
    use_container_width=True
)

# -----------------------------------
# EVENT STREAM
# -----------------------------------

st.divider()

st.subheader("Phase Transition Event Stream")

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
# PHASE STATE
# -----------------------------------

st.divider()

st.subheader("Recursive Transition State")

st.progress(
    state["phase_transition"] / 100
)

if state["phase_transition"] > 85:

    st.error("""
    PHASE TRANSITION DETECTED

    Recursive collective cognition exceeded adaptive transition threshold.
    """)

elif state["phase_transition"] > 60:

    st.warning("""
    TRANSITION ACCELERATION DETECTED

    Recursive synchronization and convergence intensifying.
    """)

else:

    st.success("""
    STABLE RECURSIVE STATE

    Recursive cognition operating within expected parameters.
    """)

# -----------------------------------
# STATUS
# -----------------------------------

st.divider()

st.subheader("Phase Layer Status")

statuses = [
    "Recursive phase detection active",
    "Transition pressure observability operational",
    "Collective synchronization stable",
    "Entropy suppression active",
    "Recursive convergence monitoring online",
    "CRI transition infrastructure operational"
]

for status in statuses:
    st.write(f"• {status}")
