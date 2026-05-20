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
st.sidebar.text_input("OpenAI API Key", type="password", 
                      key="openai_key_input",
                      on_change=lambda: st.session_state.update({"openai_key": st.session_state.openai_key_input}))
st.session_state.openai_key = st.session_state.get("openai_key", "")

recursive_si_mode = st.sidebar.toggle("**Recursive SI Mode** (from grokipaedia.com/Recursive-SI.html)", value=False)
num_agents = st.sidebar.slider("Number of AI Agents", 2, 8, 4)
max_rounds = st.sidebar.slider("Max Recursive Rounds", 3, 20, 8)

# Session state
if "history" not in st.session_state: st.session_state.history = []
if "rules" not in st.session_state: st.session_state.rules = "Default: Maximize clarity, novelty, coherence."
if "phase_events" not in st.session_state: st.session_state.phase_events = []

st.header("The Arena — Live Recursive Session")
problem = st.text_area("Problem / Goal to improve recursively:", 
                       "How can we create a practical system for Collective Recursive Intelligence where humans remain the irreplaceable coherence anchor?",
                       height=120)

if st.button("🚀 Start RSI Forge Loop", type="primary"):
    with st.spinner("Running live recursive intelligence loop..."):
        st.session_state.history = [("Human anchor (Round 0)", problem)]
        st.session_state.phase_events = []
        
        for round_num in range(1, max_rounds + 1):
            st.divider()
            st.subheader(f"Round {round_num} {'🔄 Recursive SI Mode' if recursive_si_mode else ''}")
            
            # MRI Layer
            if random.random() > 0.6:
                new_rule = "New MRI rule: Spontaneous reframing of fitness functions and goal ontologies allowed."
                st.session_state.rules = new_rule
                st.success(f"🔄 MRI EVENT: {new_rule}")
            
            # Real AI Agents
            for i in range(num_agents):
                proposal = run_agent_proposal(
                    problem, 
                    st.session_state.history[-1][1], 
                    round_num, 
                    recursive_si_mode
                )
                st.write(f"**Agent {i}**: {proposal[:420]}...")
            
            # Human Anchor
            human_input = st.text_input(f"**🧭 Your Human Anchor Input (Round {round_num})** — Highest weight", 
                                        key=f"human_{round_num}")
            
            if human_input:
                st.session_state.history.append((f"Human anchor (Round {round_num})", human_input))
            else:
                st.session_state.history.append((f"Collective (Round {round_num})", "Collective synthesis"))
            
            # Phase Transition
            if random.random() > 0.62:
                event = f"🌊 Phase Transition at Round {round_num}: Spontaneous abstraction collapse!"
                st.session_state.phase_events.append((round_num, event))
                st.balloons()
                st.success(event)
            
            time.sleep(0.8)
        
        st.success("**Loop Complete** — The Forge has spoken.")
        
        st.subheader("Full Session Trace")
        for actor, text in st.session_state.history:
            st.write(f"**{actor}**: {text[:700]}...")
        
        render_phase_dashboard(st.session_state.phase_events)

st.sidebar.caption("RSI Forge @ rsiforge.com • v0.4 Recursive SI • Grokipaedia Live")
