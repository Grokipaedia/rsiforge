
3. Create a new file in the repo called **`app.py`** and paste this **updated, branded MVP** (I’ve already swapped in RSI Forge everywhere and cleaned it up):

```python
import streamlit as st
import time
import random

st.set_page_config(page_title="RSI Forge", page_icon="🔥", layout="wide")
st.title("🔥 RSI Forge")
st.markdown("**Collective Recursive Intelligence** — Humans + AIs forging what comes *beyond* RSI")

# Sidebar controls
st.sidebar.header("Forge Controls")
num_agents = st.sidebar.slider("Number of AI agents", 2, 8, 4)
max_rounds = st.sidebar.slider("Max recursive rounds", 3, 20, 8)
human_weight = st.sidebar.slider("Human anchor weight (0-1)", 0.1, 1.0, 0.7)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []
if "rules" not in st.session_state:
    st.session_state.rules = "Default improvement rule: Maximize clarity, novelty, and coherence while preserving human meaning."
if "phase_events" not in st.session_state:
    st.session_state.phase_events = []

# Core Loop
st.header("The Arena — Run a Recursive Session")
problem = st.text_area("Problem / Goal to improve recursively:", 
                       "Design a governance primitive that makes alignment self-improving without losing human direction.", 
                       height=100)

if st.button("🚀 Start RSI Forge Loop", type="primary"):
    with st.spinner("Running recursive intelligence loop..."):
        current_solution = "Initial draft solution..."
        st.session_state.history.append(("Human anchor (Round 0)", problem))
        
        for round_num in range(1, max_rounds + 1):
            # Simulate agent proposals
            proposals = [f"Agent {i} proposes: Enhanced version with meta-recursive rule tweak #{round_num}" for i in range(num_agents)]
            
            # MRI layer: agents propose rule changes
            if random.random() > 0.6:
                new_rule = "New MRI rule: Allow spontaneous reframing of the fitness function itself."
                st.session_state.rules = new_rule
                st.success(f"🔄 MRI EVENT — Rules updated: {new_rule}")
            
            # Human anchor step
            st.write(f"**Round {round_num} — Human Anchor**")
            human_input = st.text_input(f"Your reframing / veto / enhancement (Round {round_num}):", 
                                        key=f"human_{round_num}")
            
            if human_input:
                current_solution = f"Human-refined: {human_input}"
                st.session_state.history.append((f"Human anchor (Round {round_num})", human_input))
            else:
                current_solution = random.choice(proposals)
                st.session_state.history.append((f"Collective (Round {round_num})", current_solution))
            
            # Phase Transition Detector
            if random.random() > 0.75:
                event = f"Phase Transition detected at Round {round_num}: Spontaneous abstraction collapse — problem reframed from 'solve X' to 'X dissolves into Y'"
                st.session_state.phase_events.append((round_num, event))
                st.balloons()
                st.markdown(f"**🌊 COGNITIVE PHASE TRANSITION** — {event}")
            
            time.sleep(0.8)
        
        st.success("Loop complete! The forge has spoken.")
        
        st.subheader("Session Trace")
        for actor, text in st.session_state.history:
            st.write(f"**{actor}**: {text}")
        
        if st.session_state.phase_events:
            st.subheader("Phase Transition Log")
            for r, e in st.session_state.phase_events:
                st.write(f"Round {r}: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("RSI Forge @ rsiforge.com • v0.1 • Built live from Grokipaedia • Beyond RSI is now runnable")
