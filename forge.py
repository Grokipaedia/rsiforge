import random
from forge_engine import run_agent_proposal
from datetime import datetime

print("🔥 RSI Forge - Ultra Simple Version\n")

problem = input("Problem: ") or "How should we evolve RSI Forge itself in the next 30 days..."

print("\nStarting 6 rounds...\n")

history = [f"Round 0: {problem}"]

for r in range(1, 7):
    print(f"\n--- Round {r} ---")
    
    for i in range(3):
        response = run_agent_proposal(problem, history[-1], r, True)
        print(f"Agent {i}: {response[:500]}...\n")
    
    human = input("Your Human Anchor Input (paste prompt): ").strip()
    if human:
        history.append(f"Human (Round {r}): {human}")
        print("✓ Saved\n")
    else:
        history.append(f"Round {r}: No input")

print("\n=== DONE ===\n")
for h in history:
    print(h)

print(f"\nSession saved at {datetime.now().strftime('%H:%M')}")
input("Press Enter to exit...")
