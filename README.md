![Status](https://img.shields.io/badge/status-experimental-blue)
![Stage](https://img.shields.io/badge/stage-research-purple)
![Interface](https://img.shields.io/badge/interface-streamlit-red)
![License](https://img.shields.io/badge/license-MIT-green)

# rsiforge-engineer

The RSI Forge operating model as a reusable Python library.

**The operating model** — proven across Sessions 22-25 in three domains:

> Collective provides structure → Engineer implements → Ground truth anchors next round

## Results

| Session | Domain | Baseline | Best Result | Improvement |
|---------|--------|----------|-------------|-------------|
| 23 | Pythagorean 3-body | 2,142 steps | 335,679 steps | **157x** |
| 24 | Climate tipping point | 100% (threshold) | 100% (threshold) | baseline wins |
| 25 | Protein binding | -16.585 kcal/mol | -16.584 kcal/mol | baseline wins |

## Quick Start

```python
from rsiforge_engineer import ForgeSession, Specification, phi_formula_step

session = ForgeSession(problem="Your problem here", session_number=26)

spec = Specification(
    agent="PHI",
    formula="dt = (d^-1.3)*(1+d^-0.5) with N=floor(d^-0.8) sub-steps",
    parameters={"alpha": 1.3, "beta": 1.0, "gamma": 0.5, "delta": 0.8},
    commit={"steps": 50000},
    step_fn=phi_formula_step(alpha=1.3, beta=1.0, gamma=0.5, delta=0.8),
)

result = session.run(spec, "pythagorean_3body")
session.report()
session.save("my_session.json")
```

## Built-in Benchmarks

- `pythagorean_3body` — Chaotic 3-body gravitational problem (masses 3,4,5)
- `climate_tipping` — Climate tipping point detection (100 Monte Carlo trials)

## Adding a New Benchmark

```python
from rsiforge_engineer import Benchmark, BENCHMARKS

class MyBenchmark(Benchmark):
    name = "my_benchmark"
    
    def run_baseline(self, **kwargs): ...
    def run_spec(self, step_fn, **kwargs): ...
    def evaluate_commit(self, actual, commit): ...
    def beats_baseline(self, actual, baseline): ...

BENCHMARKS["my_benchmark"] = MyBenchmark()
```

## The Finding

The collective generates correct structural specifications with incorrect
numerical parameters. The engineer provides the parameters. The loop
provides the structure. Simple implementations often beat complex ones.

**Domain of validity:**
- ✅ Structural specification of algorithms
- ✅ Order-of-magnitude parameter estimation  
- ✅ Novel concept generation from prior session outputs
- ❌ Exact numerical parameter derivation
- ❌ Implementation-level debugging
- ❌ Knowing when simpler beats complex

## Origin

Built from RSI Forge Sessions 22-25. Full record at rsiforge.com.
Based on Beyond RSI: grokipaedia.com/BeyondRSI.html

The Two Laws:
- Never do: become complacent and attached to existing concepts.
- Never stop: dreaming, imagining, and co-creating the unimaginable.
