"""
rsiforge-engineer
=================
The RSI Forge operating model as a reusable Python library.

Architecture proven across Sessions 22-25:
  Collective provides structure → Engineer implements → Ground truth anchors next round

Usage:
    from rsiforge_engineer import ForgeSession, Specification, run_benchmark

    session = ForgeSession(problem="N-body Pythagorean 3-body")
    
    spec = Specification(
        agent="PHI",
        formula="dt = (d^-1.3)*(1+d^-0.5)",
        parameters={"alpha": 1.3, "beta": 1.0, "gamma": 0.5},
        commit={"steps": 50000}
    )
    
    result = session.run(spec, benchmark="pythagorean_3body")
    session.report()
"""

import numpy as np
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, Any, Optional, List
from datetime import datetime


# ── DATA STRUCTURES ──────────────────────────────────────────────────────

@dataclass
class Specification:
    """A collective agent's specification — structure without parameters."""
    agent: str                          # SIGMA, DELTA, PHI, or custom
    formula: str                        # Human-readable formula description
    parameters: Dict[str, float]        # Numerical parameters (tunable)
    commit: Dict[str, Any]              # What the agent committed to
    step_fn: Optional[Callable] = None  # Engineer-implemented step function
    notes: str = ""

@dataclass  
class BenchmarkResult:
    """Ground truth result from running a specification."""
    spec: Specification
    actual: Dict[str, Any]              # What actually happened
    committed: Dict[str, Any]           # What was committed
    met_commit: bool                    # Did it meet the commitment?
    beat_baseline: bool                 # Did it beat the baseline?
    baseline: Dict[str, Any]            # Baseline for comparison
    runtime_seconds: float = 0.0
    timestamp: str = ""

    def summary(self):
        lines = [
            f"Agent {self.spec.agent} — {self.spec.formula}",
            f"  Committed: {self.committed}",
            f"  Actual:    {self.actual}",
            f"  Met commit: {'✅' if self.met_commit else '❌'}",
            f"  Beat baseline: {'✅' if self.beat_baseline else '❌'}",
        ]
        return "\n".join(lines)


