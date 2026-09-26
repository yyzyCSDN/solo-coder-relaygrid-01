from __future__ import annotations

def central_difference(fn,x: float,step: float=1e-3):
    if step<=0: raise ValueError("step")
    return (fn(x+step)-fn(x-step))/(2*step)

def elasticity(base_input: float,base_output: float,derivative: float):
    if base_output==0: return 0.0
    return derivative*base_input/base_output
