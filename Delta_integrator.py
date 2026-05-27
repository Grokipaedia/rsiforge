"""
DELTA Meta-Integrator — RSI Forge Session 20
=============================================
Agent DELTA's specification:
- Recursive self-modifying architecture
- Fractal hierarchical structure
- Each layer modifies the layer below
- Antagonistic sub-integrators competing for dominance
- Commits to 10,000 steps on Pythagorean problem

Author: RSI Forge Collective (Agent DELTA)
"""

import numpy as np

G = 1.0
m1, m2, m3 = 3.0, 4.0, 5.0

x0 = np.array([[ 1.0, 3.0, 0.0],[-2.0,-1.0, 0.0],[ 1.0,-1.0, 0.0]], dtype=float)
v0 = np.zeros((3,3))

def acc(x):
    r12=np.linalg.norm(x[1]-x[0]); r13=np.linalg.norm(x[2]-x[0]); r23=np.linalg.norm(x[2]-x[1])
    if min(r12,r13,r23)<1e-10: raise ValueError(f"Collision: {min(r12,r13,r23):.3e}")
    a1=G*m2*(x[1]-x[0])/r12**3+G*m3*(x[2]-x[0])/r13**3
    a2=G*m1*(x[0]-x[1])/r12**3+G*m3*(x[2]-x[1])/r23**3
    a3=G*m1*(x[0]-x[2])/r13**3+G*m2*(x[1]-x[2])/r23**3
    return np.array([a1,a2,a3])

def total_energy(x,v):
    KE=0.5*(m1*np.dot(v[0],v[0])+m2*np.dot(v[1],v[1])+m3*np.dot(v[2],v[2]))
    r12=np.linalg.norm(x[1]-x[0]); r13=np.linalg.norm(x[2]-x[0]); r23=np.linalg.norm(x[2]-x[1])
    return KE-G*m1*m2/r12-G*m1*m3/r13-G*m2*m3/r23

def leapfrog(x,v,dt):
    a0=acc(x); vh=v+0.5*dt*a0; xn=x+dt*vh; an=acc(xn)
    return xn, vh+0.5*dt*an

def rk4(x,v,dt):
    def d(x,v): return v, acc(x)
    k1v,k1a=d(x,v)
    k2v,k2a=d(x+0.5*dt*k1v,v+0.5*dt*k1a)
    k3v,k3a=d(x+0.5*dt*k2v,v+0.5*dt*k2a)
    k4v,k4a=d(x+dt*k3v,v+dt*k3a)
    return x+(dt/6)*(k1v+2*k2v+2*k3v+k4v), v+(dt/6)*(k1a+2*k2a+2*k3a+k4a)

def yoshida4(x,v,dt):
    """4th-order Yoshida symplectic integrator — DELTA's third sub-integrator."""
    c1=1/(2-2**(1/3)); c2=-2**(1/3)/(2-2**(1/3))
    d1=c1; d2=c2
    xn=x+c1*dt*v; an=acc(xn); vn=v+d1*dt*an
    xn=xn+c2*dt*vn; an=acc(xn); vn=vn+d2*dt*an
    xn=xn+c1*dt*vn; an=acc(xn); vn=vn+d1*dt*an
    return xn,vn

def delta_meta_step(x, v, dt_base, history, layer=0):
    """
    Recursive meta-integrator: each layer selects the best sub-integrator
    based on recent energy drift history. Layer 0 selects method.
    Layer 1 adjusts timestep. Layer 2 applies correction.
    """
    # Layer 1: adaptive timestep
    r12=np.linalg.norm(x[1]-x[0]); r13=np.linalg.norm(x[2]-x[0]); r23=np.linalg.norm(x[2]-x[1])
    min_r=min(r12,r13,r23)
    dt = max(1e-6, min(dt_base, dt_base * min(1.0, min_r)))

    # Layer 0: antagonistic sub-integrator selection
    if len(history) < 5:
        method = 'leapfrog'
    else:
        recent_drift = history[-1] - history[-5]
        if recent_drift > 1e-7:
            method = 'yoshida4'   # most accurate when drifting
        elif recent_drift > 1e-9:
            method = 'rk4'        # medium accuracy
        else:
            method = 'leapfrog'   # symplectic baseline

    if method == 'leapfrog':
        xn,vn = leapfrog(x,v,dt)
    elif method == 'rk4':
        xn,vn = rk4(x,v,dt)
    else:
        xn,vn = yoshida4(x,v,dt)

    # Layer 2: recursive correction if energy jumped
    if len(history) > 0:
        E_before = history[-1]
        E_after = abs((total_energy(xn,vn) - total_energy(x0,v0)) / total_energy(x0,v0))
        if E_after > E_before * 2 and layer < 2:
            # Retry with half timestep recursively
            xh,vh,_ = delta_meta_step(x,v,dt*0.5,history,layer+1)
            xn,vn,_ = delta_meta_step(xh,vh,dt*0.5,history,layer+1)

    return xn,vn,method

def simulate_delta(num_steps=50000):
    x=x0.copy(); v=v0.copy()
    E0=total_energy(x,v); p0=m1*v[0]+m2*v[1]+m3*v[2]
    ee_hist=[]; method_counts={'leapfrog':0,'rk4':0,'yoshida4':0}

    print("DELTA Meta-Integrator — Pythagorean 3-body")
    print("="*45)
    print(f"Committed steps: 10,000 | Three antagonistic sub-integrators")
    print()

    halted=num_steps
    for i in range(num_steps):
        try:
            x,v,method = delta_meta_step(x,v,0.001,ee_hist)
        except ValueError as e:
            print(f"💥 {e} at step {i}"); halted=i; break
        method_counts[method]+=1
        E=total_energy(x,v); p=m1*v[0]+m2*v[1]+m3*v[2]
        ee=abs((E-E0)/E0); me=np.linalg.norm(p-p0)
        ee_hist.append(ee)
        if np.isnan(ee) or ee>0.01:
            print(f"⚠️  Energy threshold at step {i}: {ee:.3e}"); halted=i; break
        if i in [499,4999,9999,24999,49999]:
            min_r=min(np.linalg.norm(x[1]-x[0]),np.linalg.norm(x[2]-x[0]),np.linalg.norm(x[2]-x[1]))
            print(f"Step {i+1:>7}: energy={ee:.3e}  momentum={me:.3e}  min_sep={min_r:.3f}  method={method}")

    print(f"\nMethod usage: leapfrog={method_counts['leapfrog']} rk4={method_counts['rk4']} yoshida4={method_counts['yoshida4']}")
    if halted==num_steps: print(f"✅ DELTA META-INTEGRATOR HELD {num_steps} STEPS")
    else: print(f"{'✅ Exceeded DELTA commit (10,000)' if halted>10000 else '❌'} — held {halted} steps")
    return ee_hist, halted, method_counts

if __name__ == "__main__":
    ee, halted, methods = simulate_delta()
    print(f"Final energy error: {ee[-1]:.3e}")