@dataclass
class ForgeSession:
    """A complete RSI Forge engineering session."""
    problem: str
    session_number: int = 0
    results: List[BenchmarkResult] = field(default_factory=list)
    baseline_result: Optional[Dict] = None

    def run(self, spec: Specification, benchmark: str, **kwargs) -> BenchmarkResult:
        """Run a specification against a benchmark and return ground truth."""
        bench = BENCHMARKS.get(benchmark)
        if bench is None:
            raise ValueError(f"Unknown benchmark: {benchmark}. Available: {list(BENCHMARKS.keys())}")
        
        start = time.time()
        
        # Run baseline if not yet done
        if self.baseline_result is None:
            print(f"Running baseline for {benchmark}...")
            self.baseline_result = bench.run_baseline(**kwargs)
            print(f"  Baseline: {self.baseline_result}")
        
        # Run specification
        if spec.step_fn is None:
            raise ValueError(f"spec.step_fn must be set — the engineer must implement the step function")
        
        print(f"\nRunning {spec.agent} specification...")
        actual = bench.run_spec(spec.step_fn, **kwargs)
        runtime = time.time() - start
        
        # Evaluate
        met = bench.evaluate_commit(actual, spec.commit)
        beat = bench.beats_baseline(actual, self.baseline_result)
        
        result = BenchmarkResult(
            spec=spec,
            actual=actual,
            committed=spec.commit,
            met_commit=met,
            beat_baseline=beat,
            baseline=self.baseline_result,
            runtime_seconds=round(runtime, 2),
            timestamp=datetime.now().isoformat()
        )
        self.results.append(result)
        print(result.summary())
        return result

    def report(self):
        """Print full session report."""
        print(f"\n{'='*55}")
        print(f"RSI FORGE ENGINEER — Session Report")
        print(f"Problem: {self.problem}")
        print(f"{'='*55}")
        print(f"Baseline: {self.baseline_result}")
        print()
        for i, r in enumerate(self.results):
            print(f"[{i+1}] {r.summary()}")
            print()
        
        met = sum(1 for r in self.results if r.met_commit)
        beat = sum(1 for r in self.results if r.beat_baseline)
        print(f"Summary: {met}/{len(self.results)} met commit | {beat}/{len(self.results)} beat baseline")
        
        if beat > 0:
            best = max(self.results, key=lambda r: r.actual.get("steps",0) or -r.actual.get("energy",0))
            print(f"Best result: {best.spec.agent} — {best.actual}")

    def save(self, path: str):
        """Save session to JSON."""
        data = {
            "problem": self.problem,
            "session_number": self.session_number,
            "timestamp": datetime.now().isoformat(),
            "baseline": self.baseline_result,
            "results": [
                {
                    "agent": r.spec.agent,
                    "formula": r.spec.formula,
                    "parameters": r.spec.parameters,
                    "committed": r.committed,
                    "actual": r.actual,
                    "met_commit": r.met_commit,
                    "beat_baseline": r.beat_baseline,
                    "runtime": r.runtime_seconds,
                }
                for r in self.results
            ]
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Session saved to {path}")


# ── BENCHMARKS ───────────────────────────────────────────────────────────

class Benchmark:
    """Base class for all benchmarks."""
    name: str
    description: str

    def run_baseline(self, **kwargs) -> Dict: raise NotImplementedError
    def run_spec(self, step_fn, **kwargs) -> Dict: raise NotImplementedError
    def evaluate_commit(self, actual, commit) -> bool: raise NotImplementedError
    def beats_baseline(self, actual, baseline) -> bool: raise NotImplementedError


class PythagoreanBenchmark(Benchmark):
    """
    Pythagorean 3-body gravitational problem.
    Masses 3,4,5. Start at rest. Chaotic. Guaranteed close approaches.
    Metric: steps held before energy error > 1%.
    """
    name = "pythagorean_3body"
    description = "Chaotic 3-body gravitational problem. Masses 3,4,5."

    G=1.0; m1,m2,m3=3.0,4.0,5.0
    x0=np.array([[1.0,3.0,0.0],[-2.0,-1.0,0.0],[1.0,-1.0,0.0]],dtype=float)
    v0=np.zeros((3,3))

    def _acc(self, x):
        r12=np.linalg.norm(x[1]-x[0]); r13=np.linalg.norm(x[2]-x[0]); r23=np.linalg.norm(x[2]-x[1])
        if min(r12,r13,r23)<1e-10: raise ValueError("Collision")
        a1=self.G*self.m2*(x[1]-x[0])/r12**3+self.G*self.m3*(x[2]-x[0])/r13**3
        a2=self.G*self.m1*(x[0]-x[1])/r12**3+self.G*self.m3*(x[2]-x[1])/r23**3
        a3=self.G*self.m1*(x[0]-x[2])/r13**3+self.G*self.m2*(x[1]-x[2])/r23**3
        return np.array([a1,a2,a3])

    def _energy(self, x, v):
        KE=0.5*(self.m1*np.dot(v[0],v[0])+self.m2*np.dot(v[1],v[1])+self.m3*np.dot(v[2],v[2]))
        r12=np.linalg.norm(x[1]-x[0]); r13=np.linalg.norm(x[2]-x[0]); r23=np.linalg.norm(x[2]-x[1])
        return KE-self.G*self.m1*self.m2/r12-self.G*self.m1*self.m3/r13-self.G*self.m2*self.m3/r23

    def _leapfrog(self, x, v, dt):
        a0=self._acc(x); vh=v+0.5*dt*a0; xn=x+dt*vh; an=self._acc(xn)
        return xn, vh+0.5*dt*an

    def _run(self, step_fn, num_steps=500000):
        x=self.x0.copy(); v=self.v0.copy()
        E0=self._energy(x,v); halted=num_steps; ee=0
        for i in range(num_steps):
            try: x,v=step_fn(x,v,self._acc,self._leapfrog)
            except: halted=i; break
            E=self._energy(x,v); ee=abs((E-E0)/E0)
            if np.isnan(ee) or ee>0.01: halted=i; break
        return {"steps": min(halted,num_steps), "final_energy_error": float(ee)}

    def run_baseline(self, **kwargs):
        def sigma_leap(x,v,acc,leapfrog):
            min_r=min(np.linalg.norm(x[1]-x[0]),np.linalg.norm(x[2]-x[0]),np.linalg.norm(x[2]-x[1]))
            d=max(min_r,0.001); dt=max(1e-6,min(0.001,0.001*d))
            return leapfrog(x,v,dt)
        return self._run(sigma_leap)

    def run_spec(self, step_fn, **kwargs):
        return self._run(step_fn)

    def evaluate_commit(self, actual, commit):
        return actual["steps"] >= commit.get("steps", 0)

    def beats_baseline(self, actual, baseline):
        return actual["steps"] > baseline["steps"]


class ClimateTippingBenchmark(Benchmark):
    """
    Climate tipping point detection.
    dT/dt = αT - βT³ + noise. Detect crossing before it happens.
    Metric: detection accuracy across 100 Monte Carlo trials.
    """
    name = "climate_tipping"
    description = "Climate tipping point detection. 100 Monte Carlo trials."

    def _simulate(self, T0, n_steps=500, dt=0.1, seed=0):
        np.random.seed(seed)
        T=T0; traj=[T]
        for _ in range(n_steps):
            gamma=0.05*np.random.randn()
            T+=( 0.3*T - 0.1*T**3 + gamma)*dt
            traj.append(T)
        return np.array(traj)

    def _run(self, detect_fn, n_trials=100):
        correct=0; actual_crossings=0
        for trial in range(n_trials):
            np.random.seed(trial)
            T0=0.5+0.1*np.random.randn()
            traj=self._simulate(T0,seed=trial)
            actual=any(T>1.4 for T in traj)
            if actual: actual_crossings+=1
            detected,_=detect_fn(traj[:400])
            if detected and actual: correct+=1
        acc=correct/max(actual_crossings,1)
        return {"accuracy": round(acc,3), "trials": n_trials,
                "actual_crossings": actual_crossings, "correct": correct}

    def run_baseline(self, **kwargs):
        def threshold_detect(traj):
            for i,T in enumerate(traj):
                if T>1.0: return True,i
            return False,len(traj)
        return self._run(threshold_detect)

    def run_spec(self, step_fn, **kwargs):
        return self._run(step_fn)

    def evaluate_commit(self, actual, commit):
        return actual["accuracy"] >= commit.get("accuracy", 0)

    def beats_baseline(self, actual, baseline):
        return actual["accuracy"] > baseline["accuracy"]


# ── HELPER FUNCTIONS ─────────────────────────────────────────────────────

def phi_formula_step(alpha=1.3, beta=1.0, gamma=0.5, delta=0.8):
    """
    PHI's Session 23 formula — the breakthrough implementation.
    dt = (d^-alpha)*(1+beta*d^-gamma) with N=floor(d^-delta) sub-steps.
    Achieved 335,679 steps on Pythagorean problem.
    """
    def step(x, v, acc, leapfrog):
        min_r=min(np.linalg.norm(x[1]-x[0]),np.linalg.norm(x[2]-x[0]),np.linalg.norm(x[2]-x[1]))
        d=max(min_r,0.05)
        dt=min(0.001,(d**-alpha)*(1+beta*d**-gamma)*0.00001)
        dt=max(1e-6,dt)
        n=min(256,max(1,int(d**-delta)))
        dt_sub=dt/n
        for _ in range(n): x,v=leapfrog(x,v,dt_sub)
        return x,v
    return step

def sigma_formula_step(alpha=0.9, beta=0.6, gamma=1.1, delta=0.5):
    """
    SIGMA's Session 23 Round 2 formula — 193,923 steps.
    dt = (d^-alpha)/(1+beta*d^-gamma) with N=floor(d^-delta) sub-steps.
    """
    def step(x, v, acc, leapfrog):
        min_r=min(np.linalg.norm(x[1]-x[0]),np.linalg.norm(x[2]-x[0]),np.linalg.norm(x[2]-x[1]))
        d=max(min_r,0.01)
        dt=min(0.001,(d**-alpha)/(1+beta*d**-gamma)*0.0001)
        dt=max(1e-6,dt)
        n=min(128,max(1,int(d**-delta)))
        dt_sub=dt/n
        for _ in range(n): x,v=leapfrog(x,v,dt_sub)
        return x,v
    return step


# ── REGISTRY ─────────────────────────────────────────────────────────────

BENCHMARKS = {
    "pythagorean_3body": PythagoreanBenchmark(),
    "climate_tipping":   ClimateTippingBenchmark(),
}


# ── DEMO ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("rsiforge-engineer — Demo Run")
    print("Operating model: Collective specifies → Engineer implements → Ground truth anchors")
    print("="*60)
    print()

    # Session 23 replay — PHI formula
    session = ForgeSession(
        problem="Pythagorean 3-body — proving the operating model",
        session_number=23
    )

    phi_spec = Specification(
        agent="PHI",
        formula="dt = (d^-1.3)*(1+d^-0.5) with N=floor(d^-0.8) sub-steps",
        parameters={"alpha": 1.3, "beta": 1.0, "gamma": 0.5, "delta": 0.8},
        commit={"steps": 50000},
        step_fn=phi_formula_step(alpha=1.3, beta=1.0, gamma=0.5, delta=0.8),
        notes="PHI's Session 23 formula — achieved 335,679 steps"
    )

    sigma_spec = Specification(
        agent="SIGMA",
        formula="dt = (d^-0.9)/(1+0.6*d^-1.1) with N=floor(d^-0.5) sub-steps",
        parameters={"alpha": 0.9, "beta": 0.6, "gamma": 1.1, "delta": 0.5},
        commit={"steps": 53219},
        step_fn=sigma_formula_step(alpha=0.9, beta=0.6, gamma=1.1, delta=0.5),
        notes="SIGMA's Session 23 Round 2 — achieved 193,923 steps"
    )

    session.run(phi_spec,   "pythagorean_3body")
    session.run(sigma_spec, "pythagorean_3body")
    session.report()
    session.save("/mnt/user-data/outputs/rsiforge_session23.json")

    print()
    print("Add your own benchmark:")
    print("  1. Subclass Benchmark")
    print("  2. Implement run_baseline(), run_spec(), evaluate_commit(), beats_baseline()")
    print("  3. Register in BENCHMARKS dict")
    print("  4. Run ForgeSession.run(spec, 'your_benchmark')")
