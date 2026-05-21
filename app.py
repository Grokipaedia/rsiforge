import streamlit as st
import time
import random
from forge_engine import run_agent_proposal
from visualizer import render_phase_dashboard

st.set_page_config(page_title="RSI Forge", page_icon="🔥", layout="wide")
st.title("🔥 RSI Forge")
st.markdown("**Collective Recursive Intelligence** — Humans + AIs forging what comes *beyond* RSI")

st.sidebar.header("Forge Controls")
st.sidebar.text_input("OpenAI API Key", type="password", key="openai_key_input",
                      on_change=lambda: st.session_state.update({"openai_key": st.session_state.openai_key_input}))

recursive_si_mode = st.sidebar.toggle("Recursive SI Mode", value=True)
num_agents = st.sidebar.slider("AI Agents", 2, 6, 4)
max_rounds = st.sidebar.slider("Rounds", 3, 8, 6)

st.header("The Arena")

problem = st.text_area("Main Problem / Goal:", height=120, 
    value="How should we evolve RSI Forge itself in the next 30 days...")

if st.button("🚀 Start New Loop", type="primary"):
    st.session_state.history = [("Human (Round 0)", problem)]
    st.session_state.phase_events = []
    
    for round_num in range(1, max_rounds + 1):
        st.divider()
        st.subheader(f"Round {round_num}")
        
        # Agents speak first
        for i in range(num_agents):
            proposal = run_agent_proposal(problem, st.session_state.history[-1][1], round_num, recursive_si_mode)
            st.write(f"**Agent {i}**: {proposal[:450]}...")
        
        # Human input - simple single box per round
        human_input = st.text_area(f"🧭 Your Human Anchor Input - Round {round_num}", 
                                   key=f"human_{round_num}", height=100)
        
        if human_input.strip():
            st.session_state.history.append((f"Human anchor (Round {round_num})", human_input))
            st.success("Human input recorded")
        else:
            st.session_state.history.append((f"Collective (Round {round_num})", "No human input"))
        
        # Phase Transition
        if random.random() > 0.55:
            st.balloons()
            st.success("🌊 Phase Transition Detected!")
            st.session_state.phase_events.append((round_num, "Spontaneous abstraction collapse!"))
        
        time.sleep(0.6)
    
    st.success("Loop Finished!")
    
    st.subheader("Session Trace")
    for actor, text in st.session_state.history:
        st.write(f"**{actor}**: {text[:700]}...")
    
    render_phase_dashboard(st.session_state.phase_events)
    
    from session_manager import export_session
    export_session(st.session_state.history, st.session_state.phase_events, problem, recursive_si_mode)

st.sidebar.caption("RSI Forge @ rsiforge.com • Simple v0.6")
