import gradio as gr
import random
from forge_engine import run_agent_proposal
from datetime import datetime

def run_forge(problem, recursive_si_mode, num_rounds, num_agents):
    history = []
    phase_events = []
    output = []

    history.append(f"**Human (Round 0)**: {problem}")
    output.append(f"**Round 0**\n{history[0]}\n")

    for r in range(1, int(num_rounds) + 1):
        output.append(f"\n{'─' * 60}")
        output.append(f"**ROUND {r}** {'🔄 RECURSIVE SI MODE' if recursive_si_mode else ''}")
        
        # Agents
        for i in range(int(num_agents)):
            proposal = run_agent_proposal(problem, history[-1], r, recursive_si_mode)
            output.append(f"\n**Agent {i}**: {proposal}")
        
        # Human Input will be handled in the interface
        output.append(f"\n**Waiting for Human Anchor Input (Round {r})**")
        yield "\n".join(output), "Enter your prompt below and click Submit"

        # This is where Gradio will pause for input (we'll handle it in the UI)

    return "\n".join(output), "Session Complete"

# Beautiful Gradio Interface
with gr.Blocks(title="RSI Forge", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔥 RSI Forge\n**Collective Recursive Intelligence**")
    
    with gr.Row():
        with gr.Column(scale=2):
            problem = gr.Textbox(
                label="Main Problem / Goal",
                value="How should we evolve RSI Forge itself in the next 30 days so it becomes a true Collective Recursive Intelligence platform...",
                lines=4
            )
            
            with gr.Row():
                recursive_si = gr.Checkbox(label="Recursive SI Mode", value=True)
                num_rounds = gr.Slider(3, 10, value=6, step=1, label="Number of Rounds")
                num_agents = gr.Slider(2, 6, value=4, step=1, label="Number of Agents")
        
        with gr.Column(scale=3):
            output = gr.Textbox(label="Live Session Output", lines=25, show_copy_button=True)
            status = gr.Textbox(label="Status", value="Ready to start")
    
    start_btn = gr.Button("🚀 Start RSI Forge Loop", variant="primary", size="large")
    
    start_btn.click(
        fn=run_forge,
        inputs=[problem, recursive_si, num_rounds, num_agents],
        outputs=[output, status]
    )

    gr.Markdown("### How to use:\n1. Enter your problem\n2. Click Start\n3. Paste Human Anchor prompts when asked")

demo.launch(share=False)
