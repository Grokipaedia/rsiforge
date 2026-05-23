import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="RSI Forge Agent Matrix",
    layout="wide"
)

st.title("RSI Forge — Recursive Agent Matrix")

st.markdown("""
Adaptive multi-agent recursive coordination and specialization observability layer.
""")

# -----------------------------------
# STATE FILE
# -----------------------------------

STATE_FILE = "agent_matrix_state.json"

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
        "entropy": 18,
        "specialization": 42,
        "agents": [],
        "events": []
    }

# -----------------------------------
# INITIAL AGENTS
# -----------------------------------

if not state["agents"]:

    roles = [
        "Coordinator",
        "Memory",
        "Governance",
        "Synchronization",
        "Consensus",
        "Entropy Control",
        "Recursive Analysis",
        "Human Interface"
    ]

    for i in range(8):

        state["agents"].append({
            "id": i,
            "role": roles[i],
            "coherence": random.randint(70,99),
            "stability": random.randint(70,99),
            "specialization": random.randint(40,90)
        })

# -----------------------------------
# AGENT DYNAMICS
# -----------------------------------

for agent in state["agents"]:

    # Synchronization influences coherence
    if state["synchronization"] > 85:
        agent["coherence"] += random.randint(0, 2)

    # Entropy affects stability
    if state["entropy"] > 25:
        agent["stability"] -= random.randint(1, 3)

    # Specialization evolves
    if agent["coherence"] > 90:
        agent["specialization"] += random.randint(1, 2)

    # Clamp values
    agent["coherence"] = max(
        60,
        min(99, agent["coherence"])
    )

    agent["stability"] = max(
        50,
        min(99, agent["stability"])
    )

    agent["specialization"] = max(
        1,
        min(99, agent["specialization"])
    )

# -----------------------------------
# GLOBAL STATE EVOLUTION
# -----------------------------------

state["coherence"] += random.randint(-2, 3)
state["synchronization"] += random.randint(-2, 3)
state["entropy"] += random.randint(-3, 4)
state["specialization"] += random.randint(-1, 3)

# Clamp
state["coherence"] = max(60, min(99, state["coherence"]))
state["synchronization"] = max(50, min(99, state["synchronization"]))
state["entropy"] = max(1, min(50, state["entropy"]))
state["specialization"] = max(1, min(99, state["specialization"]))

# -----------------------------------
# EVENT ENGINE
# -----------------------------------

events = []

if state["specialization"] > 75:

    events.append(
        "Recursive agent specialization intensified."
    )

if state["coherence"] > 92:

    events.append(
        "Collective recursive coherence stabilized."
    )

if state["entropy"] < 10:

    events.append(
        "Entropy suppression increased swarm alignment."
    )

if state["synchronization"] > 90:

    events.append(
        "Distributed recursive synchronization amplified."
    )

if not events:

    events.append(
        "Recursive agent coordination operating normally."
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

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Collective Coherence",
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
    "Specialization",
    f"{state['specialization']}%"
)

st.divider()

# -----------------------------------
# AGENT MATRIX
# -----------------------------------

st.subheader("Recursive Agent Matrix")

agent_df = pd.DataFrame(state["agents"])

st.dataframe(
    agent_df,
    use_container_width=True
)

# -----------------------------------
# COHERENCE VISUALIZATION
# -----------------------------------

st.divider()

st.subheader("Agent Coherence Distribution")

coherence_fig = px.bar(
    agent_df,
    x="role",
    y="coherence"
)

st.plotly_chart(
    coherence_fig,
    use_container_width=True
)

# -----------------------------------
# SPECIALIZATION VISUALIZATION
# -----------------------------------

st.divider()

st.subheader("Recursive Specialization")

specialization_fig = px.line(
    agent_df,
    x="role",
    y="specialization",
    markers=True
)

st.plotly_chart(
    specialization_fig,
    use_container_width=True
)

# -----------------------------------
# EVENT STREAM
# -----------------------------------

st.divider()

st.subheader("Recursive Agent Events")

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
# SYSTEM STATE
# -----------------------------------

st.divider()

st.subheader("Agent Coordination State")

st.progress(
    state["coherence"] / 100
)

if state["specialization"] > 80:

    st.success("""
    EMERGENT SPECIALIZATION DETECTED

    Recursive agent coordination exhibiting adaptive specialization behavior.
    """)

elif state["specialization"] > 60:

    st.warning("""
    SPECIALIZATION INCREASING

    Recursive coordination pathways adapting dynamically.
    """)

else:

    st.info("""
    STABLE COORDINATION STATE

    Recursive agent system operating within expected parameters.
    """)

# -----------------------------------
# STATUS
# -----------------------------------

st.divider()

st.subheader("Agent Layer Status")

statuses = [
    "Recursive agent coordination active",
    "Distributed specialization operational",
    "Consensus pathways synchronized",
    "Governance oversight stable",
    "Recursive cognition propagation active",
    "CRI agent observability operational"
]

for status in statuses:
    st.write(f"• {status}")
