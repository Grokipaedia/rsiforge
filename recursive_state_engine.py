import json
import os
import random
from datetime import datetime

# -----------------------------------
# GLOBAL STATE FILE
# -----------------------------------

STATE_FILE = "cri_state.json"

# -----------------------------------
# DEFAULT STATE
# -----------------------------------

DEFAULT_STATE = {

    "coherence": 85,
    "synchronization": 80,
    "entropy": 20,
    "emergence": 40,
    "phase_transition": 35,
    "memory_integrity": 88,
    "governance_strength": 90,
    "recursive_depth": 5,
    "cluster_count": 4,
    "node_count": 18,

    "agents": [],

    "events": []
}

# -----------------------------------
# LOAD STATE
# -----------------------------------

def load_state():

    if os.path.exists(STATE_FILE):

        with open(STATE_FILE, "r") as f:
            return json.load(f)

    return DEFAULT_STATE.copy()

# -----------------------------------
# SAVE STATE
# -----------------------------------

def save_state(state):

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

# -----------------------------------
# CLAMP
# -----------------------------------

def clamp(value, low, high):

    return max(low, min(high, value))

# -----------------------------------
# INITIALIZE AGENTS
# -----------------------------------

def initialize_agents(state):

    if state["agents"]:
        return state

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

    for i in range(len(roles)):

        state["agents"].append({

            "id": i,
            "role": roles[i],

            "coherence": random.randint(70, 99),
            "stability": random.randint(70, 99),
            "specialization": random.randint(40, 90)
        })

    return state

# -----------------------------------
# EVENT ENGINE
# -----------------------------------

def add_event(state, message):

    event = {

        "timestamp": datetime.utcnow().strftime("%H:%M:%S"),
        "event": message
    }

    state["events"].insert(0, event)

    state["events"] = state["events"][:50]

# -----------------------------------
# RECURSIVE DYNAMICS
# -----------------------------------

def evolve_system(state):

    # -----------------------------------
    # HUMAN COHERENCE STABILIZATION
    # -----------------------------------

    if state["governance_strength"] > 85:

        state["entropy"] -= random.randint(1, 3)

    # -----------------------------------
    # MEMORY REINFORCEMENT
    # -----------------------------------

    if state["memory_integrity"] > 90:

        state["coherence"] += random.randint(1, 2)

    # -----------------------------------
    # SYNCHRONIZATION PROPAGATION
    # -----------------------------------

    if state["coherence"] > 88:

        state["synchronization"] += random.randint(1, 3)

    # -----------------------------------
    # EMERGENCE GENERATION
    # -----------------------------------

    if state["synchronization"] > 90:

        state["emergence"] += random.randint(2, 4)

    # -----------------------------------
    # PHASE TRANSITIONS
    # -----------------------------------

    if (
        state["coherence"] > 90
        and state["entropy"] < 12
        and state["emergence"] > 75
    ):

        state["phase_transition"] += random.randint(3, 6)

        add_event(
            state,
            "Recursive phase transition acceleration detected."
        )

    # -----------------------------------
    # TOPOLOGY EVOLUTION
    # -----------------------------------

    if state["emergence"] > 80:

        state["cluster_count"] += random.choice([0, 1])

        state["node_count"] += random.randint(1, 2)

    # -----------------------------------
    # RECURSIVE DEPTH
    # -----------------------------------

    if state["phase_transition"] > 70:

        state["recursive_depth"] += random.choice([0, 1])

    # -----------------------------------
    # AGENT EVOLUTION
    # -----------------------------------

    for agent in state["agents"]:

        if state["synchronization"] > 85:

            agent["coherence"] += random.randint(0, 2)

        if state["entropy"] > 30:

            agent["stability"] -= random.randint(1, 3)

        if agent["coherence"] > 90:

            agent["specialization"] += random.randint(1, 2)

        # Clamp agent values
        agent["coherence"] = clamp(
            agent["coherence"],
            60,
            99
        )

        agent["stability"] = clamp(
            agent["stability"],
            50,
            99
        )

        agent["specialization"] = clamp(
            agent["specialization"],
            1,
            99
        )

    # -----------------------------------
    # NATURAL SYSTEM DRIFT
    # -----------------------------------

    state["coherence"] += random.randint(-2, 3)

    state["synchronization"] += random.randint(-2, 3)

    state["entropy"] += random.randint(-3, 4)

    state["memory_integrity"] += random.randint(-1, 2)

    state["governance_strength"] += random.randint(-1, 2)

    # -----------------------------------
    # CLAMP GLOBAL VALUES
    # -----------------------------------

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

    state["governance_strength"] = clamp(
        state["governance_strength"],
        60,
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
        20
    )

    state["node_count"] = clamp(
        state["node_count"],
        10,
        100
    )

    # -----------------------------------
    # GENERIC EVENTS
    # -----------------------------------

    if state["coherence"] > 92:

        add_event(
            state,
            "Collective recursive coherence stabilized."
        )

    if state["emergence"] > 85:

        add_event(
            state,
            "Emergent recursive coordination intensified."
        )

    if state["entropy"] < 10:

        add_event(
            state,
            "Entropy suppression reinforced synchronization."
        )

    if state["memory_integrity"] > 92:

        add_event(
            state,
            "Recursive memory reinforcement cycle completed."
        )

    if state["synchronization"] > 92:

        add_event(
            state,
            "Distributed synchronization amplification detected."
        )

    return state

# -----------------------------------
# MAIN ACCESS FUNCTION
# -----------------------------------

def get_evolved_state():

    state = load_state()

    state = initialize_agents(state)

    state = evolve_system(state)

    save_state(state)

    return state
