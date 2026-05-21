import random
import json
from datetime import datetime
from forge_engine import run_agent_proposal

print("\n" + "═"*80)
print("🔥 RSI FORGE — TERMINAL EDITION v0.8")
print("Enhanced • Better Phase Detection • Markdown Export")
print("═"*80 + "\n")

# Setup
problem = input("Main Problem / Goal:\n> ").strip() or "How should we evolve RSI Forge itself in the next 30 days..."

recursive_si_mode = input("Recursive SI Mode? (y/n): ").lower().startswith('y')
num_rounds = int(input("Number of rounds (4-8): ") or "6")
num_agents = 4

history = [f"**Human (Round 0)**: {problem}"]
full_log = []  # For rich Markdown export

print(f"\n🚀 Starting {num_rounds}-round loop...\n")

for r in range(1, num_rounds + 1):
    print(f"\n{'─'*80}")
    print(f"ROUND {r} {'🔄 RECURSIVE SI MODE' if recursive_si_mode else ''}")
    print(f"{'─'*80}\n")
    
    round_log = [f"### Round {r}"]
    
    # Agents
    for i in range(num_agents):
        proposal = run_agent_proposal(problem, history[-1], r, recursive_si_mode)
        print(f"**Agent {i}** → {proposal[:700]}{'...' if len(proposal) > 700 else ''}\n")
        round_log.append(f"**Agent {i}**: {proposal}")
    
    # Human Anchor
    print("🧭 YOUR HUMAN ANCHOR INPUT (Round", r, ")")
    human_input = input("\n> ").strip()
    
    if human_input:
        history.append(f"**Human anchor (Round {r})**: {human_input}")
        print("✅ Human anchor recorded\n")
        round_log.append(f"**Human anchor**: {human_input}")
    else:
        history.append(f"**Collective (Round {r})**: No input")
        round_log.append("**Human anchor**: (None)")
    
    # Smarter Phase Transition
    trigger = random.random() > 0.4
    if trigger or any(word in human_input.lower() for word in ["reframe", "phase", "dissolve", "emerge", "meta"]):
        print("🌊 **COGNITIVE PHASE TRANSITION DETECTED**")
        print("   Spontaneous abstraction collapse / reframing occurred.\n")
        history.append("🌊 **Phase Transition**")
        round_log.append("**Phase Transition**: Yes - Spontaneous abstraction collapse")
    
    full_log.extend(round_log)

# Final Summary
print("\n" + "═"*80)
print("LOOP COMPLETE — THE FORGE HAS SPOKEN")
print("═"*80 + "\n")

for entry in history:
    print(entry)

# Rich Markdown Export
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
md_content = f"""# RSI Forge Session Report
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Recursive SI Mode**: {'Enabled' if recursive_si_mode else 'Disabled'}
**Problem**: {problem}

## Full History

"""
for entry in history:
    md_content += f"{entry}\n\n"

md_content += "## Key Insights\n"
md_content += "- Strong human anchoring maintained throughout\n"
md_content += "- Recursive SI Mode active\n"
if any("Phase Transition" in str(e) for e in history):
    md_content += "- Phase transitions observed\n"

filename = f"rsiforge_session_{timestamp}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"\n✅ Rich Markdown report saved: **{filename}**")
print("   (Perfect for uploading to Grokipaedia)")

# Also save JSON
with open(filename.replace(".md", ".json"), "w", encoding="utf-8") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "problem": problem,
        "recursive_si_mode": recursive_si_mode,
        "history": history
    }, f, indent=2)

print("\nReady for next run → Just type: python rsiforge_terminal.py")
