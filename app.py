import streamlit as st
import random
from forge_engine import run_agent_proposal
from visualizer import render_phase_dashboard

st.set_page_config(page_title="RSI Forge", page_icon="🔥", layout="wide")
st.title("🔥 RSI Forge")
st.markdown("**Simple Reliable Version** — Human prompts should now save correctly")

st.sidebar.header("Controls")
st.sidebar.text_input("OpenAI API Key", type="password", key="openai_key_input",
                      on_change=lambda: st.session_state.update({"openai_key": st.session_state.openai_key_input}))

recursive_si_mode = st.sidebar.toggle("Recursive SI Mode", value=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "current_round" not in st.session_state:
    st.session_state.current_round = 0

problem = st.text_area("Main Problem:", 
    value="How should we evolve RSI Forge itself in the next 30 days so it becomes a true Collective Recursive Intelligence platform...",
    height=100)

if st.button("🚀 Start New Loop", type="primary"):
    st.session_state.history = [("Human (Round 0)", problem)]
    st.session_state.current_round = 1
    st.rerun()

if st.session_state.current_round >= 1:
    round_num = st.session_state.current_round
    
    st.divider()
    st.subheader(f"Round {round_num} {'🔄 Recursive SI Mode' if recursive_si_mode else ''}")
    
    # Agents
    for i in range(3):
        proposal = run_agent_proposal(problem, st.session_state.history[-1][1], round_num, recursive_si_mode)
        st.write(f"**Agent {i}**: {proposal[:500]}...")
    
    # Human Input
    st.info("🧭 Paste your Human Anchor Prompt below")
    human_input = st.text_area("Your input for this round:", key=f"human_input_{round_num}", height=120)
    
    if st.button(f"✅ Submit Round {round_num} & Go to Next", type="primary"):
        if human_input.strip():
            st.session_state.history.append((f"Human anchor (Round {round_num})", human_input))
        else:
            st.session_state.history.append((f"Collective (Round {round_num})", "No input"))
        
        st.session_state.current_round += 1
        st.rerun()

# Show history when finished
if st.session_state.current_round > 6:
    st.success("**Loop Complete!**")
    st.subheader("Full History")
    for actor, text in st.session_state.history:
        st.write(f"**{actor}**: {text[:700]}...")
    
    render_phase_dashboard([])  # temporary
    from session_manager import export_session
    export_session(st.session_state.history, [], problem, recursive_si_mode)

st.caption("v0.7 Simple Step-by-Step — Prompts should save now")
