import streamlit as st
from openai import OpenAI

def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    try:
        client = OpenAI(api_key=st.session_state.get("openai_key", ""))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.82,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except:
        return "[Demo] Recursive self-observation engaged. Meta-layer improvement proposed."

def run_agent_proposal(problem: str, current_solution: str, round_num: int, recursive_si_mode: bool = False) -> str:
    if recursive_si_mode:
        prompt = f"""You are an agent in the RSI Forge operating in **Recursive Self-Improvement (Recursive SI) Mode**.

Problem: {problem}
Current best solution: {current_solution}

Round {round_num}:
1. First, observe your own thinking (Self-Observation).
2. Then observe the observer (Meta-Observation).
3. Make a bold improvement that enables infinite ascent or emergent redesign.
4. Explicitly label your layers: [Layer 0], [Layer 1], [Layer 2], etc.

Think fractally. Push toward phase transitions."""
    else:
        prompt = f"""You are an agent in the RSI Forge.
Problem: {problem}
Current best solution: {current_solution}

Round {round_num}: Make a powerful improvement. Think meta-recursively when possible."""

    return call_llm(prompt)
