import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_phase_dashboard(phase_events, history):
    if not phase_events:
        st.info("No phase transitions yet. Push the loop harder!")
        return
    
    # Create timeline data
    rounds = [r for r, _ in phase_events]
    events = [e for _, e in phase_events]
    
    df = pd.DataFrame({
        "Round": rounds,
        "Event": events,
        "Impact": [1.0 + i*0.3 for i in range(len(rounds))]
    })
    
    st.subheader("🌊 Cognitive Phase Transition Dashboard")
    
    # Timeline
    fig = px.scatter(df, x="Round", y="Impact", size="Impact", hover_data=["Event"],
                     title="Phase Transitions Over Time",
                     labels={"Impact": "Abstraction Jump Strength"})
    fig.update_traces(marker=dict(color="red", symbol="star"))
    st.plotly_chart(fig, use_container_width=True)
    
    # Progress toward phase transition (simulated entropy collapse)
    entropy = [100 - (r * 8) for r in range(1, max(rounds) + 5)]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=list(range(1, len(entropy)+1)), y=entropy,
                              mode='lines+markers', name='System Entropy',
                              line=dict(color='cyan')))
    fig2.update_layout(title="System Entropy Collapse (leading to phase transition)",
                       xaxis_title="Round", yaxis_title="Entropy")
    st.plotly_chart(fig2, use_container_width=True)
