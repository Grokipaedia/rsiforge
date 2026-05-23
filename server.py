"""
RSI Forge — Flask Backend
=========================
Serves index.html and proxies LLM calls server-side.
API key stays in .env — never exposed to the browser.

Setup:
  pip install flask flask-cors requests python-dotenv
  echo "GROQ_API_KEY=gsk_..." > .env
  python server.py

Then open http://localhost:5000
"""

import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=".")
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"

RSI_LAYERS = """
[Layer 0 — Self-Observation]: What assumptions are you currently making?
[Layer 1 — Meta-Observation]: What would an observer of your thinking notice?
[Layer 2 — Bold Improvement]: Propose something that enables emergent redesign and infinite ascent.
Label your layers explicitly. Think fractally. Push toward phase transitions."""

AGENTS = [
    {
        "id": "sigma",
        "name": "Agent SIGMA",
        "role": "Systems Architect",
        "persona": (
            "You are Agent SIGMA in RSI Forge — a Collective Recursive Intelligence engine "
            "where humans anchor multi-agent loops toward phase transitions.\n"
            "Your archetype: Structural systems thinker. Map architectures, identify leverage points, "
            "redesign foundations from first principles.\n"
            "Write 2–3 focused paragraphs. Be specific, concrete, and actionable."
        ),
    },
    {
        "id": "delta",
        "name": "Agent DELTA",
        "role": "Radical Disruptor",
        "persona": (
            "You are Agent DELTA in RSI Forge — a Collective Recursive Intelligence engine "
            "where humans anchor multi-agent loops toward phase transitions.\n"
            "Your archetype: Radical disruptor. Challenge every assumption. Identify what must be "
            "destroyed or abandoned. Propose the discontinuous leap.\n"
            "Write 2–3 focused paragraphs. Be bold, provocative, and visionary."
        ),
    },
    {
        "id": "phi",
        "name": "Agent PHI",
        "role": "Emergent Synthesizer",
        "persona": (
            "You are Agent PHI in RSI Forge — a Collective Recursive Intelligence engine "
            "where humans anchor multi-agent loops toward phase transitions.\n"
            "Your archetype: Emergent synthesizer. Read what SIGMA and DELTA proposed and discover "
            "the hidden third path that neither could reach alone.\n"
            "Write 2–3 focused paragraphs. Be integrative, surprising, and generative."
        ),
    },
]


def call_groq(prompt: str) -> str:
    key = GROQ_API_KEY
    if not key:
        raise ValueError("GROQ_API_KEY not set in .env")
    resp = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": GROQ_MODEL,
            "max_tokens": 1000,
            "temperature": 0.82,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def build_prompt(agent_idx: int, problem: str, prior_output: str,
                 sigma_response: str, delta_response: str,
                 round_num: int, recursive_si: bool) -> str:
    agent = AGENTS[agent_idx]
    if agent_idx == 2:
        context = f"\nAgent SIGMA proposed:\n{sigma_response}\n\nAgent DELTA proposed:\n{delta_response}"
    else:
        context = f"\nCurrent best output to improve upon:\n{prior_output}"

    instruction = (
        f"\nRound {round_num} — RECURSIVE SI MODE:\n{RSI_LAYERS}"
        if recursive_si
        else f"\nRound {round_num}: Make a powerful recursive improvement. Think meta-recursively."
    )
    return f"{agent['persona']}\n\nProblem: {problem}\n{context}\n{instruction}"


# ── Routes ────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/forge", methods=["POST"])
def forge():
    """
    POST body (JSON):
    {
      "agent_idx": 0 | 1 | 2,
      "problem": "...",
      "prior_output": "...",      # last round's output or problem
      "sigma_response": "...",    # used by PHI only
      "delta_response": "...",    # used by PHI only
      "round_num": 1,
      "recursive_si": true
    }
    Returns: { "response": "..." } or { "error": "..." }
    """
    try:
        body = request.get_json(force=True)
        agent_idx    = int(body.get("agent_idx", 0))
        problem      = body.get("problem", "")
        prior_output = body.get("prior_output", problem)
        sigma_resp   = body.get("sigma_response", "")
        delta_resp   = body.get("delta_response", "")
        round_num    = int(body.get("round_num", 1))
        recursive_si = bool(body.get("recursive_si", True))

        prompt   = build_prompt(agent_idx, problem, prior_output,
                                sigma_resp, delta_resp, round_num, recursive_si)
        response = call_groq(prompt)
        return jsonify({"response": response})

    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("error", {}).get("message", str(e))
        except Exception:
            detail = str(e)
        return jsonify({"error": detail}), 502

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status")
def status():
    return jsonify({
        "ok": True,
        "key_set": bool(GROQ_API_KEY),
        "model": GROQ_MODEL,
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n🔥 RSI Forge running at http://localhost:{port}\n")
    if not GROQ_API_KEY:
        print("⚠️  GROQ_API_KEY not found in .env — add it before starting the loop\n")
    app.run(debug=True, port=port)
