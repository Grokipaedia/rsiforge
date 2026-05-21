import gradio as gr
import random
from forge_engine import run_agent_proposal   # we'll keep using your existing engine

def run_forge_loop(problem, recursive_si_mode, num_rounds=6):
    history = [f"**Human (Round 0)**: {problem}"]
    phase_events = []
    
    yield "\n".join(history), "Starting loop...\n"
    
    for r in range(1, num_rounds + 1):
        # Agents speak
        agent_texts = []
        for i in range(3):
            proposal = run_agent_proposal(problem, history[-1], r, recursive_si_mode)
            agent_texts.append(f"**Agent {i}**: {proposal[:500]}...")
        
        history.append("\n".join(agent_texts))
        yield "\n\n".join(history), f"Round {r} — Waiting for your Human Anchor input..."
        
        # Wait for human input (Gradio will handle this in the interface)
        human_input = yield "\n\n".join(history), f"Round {r} — Enter your prompt:"
        
        if human_input and human_input.strip():
            history.append(f"**Human Anchor (Round {r})**: {human_input}")
        else:
            history.append(f"**Collective (Round {r})**: No input")
        
        # Random phase transition
        if random.random() > 0.5:
            phase_events.append(r)
            history.append("🌊 **Phase Transition Detected!**")
        
    final = "\n\n".join(history)
    yield final, "Loop Complete! Download the session below."

# Gradio Interface
with gr.Blocks(title="RSI Forge") as demo:
    gr.Markdown("# 🔥 RSI Forge\n**Collective Recursive Intelligence**")
    
    problem = gr.Textbox(label="Main Problem", lines=4, value="How should we evolve RSI Forge itself in the next 30 days...")
    recursive_si = gr.Checkbox(label="Recursive SI Mode", value=True)
    rounds = gr.Slider(3, 10, value=6, step=1, label="Number of Rounds")
    
    start_btn = gr.Button("🚀 Start Loop", variant="primary")
    
    output = gr.Textbox(label="Live Session", lines=20)
    status = gr.Textbox(label="Status")
    
    start_btn.click(
        fn=run_forge_loop,
        inputs=[problem, recursive_si, rounds],
        outputs=[output, status]
    )

demo.launch()
