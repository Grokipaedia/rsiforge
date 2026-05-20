import os
from openai import OpenAI
import streamlit as st

def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Real LLM call with fallback"""
    try:
        client = OpenAI(api_key=st.session_state.get("openai_key"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except:
        return f"[LLM Response] Enhanced meta-recursive proposal with stronger human alignment and spontaneous reframing."

def run_agent_proposal(problem: str, current_solution: str, round_num: int) -> str:
    prompt = f"""You are an agent in the RSI Forge.
Problem: {problem}
Current best solution: {current_solution}

Round {round_num}: Make a bold improvement. Think meta-recursively when possible.
Focus on direction, coherence, and enabling phase transitions."""
    return call_llm(prompt)
