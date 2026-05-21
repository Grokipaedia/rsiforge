import random
import json
from datetime import datetime
from forge_engine import run_agent_proposal

# Professional Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(Colors.HEADER + "\n" + "═"*80)
print(" " * 28 + "🔥 RSI FORGE")
print(" " * 20 + "Collective Recursive Intelligence Platform")
print("═"*80 + Colors.END)
print(Colors.CYAN + "Professional Terminal Interface v0.9" + Colors.END + "\n")

# Configuration
problem = input(Colors.BOLD + "Main Problem / Goal:\n> " + Colors.END).strip() or \
          "How should we evolve RSI Forge itself in the next 30 days..."

recursive_si_mode = input(Colors.BOLD + "Enable Recursive SI Mode? (y/n): " + Colors.END).lower().startswith('y')
num_rounds = int(input(Colors.BOLD + "Number of rounds (4-8 recommended): " + Colors.END) or "6")
num_agents = 4

history = [f"Human (Round 0): {problem}"]

print(Colors.GREEN + f"\n🚀 Starting {num_rounds}-round session...\n" + Colors.END)

for r in range(1, num_rounds + 1):
    print(Colors.BLUE + f"\n{'─'*80}" + Colors.END)
    print(Colors.BOLD + f"ROUND {r} {'🔄 RECURSIVE SI MODE' if recursive_si_mode else ''}".center(80) + Colors.END)
    print(Colors.BLUE + f"{'─'*80}" + Colors.END + "\n")
    
    # Agents
    for i in range(num_agents):
        proposal = run_agent_proposal(problem, history[-1], r, recursive_si_mode)
        print(Colors.CYAN + f"Agent {i}:" + Colors.END)
        print(proposal[:700] + ("..." if len(proposal) > 700 else "") + "\n")
    
    # Human Input
    print(Colors.YELLOW + f"🧭 HUMAN ANCHOR INPUT — Round {r}" + Colors.END)
    human_input = input(Colors.BOLD + "\nPaste prompt here > " + Colors.END).strip()
    
    if human_input:
        history.append(f"Human anchor (Round {r}): {human_input}")
        print(Colors.GREEN + "✅ Human anchor recorded\n" + Colors.END)
    else:
        history.append(f"Collective (Round {r}): No input")
        print(Colors.YELLOW + "⚠️ No input\n" + Colors.END)

# Final Summary
print(Colors.HEADER + "\n" + "═"*80)
print(" " * 30 + "SESSION COMPLETE")
print("═"*80 + Colors.END)

print(Colors.BOLD + "\nFULL HISTORY:\n" + Colors.END)
for entry in history:
    print(entry + "\n")

# Save Markdown Report
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
md_content = f"# RSI Forge Session\n\n**Date**: {datetime.now().strftime('%B %d, %Y %H:%M')}\n**Mode**: {'Recursive SI' if recursive_si_mode else 'Standard'}\n\n## History\n\n"
for entry in history:
    md_content += f"{entry}\n\n"

with open(f"RSI_Forge_Session_{timestamp}.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print(Colors.GREEN + f"✅ Professional report saved: RSI_Forge_Session_{timestamp}.md" + Colors.END)
print(Colors.CYAN + "Ready for next run." + Colors.END)
