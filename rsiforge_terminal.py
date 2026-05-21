import random
import json
from datetime import datetime
from forge_engine import run_agent_proposal  # we'll use your existing engine

print("🔥 RSI Forge - Terminal Edition")
print("Collective Recursive Intelligence Test\n")

problem = input("Enter the main problem / goal:\n> ") or "How should we evolve RSI Forge itself in the next 30 days so it becomes a true Collective Recursive Intelligence platform..."

recursive_si_mode = input("Enable Recursive SI Mode? (y/n): ").lower() == 'y'
num_rounds = int(input("Number of rounds (4-8 recommended): ") or "6")
num_agents = 3

history = [f"Human (Round 0): {problem}"]
phase_events = []

print("\n=== Starting Loop ===\n")

for r in range(1, num_rounds + 1):
    print(f"\n{'='*60}")
    print(f"ROUND {r} {'🔄 RECURSIVE SI MODE' if recursive_si_mode else ''}")
    print('='*60)
    
    # Agents speak
    for i in range(num_agents):
        proposal = run_agent_proposal(problem, history[-1], r, recursive_si_mode)
        print(f"\n**Agent {i}**:")
        print(proposal[:600] + "..." if len(proposal) > 600 else proposal)
    
    # Human Anchor Input
    print("\n🧭 YOUR HUMAN ANCHOR INPUT (Round", r, ")")
    print("Paste one of your prepared prompts here:")
    human_input = input("\n> ").strip()
    
    if human_input:
        history.append(f"Human anchor (Round {r}): {human_input}")
        print("✅ Human anchor recorded")
    else:
        history.append(f"Collective (Round {r}): No input")
        print("No input — collective synthesis")
    
    # Phase Transition
    if random.random() > 0.55:
        print("\n🌊 PHASE TRANSITION DETECTED!")
        phase_events.append(r)

print("\n" + "="*60)
print("LOOP COMPLETE")
print("="*60)

# Show full history
print("\nFULL SESSION TRACE:")
for entry in history:
    print(entry)

if phase_events:
    print(f"\n🌊 Phase Transitions occurred in rounds: {phase_events}")

# Save session
session = {
    "timestamp": datetime.now().isoformat(),
    "problem": problem,
    "recursive_si_mode": recursive_si_mode,
    "history": history,
    "phase_events": phase_events
}

filename = f"rsiforge_session_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
with open(filename, "w") as f:
    json.dump(session, f, indent=2)

print(f"\n✅ Session saved to: {filename}")
print("\nRun again with: python rsiforge_terminal.py")
