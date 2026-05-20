import json
import streamlit as st
from datetime import datetime

def export_session(history, phase_events, problem, recursive_si_mode):
    session_data = {
        "timestamp": datetime.now().isoformat(),
        "problem": problem,
        "recursive_si_mode": recursive_si_mode,
        "history": history,
        "phase_events": phase_events,
        "version": "0.4"
    }
    
    json_str = json.dumps(session_data, indent=2)
    
    st.download_button(
        label="📥 Download Session as JSON",
        data=json_str,
        file_name=f"rsiforge_session_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )
    
    # Shareable link simulation (for now)
    st.caption("🔗 In future versions: one-click shareable public links")
    
    return session_data
