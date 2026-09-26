from __future__ import annotations
import cmath
from dataclasses import dataclass

A=cmath.rect(1,2*3.141592653589793/3)

@dataclass(frozen=True)
class PhaseValues:
    a: complex
    b: complex
    c: complex


def symmetrical_components(v:PhaseValues):
    zero=(v.a+v.b+v.c)/3
    pos=(v.a+A*v.b+A*A*v.c)/3
    neg=(v.a+A*A*v.b+A*v.c)/3
    return zero,pos,neg


def sequence_to_phase(zero:complex,pos:complex,neg:complex):
    va=zero+pos+neg
    vb=zero+A*A*pos+A*neg
    vc=zero+A*pos+A*A*neg
    return PhaseValues(va,vb,vc)


def voltage_unbalance_percent(v:PhaseValues):
    _,pos,neg=symmetrical_components(v)
    return 0.0 if abs(pos)==0 else 100*abs(neg)/abs(pos)


def neutral_current(i:PhaseValues): return -(i.a+i.b+i.c)


def phase_power_kw(v:PhaseValues,i:PhaseValues):
    vals=[]
    for vv,ii in [(v.a,i.a),(v.b,i.b),(v.c,i.c)]: vals.append((vv*ii.conjugate()).real/1000)
    return tuple(vals)


def apply_phase_impedance(source:PhaseValues,current:PhaseValues,z:PhaseValues):
    return PhaseValues(source.a-current.a*z.a,source.b-current.b*z.b,source.c-current.c*z.c)


def max_phase_deviation(values:PhaseValues):
    mags=[abs(values.a),abs(values.b),abs(values.c)]; avg=sum(mags)/3
    return max(abs(x-avg) for x in mags)
