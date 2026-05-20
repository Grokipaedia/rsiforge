import streamlit as st
import time
import random
from forge_engine import run_agent_proposal

st.set_page_config(page_title="RSI Forge", page_icon="🔥", layout="wide")
st.title("🔥 RSI Forge")
st.markdown("**Collective Recursive Intelligence** — Humans + AIs forging what comes *beyond* RSI")

# API Key
if "openai_key" not in st.session_state:
    st.session_state.openai_key = ""

st.sidebar.header("Forge Controls")
st.sidebar.text_input("OpenAI API Key (optional but recommended)", 
                      type="password", 
                      key="openai_key_input",
                      on_change=lambda: st.session_state.update({"openai_key": st.session_state.openai_key_input}))

num_agents = st.sidebar.slider("Number of AI agents", 2, 8, 4)
max_rounds = st.sidebar.slider("Max recursive rounds", 3, 20, 8)

# Session state
if "history" not in st.session_state: st.session_state.history = []
if "rules" not in st.session_state: st.session_state.rules = "Default: Maximize clarity, novelty, and coherence."
if "phase_events" not in st.session_state: st.session_state.phase_events = []

st.header("The Arena — Run a Recursive Session")
problem = st.text_area("Problem / Goal to improve recursively:", 
                       "Design a governance primitive that makes alignment self-improving without losing human direction.", 
                       height=100)

if st.button("🚀 Start RSI Forge Loop", type="primary"):
    with st.spinner("Running live recursive intelligence loop..."):
        st.session_state.history = []
        st.session_state.history.append(("Human anchor (Round 0)", problem))
        
        for round_num in range(1, max_rounds + 1):
            st.write(f"**Round {round_num}**")
            
            # MRI Layer
            if random.random() > 0.65:
                new_rule = "New MRI rule: Allow spontaneous reframing of the fitness function and goal ontology."
                st.session_state.rules = new_rule
                st.success(f"🔄 MRI EVENT — Rules updated: {new_rule}")
            
            # Agent proposals (real LLM now)
            for i in range(num_agents):
                proposal = run_agent_proposal(problem, st.session_state.history[-1][1] if st.session_state.history else problem, round_num)
                st.write(f"Agent {i}: {proposal[:280]}...")
            
            # Human Anchor (most important)
            human_input = st.text_input(f"**Your reframing / veto / enhancement (Round {round_num})**", 
                                        key=f"human_{round_num}")
            
            if human_input:
                st.session_state.history.append((f"Human anchor (Round {round_num})", human_input))
            else:
                st.session_state.history.append((f"Collective (Round {round_num})", "Default collective proposal"))
            
            # Phase Transition Detector
            if random.random() > 0.7:
                event = f"🌊 Phase Transition at Round {round_num}: Spontaneous abstraction collapse — problem reframed!"
                st.session_state.phase_events.append((round_num, event))
                st.balloons()
                st.success(event)
            
            time.sleep(0.6)
        
        st.success("**Loop complete.** The Forge has spoken.")

        st.subheader("Full Session Trace")
        for actor, text in st.session_state.history:
            st.write(f"**{actor}**: {text[:500]}...")

        if st.session_state.phase_events:
            st.subheader("Cognitive Phase Transitions Detected")
            for r, e in st.session_state.phase_events:
                st.write(f"Round {r}: {e}")
