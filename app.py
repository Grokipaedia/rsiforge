import streamlit as st
import time
import random
from forge_engine import run_agent_proposal
from visualizer import render_phase_dashboard

st.set_page_config(page_title="RSI Forge", page_icon="🔥", layout="wide")
st.title("🔥 RSI Forge")
st.markdown("**Collective Recursive Intelligence** — Humans + AIs forging what comes *beyond* RSI")

# Sidebar
st.sidebar.header("Forge Controls")
st.sidebar.text_input("OpenAI API Key", type="password", key="openai_key_input",
                      on_change=lambda: st.session_state.update({"openai_key": st.session_state.openai_key_input}))
st.session_state.openai_key = st.session_state.get("openai_key_input", "")

num_agents = st.sidebar.slider("AI Agents", 2, 8, 4)
max_rounds = st.sidebar.slider("Max Rounds", 3, 20, 8)

# Session state
if "history" not in st.session_state: st.session_state.history = []
if "rules" not in st.session_state: st.session_state.rules = "Default: Maximize clarity, novelty, coherence."
if "phase_events" not in st.session_state: st.session_state.phase_events = []

st.header("The Arena")
problem = st.text_area("Problem / Goal to improve recursively:", 
                       "Design a governance primitive that makes alignment self-improving without losing human direction.", 
                       height=120)

if st.button("🚀 Start RSI Forge Loop", type="primary"):
    with st.spinner("Running live recursive intelligence..."):
        st.session_state.history = [("Human anchor (Round 0)", problem)]
        st.session_state.phase_events = []
        
        for round_num in range(1, max_rounds + 1):
            st.divider()
            st.write(f"### Round {round_num}")
            
            # MRI Layer
            if random.random() > 0.6:
                new_rule = "New MRI rule: Allow spontaneous reframing of goals and fitness functions."
                st.session_state.rules = new_rule
                st.success(f"🔄 MRI EVENT: {new_rule}")
            
            # Agents
            for i in range(num_agents):
                proposal = run_agent_proposal(problem, st.session_state.history[-1][1], round_num)
                st.write(f"**Agent {i}**: {proposal[:320]}...")
            
            # Human Anchor
            human_input = st.text_input(f"**🧭 Your Human Anchor Input (Round {round_num})** — This carries the most weight", 
                                        key=f"human_{round_num}")
            
            if human_input:
                st.session_state.history.append((f"Human anchor (Round {round_num})", human_input))
            else:
                st.session_state.history.append((f"Collective (Round {round_num})", "Collective synthesis"))
            
            # Phase Transition
            if random.random() > 0.68:
                event = f"🌊 Phase Transition at Round {round_num}: Spontaneous abstraction collapse & reframing!"
                st.session_state.phase_events.append((round_num, event))
                st.balloons()
                st.success(event)
            
            time.sleep(0.7)
        
        st.success("**Loop Complete** — The Forge has spoken.")

        st.subheader("Session Trace")
        for actor, text in st.session_state.history:
            st.write(f"**{actor}**: {text[:600]}...")

        render_phase_dashboard(st.session_state.phase_events, st.session_state.history)

st.sidebar.caption("RSI Forge @ rsiforge.com • v0.2 • Grokipaedia Live")
