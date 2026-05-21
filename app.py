import streamlit as st
import random
from forge_engine import run_agent_proposal
from visualizer import render_phase_dashboard

st.set_page_config(page_title="RSI Forge", page_icon="🔥", layout="wide")
st.title("🔥 RSI Forge - Minimal Working Version")

st.sidebar.header("Controls")
st.sidebar.text_input("OpenAI API Key", type="password", key="openai_key_input",
                      on_change=lambda: st.session_state.update({"openai_key": st.session_state.openai_key_input}))

recursive_si_mode = st.sidebar.toggle("Recursive SI Mode", value=True)

problem = st.text_area("What do you want to explore today?", 
    value="How should we evolve RSI Forge itself in the next 30 days...",
    height=100)

if st.button("Run One Full Loop (6 rounds)", type="primary"):
    history = [("Human (Round 0)", problem)]
    
    for r in range(1, 7):
        st.divider()
        st.subheader(f"Round {r}")
        
        # Agents
        for i in range(3):
            proposal = run_agent_proposal(problem, history[-1][1], r, recursive_si_mode)
            st.write(f"**Agent {i}**: {proposal[:450]}...")
        
        # Human input - very simple
        human_input = st.text_area(f"🧭 Round {r} - Your Human Anchor Input", key=f"h{r}", height=80)
        
        if human_input.strip():
            history.append((f"Human (Round {r})", human_input))
        else:
            history.append((f"Collective (Round {r})", "No input"))
        
        if random.random() > 0.5:
            st.success("🌊 Phase Transition Occurred!")
    
    st.success("Loop finished!")
    st.subheader("History")
    for actor, text in history:
        st.write(f"**{actor}**: {text[:600]}...")

st.caption("Minimal version - paste prompts one by one")
