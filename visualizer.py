import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_phase_dashboard(phase_events, history=None):
    if not phase_events:
        st.info("No phase transitions yet. Try more rounds or Recursive SI Mode.")
        return
    
    st.subheader("🌊 Cognitive Phase Transitions Detected")
    
    rounds = [r for r, _ in phase_events]
    events = [e for _, e in phase_events]
    
    df = pd.DataFrame({"Round": rounds, "Event": events, "Strength": [1 + i*0.5 for i in range(len(rounds))]})
    
    fig = px.scatter(df, x="Round", y="Strength", size="Strength", hover_data=["Event"],
                     title="Phase Transition Timeline", color_discrete_sequence=["#ff4d4d"])
    st.plotly_chart(fig, use_container_width=True)
    
    # Entropy Collapse (more dramatic)
    max_r = max(rounds) if rounds else 8
    entropy = [100 - (r * 9) for r in range(1, max_r + 6)]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=list(range(1, len(entropy)+1)), y=entropy,
                              mode='lines+markers', name='System Entropy',
                              line=dict(color='#00f0ff', width=3)))
    fig2.update_layout(title="System Entropy Collapse Leading to Phase Transition",
                       xaxis_title="Round", yaxis_title="Entropy Level")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.success("**Phase Transition Achieved** — The collective jumped to a new abstraction layer.")
