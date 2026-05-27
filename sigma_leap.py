"""
Sigma-Leap Integrator — RSI Forge Session 20
============================================
Agent SIGMA's specification:
- Symplectic corrector base
- Adaptive step size controller
- Division-by-zero protection (no softening)
- Commits to 100,000 steps below 1e-4 energy error

Author: RSI Forge Collective (Agent SIGMA)
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

def accelerations(x):
    r12 = np.linalg.norm(x[1]-x[0])
    r13 = np.linalg.norm(x[2]-x[0])
    r23 = np.linalg.norm(x[2]-x[1])
    if min(r12,r13,r23) < 1e-10:
        raise ValueError(f"Near-collision: min separation {min(r12,r13,r23):.3e}")
    ax1 = G*m*(x[1]-x[0])/r12**3 + G*m*(x[2]-x[0])/r13**3
    ax2 = G*m*(x[0]-x[1])/r12**3 + G*m*(x[2]-x[1])/r23**3
    ax3 = G*m*(x[0]-x[2])/r13**3 + G*m*(x[1]-x[2])/r23**3
    return np.array([ax1, ax2, ax3])

def total_energy(x, v):
    KE = 0.5*m*(np.dot(v[0],v[0])+np.dot(v[1],v[1])+np.dot(v[2],v[2]))
    r12=np.linalg.norm(x[1]-x[0])
    r13=np.linalg.norm(x[2]-x[0])
    r23=np.linalg.norm(x[2]-x[1])
    PE=-G*m*m/r12-G*m*m/r13-G*m*m/r23
    return KE+PE

def sigma_leap_step(x, v, dt):
    """Leapfrog (Verlet) symplectic integrator with adaptive step size."""
    acc = accelerations(x)
    # Half-step velocity
    v_half = v + 0.5*dt*acc
    # Full-step position
    x_new = x + dt*v_half
    # New acceleration
    acc_new = accelerations(x_new)
    # Half-step velocity complete
    v_new = v_half + 0.5*dt*acc_new
    return x_new, v_new

def adaptive_dt(x, v, dt_base=0.001, dt_min=1e-6, dt_max=0.01):
    """Adaptive step size: shrink near close approaches."""
    r12=np.linalg.norm(x[1]-x[0])
    r13=np.linalg.norm(x[2]-x[0])
    r23=np.linalg.norm(x[2]-x[1])
    min_r = min(r12,r13,r23)
    # Scale dt with minimum separation
    dt = dt_base * min(1.0, min_r**1.5)
    return max(dt_min, min(dt_max, dt))

def simulate_sigma_leap(num_steps=100000):
    x = x0.copy(); v = v0.copy()
    E0 = total_energy(x, v)
    p0 = m*(v[0]+v[1]+v[2])
    
    energy_errors = []
    momentum_errors = []
    
    print("Sigma-Leap Integrator")
    print("="*45)
    print(f"Committed steps: 100,000 | Target: energy error < 1e-4")
    print()
    
    halted = num_steps
    for i in range(num_steps):
        dt = adaptive_dt(x, v)
        try:
            x, v = sigma_leap_step(x, v, dt)
        except ValueError as e:
            print(f"💥 {e} at step {i}")
            halted = i; break
        
        E = total_energy(x, v)
        p = m*(v[0]+v[1]+v[2])
        ee = abs((E-E0)/E0)
        me = np.linalg.norm(p-p0)
        energy_errors.append(ee)
        momentum_errors.append(me)
        
        if np.isnan(ee) or ee > 1e-4:
            print(f"⚠️  Energy threshold at step {i}: {ee:.3e}")
            halted = i; break
        
        if i in [499, 4999, 9999, 49999, 99999]:
            print(f"Step {i+1:>7}: energy={ee:.3e}  momentum={me:.3e}")
    
    if halted == num_steps:
        print(f"\n✅ SIGMA-LEAP HELD {num_steps} STEPS")
    else:
        print(f"\n❌ Failed at step {halted}")
    
    return energy_errors, momentum_errors, halted

if __name__ == "__main__":
    ee, me, halted = simulate_sigma_leap()
    print(f"\nFinal energy error: {ee[-1]:.3e}")
    print(f"Final momentum error: {me[-1]:.3e}")
