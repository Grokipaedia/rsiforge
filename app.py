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
st.session_state.openai_key = st.session_state.get("openai_key", "")

recursive_si_mode = st.sidebar.toggle("**Recursive SI Mode**", value=True)
num_agents = st.sidebar.slider("Number of AI Agents", 2, 8, 5)
max_rounds = st.sidebar.slider("Max Recursive Rounds", 3, 12, 6)

st.header("The Arena — Live Recursive Session")
problem = st.text_area("Problem:", height=100, value="How should we evolve RSI Forge itself in the next 30 days...")

if st.button("🚀 Start RSI Forge Loop", type="primary"):
    with st.spinner("Running..."):
        st.session_state.history = [("Human anchor (Round 0)", problem)]
        st.session_state.phase_events = []
        
        for round_num in range(1, max_rounds + 1):
            st.divider()
            st.subheader(f"Round {round_num} {'🔄 Recursive SI' if recursive_si_mode else ''}")
            
            # Agents
            for i in range(num_agents):
                proposal = run_agent_proposal(problem, st.session_state.history[-1][1], round_num, recursive_si_mode)
                st.write(f"**Agent {i}**: {proposal[:400]}...")
            
            # Human Anchor - More reliable
            st.info("🧭 **Paste Human Anchor Prompt Here** (Round " + str(round_num) + ")")
            human_input = st.text_area("Your input (this is the most important part):", 
                                       key=f"human_input_{round_num}", height=80)
            
            if human_input.strip():
                st.session_state.history.append((f"Human anchor (Round {round_num})", human_input))
                st.success("Human anchor recorded")
            else:
                st.session_state.history.append((f"Collective (Round {round_num})", "No human input this round"))
            
            # Phase Transition
            if random.random() > 0.65:
                event = f"🌊 Phase Transition at Round {round_num}: Spontaneous abstraction collapse!"
                st.session_state.phase_events.append((round_num, event))
                st.balloons()
                st.success(event)
            
            time.sleep(0.7)
        
        st.success("Loop Complete")

        st.subheader("Session Trace")
        for actor, text in st.session_state.history:
            st.write(f"**{actor}**: {text[:600]}...")

        render_phase_dashboard(st.session_state.phase_events)
        from session_manager import export_session
        export_session(st.session_state.history, st.session_state.phase_events, problem, recursive_si_mode)

st.sidebar.caption("RSI Forge @ rsiforge.com • v0.5.1 • Improved Human Input")
