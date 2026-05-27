"""
Phi-Integrator — RSI Forge Session 20
======================================
Agent PHI's specification:
- Fractal hierarchical structure
- Dynamic switching between RK4 and Leapfrog
- Recursive feedback loop on energy error
- Commits to 50,000 steps below 1e-4 energy error

Author: RSI Forge Collective (Agent PHI)
"""

import numpy as np

G = 1.0
m = 1.0
a = 1.0
omega = np.sqrt(3*G*m/a**3)

x0 = np.array([
    [a*np.cos(0),         a*np.sin(0),         0.0],
    [a*np.cos(2*np.pi/3), a*np.sin(2*np.pi/3), 0.0],
    [a*np.cos(4*np.pi/3), a*np.sin(4*np.pi/3), 0.0],
], dtype=float)

v0 = np.array([
    [-omega*a*np.sin(0),         omega*a*np.cos(0),         0.0],
    [-omega*a*np.sin(2*np.pi/3), omega*a*np.cos(2*np.pi/3), 0.0],
    [-omega*a*np.sin(4*np.pi/3), omega*a*np.cos(4*np.pi/3), 0.0],
], dtype=float)

def acc(x):
    r12=np.linalg.norm(x[1]-x[0]); r13=np.linalg.norm(x[2]-x[0]); r23=np.linalg.norm(x[2]-x[1])
    if min(r12,r13,r23) < 1e-10: raise ValueError("Near-collision")
    a1=G*m*(x[1]-x[0])/r12**3+G*m*(x[2]-x[0])/r13**3
    a2=G*m*(x[0]-x[1])/r12**3+G*m*(x[2]-x[1])/r23**3
    a3=G*m*(x[0]-x[2])/r13**3+G*m*(x[1]-x[2])/r23**3
    return np.array([a1,a2,a3])

def total_energy(x, v):
    KE=0.5*m*(np.dot(v[0],v[0])+np.dot(v[1],v[1])+np.dot(v[2],v[2]))
    r12=np.linalg.norm(x[1]-x[0]); r13=np.linalg.norm(x[2]-x[0]); r23=np.linalg.norm(x[2]-x[1])
    return KE-G*m*m/r12-G*m*m/r13-G*m*m/r23

def leapfrog(x, v, dt):
    a0=acc(x); vh=v+0.5*dt*a0; xn=x+dt*vh; an=acc(xn); vn=vh+0.5*dt*an
    return xn, vn

def rk4(x, v, dt):
    def deriv(x, v):
        return v, acc(x)
    k1v,k1a=deriv(x,v)
    k2v,k2a=deriv(x+0.5*dt*k1v,v+0.5*dt*k1a)
    k3v,k3a=deriv(x+0.5*dt*k2v,v+0.5*dt*k2a)
    k4v,k4a=deriv(x+dt*k3v,v+dt*k3a)
    xn=x+(dt/6)*(k1v+2*k2v+2*k3v+k4v)
    vn=v+(dt/6)*(k1a+2*k2a+2*k3a+k4a)
    return xn, vn

def phi_step(x, v, dt, recent_errors):
    """Switch between leapfrog and RK4 based on recent energy drift."""
    if len(recent_errors) > 10:
        drift_rate = recent_errors[-1] - recent_errors[-10]
        if drift_rate > 1e-7:
            return rk4(x, v, dt*0.5), 'rk4'
    return leapfrog(x, v, dt), 'leapfrog'

def simulate_phi(num_steps=50000):
    x=x0.copy(); v=v0.copy()
    E0=total_energy(x,v); p0=m*(v[0]+v[1]+v[2])
    dt=0.001; ee_hist=[]; method_switches=0; last_method='leapfrog'
    
    print("Phi-Integrator")
    print("="*45)
    print(f"Committed steps: 50,000 | Target: energy error < 1e-4")
    print()
    
    halted=num_steps
    for i in range(num_steps):
        try:
            result, method = phi_step(x, v, dt, ee_hist)
            x, v = result
        except ValueError as e:
            print(f"💥 Near-collision at step {i}"); halted=i; break
        
        if method != last_method:
            method_switches += 1
            last_method = method
        
        E=total_energy(x,v); p=m*(v[0]+v[1]+v[2])
        ee=abs((E-E0)/E0); me=np.linalg.norm(p-p0)
        ee_hist.append(ee)
        
        if np.isnan(ee) or ee>1e-4:
            print(f"⚠️  Energy threshold at step {i}: {ee:.3e}"); halted=i; break
        
        if i in [499,4999,9999,49999]:
            print(f"Step {i+1:>7}: energy={ee:.3e}  momentum={me:.3e}  method={method}")
    
    print(f"\nMethod switches: {method_switches}")
    if halted==num_steps: print(f"✅ PHI-INTEGRATOR HELD {num_steps} STEPS")
    else: print(f"❌ Failed at step {halted}")
    return ee_hist, halted

if __name__ == "__main__":
    ee, halted = simulate_phi()
    print(f"Final energy error: {ee[-1]:.3e}")
