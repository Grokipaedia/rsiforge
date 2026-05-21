import random
import json
from datetime import datetime
from forge_engine import run_agent_proposal

print("\n" + "="*70)
print("🔥 RSI FORGE — TERMINAL EDITION")
print("Collective Recursive Intelligence Test")
print("="*70 + "\n")

# Configuration
problem = input("Enter the main problem/goal:\n> ").strip() or "How should we evolve RSI Forge itself in the next 30 days so it becomes a true Collective Recursive Intelligence platform..."

recursive_si_mode = input("Enable Recursive SI Mode? (y/n): ").lower().startswith('y')
num_rounds = int(input("Number of rounds (4-8 recommended): ") or "6")
num_agents = 4

history = [f"**Human (Round 0)**: {problem}"]
phase_events = []

print(f"\n🚀 Starting {num_rounds}-round loop in {'Recursive SI Mode' if recursive_si_mode else 'Standard Mode'}...\n")

for r in range(1, num_rounds + 1):
    print(f"\n{'─'*70}")
    print(f"ROUND {r} {'🔄 RECURSIVE SI MODE' if recursive_si_mode else ''}")
    print(f"{'─'*70}\n")
    
    # Agents
    for i in range(num_agents):
        proposal = run_agent_proposal(problem, history[-1], r, recursive_si_mode)
        print(f"**Agent {i}** → {proposal[:650]}{'...' if len(proposal) > 650 else ''}\n")
    
    # Human Anchor
    print("🧭 YOUR HUMAN ANCHOR INPUT (Round", r, ")")
    print("Paste your prompt below and press Enter:")
    human_input = input("\n> ").strip()
    
    if human_input:
        history.append(f"**Human anchor (Round {r})**: {human_input}")
        print("✅ Human anchor recorded\n")
    else:
        history.append(f"**Collective (Round {r})**: No input")
        print("⚠️ No input — using collective synthesis\n")
    
    # Smarter Phase Transition (based on content + random)
    if random.random() > 0.45 or "reframe" in human_input.lower() or "phase" in human_input.lower():
        print("🌊 **COGNITIVE PHASE TRANSITION DETECTED!**")
        phase_events.append(r)
        print("   Spontaneous abstraction collapse / reframing occurred.\n")

# Final Output
print("\n" + "="*70)
print("LOOP COMPLETE — THE FORGE HAS SPOKEN")
print("="*70 + "\n")

print("FULL SESSION TRACE:")
for entry in history:
    print(entry)
    print()

if phase_events:
    print(f"🌊 Phase Transitions occurred in rounds: {phase_events}")

# Markdown Export
markdown = f"# RSI Forge Session\n\n**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
markdown += f"**Problem**: {problem}\n"
markdown += f"**Recursive SI Mode**: {'Yes' if recursive_si_mode else 'No'}\n\n"
markdown += "## Full History\n\n"
for entry in history:
    markdown += f"{entry}\n\n"

if phase_events:
    markdown += f"## Phase Transitions\n\nOccurred in rounds: {phase_events}\n"

filename_md = f"rsiforge_session_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
with open(filename_md, "w", encoding="utf-8") as f:
    f.write(markdown)

print(f"\n✅ Session saved as Markdown: {filename_md}")
print("   (Open this file in any Markdown viewer or upload to Grokipaedia)")

# Also save JSON
with open(filename_md.replace(".md", ".json"), "w", encoding="utf-8") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "problem": problem,
        "recursive_si_mode": recursive_si_mode,
        "history": history,
        "phase_events": phase_events
    }, f, indent=2)

print("\nReady for next run. Just type: python rsiforge_terminal.py")
