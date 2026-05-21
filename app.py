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
max_rounds = st.sidebar.slider("Max Recursive Rounds", 3, 10, 6)

st.header("The Arena — Live Recursive Session")
problem = st.text_area("Problem:", 
    value="How should we evolve RSI Forge itself in the next 30 days so it becomes a true Collective Recursive Intelligence platform...",
    height=100)

if st.button("🚀 Start RSI Forge Loop", type="primary"):
    with st.spinner("Preparing loop..."):
        st.session_state.history = [("Human anchor (Round 0)", problem)]
        st.session_state.phase_events = []
        
        # === COLLECT ALL HUMAN INPUTS FIRST (this fixes the issue) ===
        human_inputs = []
        for r in range(1, max_rounds + 1):
            st.subheader(f"Round {r} — Human Anchor Input")
            inp = st.text_area(f"Your prompt for Round {r}:", 
                               key=f"pre_input_{r}", 
                               height=90,
                               help="Paste one of the prepared prompts here")
            human_inputs.append(inp if inp.strip() else "No human input this round")
        
        # Now run the actual loop
        if st.button("▶️ Run the Full Loop Now", type="primary"):
            with st.spinner("Running the Forge..."):
                for round_num in range(1, max_rounds + 1):
                    st.divider()
                    st.subheader(f"Round {round_num} {'🔄 Recursive SI Mode' if recursive_si_mode else ''}")
                    
                    # Agents
                    for i in range(num_agents):
                        proposal = run_agent_proposal(problem, st.session_state.history[-1][1], round_num, recursive_si_mode)
                        st.write(f"**Agent {i}**: {proposal[:420]}...")
                    
                    # Use pre-collected human input
                    human_input = human_inputs[round_num-1]
                    st.session_state.history.append((f"Human anchor (Round {round_num})", human_input))
                    
                    if human_input != "No human input this round":
                        st.success("✅ Human anchor recorded")
                    else:
                        st.warning("No human input this round")
                    
                    # Phase Transition
                    if random.random() > 0.6:
                        event = f"🌊 Phase Transition at Round {round_num}: Spontaneous abstraction collapse!"
                        st.session_state.phase_events.append((round_num, event))
                        st.balloons()
                        st.success(event)
                    
                    time.sleep(0.7)
                
                st.success("**Loop Complete** — The Forge has spoken.")

                st.subheader("Full Session Trace")
                for actor, text in st.session_state.history:
                    st.write(f"**{actor}**: {text[:700]}...")

                render_phase_dashboard(st.session_state.phase_events)

                from session_manager import export_session
                export_session(st.session_state.history, st.session_state.phase_events, problem, recursive_si_mode)
