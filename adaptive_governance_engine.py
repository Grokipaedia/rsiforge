import streamlit as st
import random
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="RSI Forge Governance Engine",
    layout="wide"
)

st.title("RSI Forge — Adaptive Governance Engine")

st.markdown("""
Adaptive recursive governance and coherence stabilization layer.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "governance_state.json"

# -----------------------------------
# LOAD STATE
# -----------------------------------

if os.path.exists(STATE_FILE):

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

else:

    state = {
        "coherence": 85,
        "entropy": 20,
        "synchronization": 80,
        "governance_strength": 88,
        "stability": 90,
        "interventions": 0,
        "events": []
    }

# -----------------------------------
# GOVERNANCE LOGIC
# -----------------------------------

# Entropy pressure
state["entropy"] += random.randint(-2, 4)

# Governance stabilizes entropy
if state["governance_strength"] > 85:
    state["entropy"] -= random.randint(1, 4)

# Synchronization improves coherence
if state["synchronization"] > 85:
    state["coherence"] += random.randint(1, 3)

# Rising entropy reduces stability
if state["entropy"] > 30:
    state["stability"] -= random.randint(1, 4)

# Governance intervention
intervention_triggered = False

if state["entropy"] > 35:

    intervention_triggered = True

    state["interventions"] += 1

    state["entropy"] -= random.randint(4, 8)

    state["stability"] += random.randint(2, 5)

    state["coherence"] += random.randint(1, 3)

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

state["entropy"] = clamp(
    state["entropy"],
    1,
    50
)

state["synchronization"] = clamp(
    state["synchronization"] + random.randint(-2, 3),
    50,
    99
)

state["governance_strength"] = clamp(
    state["governance_strength"] + random.randint(-1, 2),
    70,
    99
)

state["stability"] = clamp(
    state["stability"],
    50,
    99
)

# -----------------------------------
# EVENT ENGINE
# -----------------------------------

events = []

if intervention_triggered:

    events.append(
        "Adaptive governance intervention stabilized recursive coordination."
    )

if state["coherence"] > 92:

    events.append(
        "Collective coherence exceeded governance threshold."
    )

if state["entropy"] < 10:

    events.append(
        "Entropy divergence minimized across recursive layers."
    )

if state["stability"] > 92:

    events.append(
        "Recursive system stability reinforced."
    )

if not events:

    events.append(
        "Governance observability operating within expected parameters."
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
# METRICS
# -----------------------------------

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Governance Strength",
    f"{state['governance_strength']}%"
)

metric2.metric(
    "System Stability",
    f"{state['stability']}%"
)

metric3.metric(
    "Governance Interventions",
    state["interventions"]
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
# GOVERNANCE TREND
# -----------------------------------

st.subheader("Governance Stabilization Trend")

trend_data = pd.DataFrame({
    "Cycle": list(range(1,21)),
    "Stability": [
        clamp(
            state["stability"] + random.randint(-10, 5),
            50,
            99
        )
        for _ in range(20)
    ]
})

trend_fig = px.line(
    trend_data,
    x="Cycle",
    y="Stability",
    markers=True
)

st.plotly_chart(
    trend_fig,
    use_container_width=True
)

# -----------------------------------
# GOVERNANCE LAYERS
# -----------------------------------

st.divider()

st.subheader("Recursive Governance Layers")

layer_data = pd.DataFrame({
    "Layer": [
        "Human Oversight",
        "Memory Validation",
        "Synchronization Control",
        "Entropy Suppression",
        "Recursive Stabilization"
    ],
    "Integrity": [
        random.randint(70,99)
        for _ in range(5)
    ]
})

layer_fig = px.bar(
    layer_data,
    x="Layer",
    y="Integrity"
)

st.plotly_chart(
    layer_fig,
    use_container_width=True
)

# -----------------------------------
# EVENT STREAM
# -----------------------------------

st.divider()

st.subheader("Governance Event Stream")

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
# SYSTEM STATUS
# -----------------------------------

st.divider()

st.subheader("Adaptive Governance State")

st.progress(
    state["stability"] / 100
)

if intervention_triggered:

    st.warning("""
    GOVERNANCE INTERVENTION ACTIVE

    Recursive instability detected and stabilization measures applied.
    """)

elif state["stability"] > 90:

    st.success("""
    SYSTEM STABLE

    Recursive governance operating within optimal parameters.
    """)

else:

    st.error("""
    STABILITY DEGRADATION DETECTED

    Recursive coordination drift increasing.
    """)

# -----------------------------------
# GOVERNANCE STATUS
# -----------------------------------

st.divider()

st.subheader("Governance Layer Status")

statuses = [
    "Adaptive governance operational",
    "Human oversight verified",
    "Recursive stabilization active",
    "Entropy suppression online",
    "Distributed cognition safeguards active",
    "CRI governance observability operational"
]

for status in statuses:
    st.write(f"• {status}")
