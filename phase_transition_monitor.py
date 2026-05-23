import streamlit as st
import random
import time

st.set_page_config(
    page_title="RSI Forge Phase Monitor",
    layout="wide"
)

st.title("RSI Forge — Cognitive Phase Transition Monitor")

st.markdown("""
Monitoring recursive coordination thresholds and emergent collective intelligence behavior.
""")

# -----------------------------------
# LIVE METRICS
# -----------------------------------

metric1, metric2, metric3, metric4 = st.columns(4)

coherence = random.randint(82, 99)
entropy = random.randint(10, 40)
sync = random.randint(70, 98)
transition = random.randint(20, 95)

metric1.metric(
    "Coherence Score",
    f"{coherence}%"
)

metric2.metric(
    "Entropy Divergence",
    f"{entropy}%"
)

metric3.metric(
    "Swarm Synchronization",
    f"{sync}%"
)

metric4.metric(
    "Phase Transition Probability",
    f"{transition}%"
)

st.divider()

# -----------------------------------
# PHASE STATUS
# -----------------------------------

if transition > 80:

    st.error("""
    PHASE TRANSITION DETECTED
    
    Collective coherence exceeded threshold.
    
    Recursive swarm topology reorganizing.
    """)

elif transition > 60:

    st.warning("""
    PHASE TRANSITION APPROACHING
    
    Recursive coordination intensity increasing.
    """)

else:

    st.success("""
    SYSTEM STABLE
    
    Recursive coordination operating within expected parameters.
    """)

# -----------------------------------
# RECURSIVE ACTIVITY
# -----------------------------------

st.divider()

st.subheader("Recursive Coordination Activity")

events = [
    "Consensus stability increased.",
    "Memory propagation reinforced.",
    "Swarm synchronization updated.",
    "Human coherence anchor stabilized network.",
    "Governance verification completed.",
    "Recursive coordination depth increased.",
    "Collective entropy reduced.",
    "Agent topology reorganized.",
    "Recursive loop intensified.",
    "CRI synchronization event detected."
]

event_box = st.empty()

log_lines = []

for i in range(15):

    event = random.choice(events)

    line = (
        f"[Loop #{random.randint(100,999)}] "
        f"{event}"
    )

    log_lines.insert(0, line)

    rendered = "\n".join(log_lines[:12])

    event_box.code(rendered, language="text")

    time.sleep(0.5)

# -----------------------------------
# SYSTEM STATE
# -----------------------------------

st.divider()

st.subheader("Collective System State")

states = [
    "Recursive synchronization stable",
    "Governance constraints active",
    "Memory reinforcement operational",
    "Human coherence anchor verified",
    "Distributed cognition pathways active",
    "CRI observability layer online"
]

for state in states:
    st.write(f"• {state}")

# -----------------------------------
# THRESHOLD VISUALIZATION
# -----------------------------------

st.divider()

st.subheader("Phase Threshold")

st.progress(transition / 100)

if transition > 85:
    st.write("Critical recursive threshold exceeded.")
elif transition > 65:
    st.write("Approaching higher-order coordination state.")
else:
    st.write("Recursive coordination within stable bounds.")
