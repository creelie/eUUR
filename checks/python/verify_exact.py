"""Interval verification of the inequalities (K) and (M) at the exact constant C*.

The program is adapted from the interval program in Appendix B of Y. Jiang,
"Entropy bounds and global couplings for union-closed families", arXiv:2609.08291.
The profile is centred at the root q* of (1-q)ln(1-q) + q ln(1+q) = 0, enclosed by a
certified sign change; the scale is sigma = 1; the weights satisfy m w0 = 1/2 and
m w4 = f(q*)/ln 2, so that 1 - m = C*.  Boxes inside the tangency square
[q* - 0.008, q* + 0.008]^2 are accepted because tangency.py certifies there that both
gaps are convex with value and gradient zero at (q*, q*).

Run with Python 3, without -O and with PYTHONOPTIMIZE unset.
Only the Python standard library is required.
"""
from decimal import Decimal as D, Context, ROUND_FLOOR, ROUND_CEILING, getcontext
import json
import os
import time
import hashlib

getcontext().prec = 60
PREC = 35
DOWN = Context(prec=PREC, rounding=ROUND_FLOOR)
UP = Context(prec=PREC, rounding=ROUND_CEILING)


class I:
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        if isinstance(lo, I):
            self.lo, self.hi = lo.lo, lo.hi
            return
        self.lo = lo if isinstance(lo, D) else D(str(lo))
        self.hi = self.lo if hi is None else (hi if isinstance(hi, D) else D(str(hi)))
        assert self.lo <= self.hi

    def __add__(self, other):
        b = I(other)
        return I(DOWN.add(self.lo,b.lo), UP.add(self.hi,b.hi))
    __radd__ = __add__

    def __neg__(self):
        return I(self.hi.copy_negate(), self.lo.copy_negate())

    def __sub__(self, other): return self + (-I(other))
    def __rsub__(self, other): return I(other) + (-self)

    def __mul__(self, other):
        b = I(other)
        pairs = [(a,c) for a in (self.lo,self.hi) for c in (b.lo,b.hi)]
        return I(min(DOWN.multiply(a,c) for a,c in pairs), max(UP.multiply(a,c) for a,c in pairs))
    __rmul__ = __mul__

    def __truediv__(self, other):
        b = I(other)
        assert b.lo > 0 or b.hi < 0, (b.lo,b.hi)
        return self * I(DOWN.divide(D(1),b.hi), UP.divide(D(1),b.lo))

    def __rtruediv__(self, other): return I(other)/self

    def exp(self):
        # Decimal exp/ln/sqrt are correctly rounded to nearest; enlarge one ulp.
        return I(DOWN.next_minus(DOWN.exp(self.lo)), UP.next_plus(UP.exp(self.hi)))

    def log(self):
        assert self.lo > 0
        return I(DOWN.next_minus(DOWN.ln(self.lo)), UP.next_plus(UP.ln(self.hi)))

    def sqrt(self):
        assert self.lo >= 0
        lo = D(0) if self.lo == 0 else DOWN.next_minus(DOWN.sqrt(self.lo))
        return I(lo, UP.next_plus(UP.sqrt(self.hi)))

    def absmax(self): return max(self.lo.copy_abs(),self.hi.copy_abs())

    def midpoint(self): return DOWN.divide(DOWN.add(self.lo,self.hi),D(2))

    def radius(self, center): return max(UP.subtract(center,self.lo),UP.subtract(self.hi,center))

    def width(self): return UP.subtract(self.hi,self.lo)

    def __repr__(self): return f'[{self.lo},{self.hi}]'


ZERO = I(0)
ONE = I(1)
HALF = I('.5')
LOG2 = I(2).log()


def hull(values): return I(min(x.lo for x in values),max(x.hi for x in values))


def hpoint(x):
    z = I(x)
    if z.lo == z.hi and z.lo in (D(0),D(1)): return ZERO
    assert z.lo > 0 and z.hi < 1, z
    return -(z*z.log()+(1-z)*(1-z).log())


def h(z):
    z=I(z)
    assert z.lo >= 0 and z.hi <= 1, z
    a,b=hpoint(z.lo),hpoint(z.hi)
    lower=min(a.lo,b.lo)
    upper=LOG2.hi if z.lo <= D('.5') <= z.hi else max(a.hi,b.hi)
    return I(lower,upper)


def hp(z): return (1-z).log()-z.log()


def fprime(q):
    # f(q)=q h(q)-h(q^2)/2 has f'(q)=-((1-q)ln(1-q)+q ln(1+q)); its unique zero in (0,1) is q*.
    q=I(q)
    return -((1-q)*(1-q).log()+q*(1+q).log())


# q* is enclosed by a certified sign change of f'; the centre of the profile is q* itself.
QLO = D('0.690907738725407754557261116504')
QHI = D('0.690907738725407754557261116506')
assert fprime(QLO).lo > 0 and fprime(QHI).hi < 0
XSTAR = I(QLO,QHI)
HSTAR = h(XSTAR)
KSTAR = hp(XSTAR)/(2*HSTAR)
SIGMA = ONE
XCUT = D(181)/D(256)
CUTH = h(I(XCUT)*I(XCUT))

def Gpoint(u):
    u=I(u)
    if u.lo == u.hi == 0: return ZERO
    x=(-u).exp()
    return h(x)/x


def G(u): return I(Gpoint(u.lo).lo,Gpoint(u.hi).hi)


def GPpoint(u):
    x=(-I(u)).exp()
    return -(1-x).log()/x


def GP(u):
    # G' decreases because G''<0, as follows from its convergent series.
    return I(GPpoint(u.hi).lo,GPpoint(u.lo).hi)



import sys

ZERO=I(0); ONE=I(1)
A=I('.716'); B=I('.721')
# m = 1 - C*, w0 = 1/(2m), w4 = 1 - w0.  Thus m*w0 = 1/2 exactly and m*w4 = m - 1/2 = f(q*)/ln 2.
K0=I('.5')
MW4=(XSTAR*h(XSTAR)-h(XSTAR*XSTAR)/2)/LOG2
M=K0+MW4
CSTAR=1-M
ROOT_HALF=1/I(2).sqrt()
LOW=D(1)/16; HIGH=D(15)/16
TMIN=D('.001'); TMAX=D(16)


def E(x):
    d=x-XSTAR
    return -KSTAR*d-I('.7')*d*d


def EP(x): return -KSTAR-I('1.4')*(x-XSTAR)


def uphi_piece(x,idx):
    hx=h(x)
    if idx==0: dx,dp=hx,hp(x)
    elif idx==1: dx,dp=LOG2,ZERO
    else: dx,dp=LOG2*h(x*x)/CUTH,LOG2*2*x*hp(x*x)/CUTH
    f=SIGMA*(dx*hx/HSTAR).sqrt()*E(x).exp()
    fp=f*(dp/(2*dx)+hp(x)/(2*hx)+EP(x))
    return f,fp


def uphi(x):
    # The input intervals used in compact certificates avoid 0 and 1.
    cuts=[D(0),D('.5'),XCUT,D(1)]
    vals=[];ders=[]
    for j in range(3):
        lo,hi=max(x.lo,cuts[j]),min(x.hi,cuts[j+1])
        if lo<=hi:
             f,fp=uphi_piece(I(lo,hi),j)
             vals.append(f);ders.append(fp)
    return hull(vals),hull(ders)


def sfun(x):
    s=h(x*x).sqrt()
    return s,x*hp(x*x)/s


def psi(x):
    vals=[];ders=[]
    for lo,hi,idx in [(max(x.lo,D(0)),min(x.hi,A.hi),0),
                       (max(x.lo,A.lo),min(x.hi,B.hi),1),
                       (max(x.lo,B.lo),min(x.hi,D(1)),2)]:
        if lo>hi: continue
        xx=I(lo,hi)
        if idx==0: f,fp=uphi(xx)
        elif idx==2: f,fp=sfun(xx)
        else:
            p,pp=uphi(xx);s,sp=sfun(xx)
            z=(xx-A)/(B-A)
            f=(1-z)*p+z*s
            fp=(1-z)*pp+z*sp+(s-p)/(B-A)
        vals.append(f);ders.append(fp)
    return hull(vals),hull(ders)


def Psi(u):
    x=(-u).exp();f,fp=psi(x)
    return f/x,f/x-fp


CMIN=SIGMA/HSTAR.sqrt()*E(I(0)).exp()
CBOTTOM=SIGMA/HSTAR.sqrt()*E(I(LOW)).exp()
LOWPHI=SIGMA*LOG2/HSTAR.sqrt()*E(I('.5')).exp()
CGLOBAL=SIGMA*(2*LOG2/(HSTAR*CUTH)).sqrt()*E(I(1)).exp()
CTOP=SIGMA/I(HIGH)*(LOG2/CUTH*h(I(HIGH)*I(HIGH))*h(I(HIGH))/HSTAR).sqrt()*E(I(1)).exp()


def scalar_checks():
    sa,_=sfun(A);pa,_=uphi(A)
    checks={
      'exponent_increasing':EP(I(1)),
      'top_extension_margin':1-CGLOBAL*CTOP,
      'bottom_low_margin':1-CBOTTOM*LOWPHI,
      'bottom_high_margin':1-2*CBOTTOM*LOWPHI,
      'phi_over_x_decreasing_margin':1-EP(I('.5'))-hp(I(XCUT)*I(XCUT))/CUTH,
      'bridge_small_y_margin':A-sa*CBOTTOM,
      'upper_tail_dominance_at_a':sa-pa,
      'upper_tail_ratio_decreasing_margin':-(hp(A)/(2*h(A))+EP(A)),
      'small_t_margin':2*MW4*(1-(4*I(TMIN)).log())-1,
      'small_t_uses_upper_tail':(-2*I(TMIN)).exp()-B,
      'large_t_margin':MW4*CMIN*CMIN*I(TMAX)-I('.5')
    }
    for key,value in checks.items():
        assert value.lo>0,(key,value)
    return {k:{'lo':str(v.lo),'hi':str(v.hi)} for k,v in checks.items()}


def bridge(y,derivatives=False):
    p,pp=uphi(y);sa,_=sfun(A)
    f=h(A*y)-sa*p
    if derivatives:return f,A*hp(A*y)-sa*pp
    return f


def verify_bridge():
    stack=[I(LOW,A.hi)];n=0;minmargin=None;digest=hashlib.sha256()
    while stack:
        y=stack.pop();n+=1
        if n>100000: raise RuntimeError('Bridge resource limit')
        f,fp=bridge(y,True)
        mid=y.midpoint()
        if f.lo>0:bound=f.lo
        else:
            fc=bridge(I(mid))
            if fc.hi<0:raise ArithmeticError(('bridge negative witness',mid,fc))
            bound=DOWN.subtract(fc.lo,UP.multiply(fp.absmax(),y.radius(mid)))
        if bound>0:
            minmargin=bound if minmargin is None else min(minmargin,bound)
            digest.update(f'{y.lo},{y.hi},{bound}\n'.encode())
        else: stack.extend([I(y.lo,mid),I(mid,y.hi)])
    return {'status':'CERTIFIED','visited':n,'leaves':(n+1)//2,'smallest_lower':str(minmargin),'leaf_sha256':digest.hexdigest()}


# Tangency box around (q*,q*): there (K) and (M) vanish to second order;
# tangency.py certifies positive definite Hessians on it, so these boxes are accepted with bound 0.
TAN=I(UP.subtract(QHI,D('0.008')),DOWN.add(QLO,D('0.008')))  # inside [q*-0.008,q*+0.008]
def in_tan(x,y): return TAN.lo<=x.lo and x.hi<=TAN.hi and TAN.lo<=y.lo and y.hi<=TAN.hi


def coord(t,branch):
    """Map [0,1] to low, middle, or high x ranges; return x,a,dx,da."""
    if branch==0:return I(LOW)+(I('.5')-I(LOW))*t,ONE,I('.5')-I(LOW),ZERO
    if branch==2:return ROOT_HALF+(I(HIGH)-ROOT_HALF)*t,ZERO,I(HIGH)-ROOT_HALF,ZERO
    z=t*t;r=((z-1)*(z-1)+1).sqrt();den=z+r
    x=1/den
    xp=-2*t*(1+(z-1)/r)/(den*den)
    return x,t,xp,ONE


def kernel_gap(t,z,bi,bj,derivatives=False):
    x,a,xp,ap=coord(t,bi);y,b,yp,bp=coord(z,bj)
    lower=I(min(x.lo,y.lo),min(x.hi,y.hi))
    if x.hi<=y.lo: lx,lz=xp,ZERO
    elif y.hi<=x.lo:lx,lz=ZERO,yp
    else: lx,lz=xp*I(0,1),yp*I(0,1)
    q=x*y+a*b*(lower-x*y)
    # For all real arguments: xy<=q<=min(x,y).
    q=I(max(q.lo,D(1)/256),min(q.hi,HIGH))
    px,pdx=uphi(x);py,pdy=uphi(y)
    val=h(q)-px*py
    if not derivatives:return val
    qt=xp*y+ap*b*(lower-x*y)+a*b*(lx-xp*y)
    qz=x*yp+a*bp*(lower-x*y)+a*b*(lz-x*yp)
    return val,hp(q)*qt-pdx*xp*py,hp(q)*qz-px*pdy*yp


def verify_kernel():
    start=time.monotonic();last=start
    stack=[(I(0,1),I(0,1),i,j,0) for i in range(3) for j in range(i,3)]
    n=leaves=tanleaves=0;minmargin=None;maxdepth=0;digest=hashlib.sha256()
    while stack:
        t,z,i,j,depth=stack.pop();n+=1;maxdepth=max(maxdepth,depth)
        if n>500000 or depth>65:raise RuntimeError(('kernel unresolved',n,depth,t,z,i,j))
        try:val,dt,dz=kernel_gap(t,z,i,j,True)
        except AssertionError:val=dt=dz=None
        tm,zm=t.midpoint(),z.midpoint()
        tan=False
        if i==1 and j==1:
            xx,_,_,_=coord(t,1);yy,_,_,_=coord(z,1);tan=in_tan(xx,yy)
        if tan:bound=D(0);tanleaves+=1
        elif val is not None and val.lo>0:bound=val.lo
        else:
            fc=kernel_gap(I(tm),I(zm),i,j)
            if fc.hi<0:raise ArithmeticError(('kernel negative witness',i,j,tm,zm,fc))
            et=UP.multiply(dt.absmax(),t.radius(tm)) if dt else None
            ez=UP.multiply(dz.absmax(),z.radius(zm)) if dz else None
            bound=DOWN.subtract(DOWN.subtract(fc.lo,et),ez) if dt else D('-Infinity')
        if bound>0 or tan:
            leaves+=1
            if not tan:minmargin=bound if minmargin is None else min(minmargin,bound)
            digest.update(f'{i},{j},{t.lo},{t.hi},{z.lo},{z.hi},{bound}\n'.encode())
        else:
            if dt and et>=ez or (not dt and t.width()>=z.width()):
                 stack.extend([(I(t.lo,tm),z,i,j,depth+1),(I(tm,t.hi),z,i,j,depth+1)])
            else:stack.extend([(t,I(z.lo,zm),i,j,depth+1),(t,I(zm,z.hi),i,j,depth+1)])
        now=time.monotonic()
        if now-last>15:
            print(json.dumps({'phase':'kernel','visited':n,'leaves':leaves,'pending':len(stack),'seconds':round(now-start,1)}),flush=True);last=now
    return {'status':'CERTIFIED','visited':n,'leaves':leaves,'tangency_leaves':tanleaves,'max_depth':maxdepth,'smallest_lower':str(minmargin),'leaf_sha256':digest.hexdigest(),'seconds':round(time.monotonic()-start,2)}


def mixture(t,z,derivatives=False):
    u,v=t*(1+z),t*(1-z)
    pu,pup=Psi(u);pv,pvp=Psi(v)
    val=K0*G(2*t)+MW4*pu*pv-(G(u)+G(v))/2
    if not derivatives:return val
    gu,gv=GP(u),GP(v)
    dt=2*K0*GP(2*t)+MW4*((1+z)*pup*pv+(1-z)*pu*pvp)-((1+z)*gu+(1-z)*gv)/2
    dz=t*(MW4*(pup*pv-pu*pvp)-(gu-gv)/2)
    return val,dt,dz


def verify_mixture():
    start=time.monotonic();last=start
    knots=list(map(D,['.001','.01','.1','.3','.5','1','2','4','8','16']))
    stack=[(I(a,b),I(0,1),0) for a,b in zip(knots[:-1],knots[1:])]
    n=leaves=edges=tans=0;minmargin=None;maxdepth=0;digest=hashlib.sha256()
    tail_limit=-B.log()
    while stack:
        t,z,depth=stack.pop();n+=1;maxdepth=max(maxdepth,depth)
        if n>500000 or depth>65:raise RuntimeError(('mixture unresolved',n,depth,t,z))
        vmax=UP.multiply(t.hi,UP.subtract(D(1),z.lo))
        vg=G(I(vmax))
        bound_edge=(K0-I('.5'))*G(2*I(t.lo))-vg/2
        edge2=(2*MW4*CMIN*G(I(t.lo)))
        xx=(-(t*(1+z))).exp();yy=(-(t*(1-z))).exp()
        if in_tan(xx,yy):
            bound=D(0);tans+=1
        elif bound_edge.lo>0:
            bound=bound_edge.lo;edges+=1
        elif vmax<=tail_limit.lo and vg.hi<=(edge2*edge2).lo:
            bound=D(0);edges+=1
        else:
            if (t*(1-z)).lo<=0:
                 mid=z.midpoint();stack.extend([(t,I(z.lo,mid),depth+1),(t,I(mid,z.hi),depth+1)]);continue
            try:val,dt,dz=mixture(t,z,True)
            except AssertionError:val=dt=dz=None
            tm,zm=t.midpoint(),z.midpoint()
            if val is not None and val.lo>0:bound=val.lo
            else:
                 fc=mixture(I(tm),I(zm))
                 if fc.hi<0:raise ArithmeticError(('mixture negative witness',tm,zm,fc))
                 et=UP.multiply(dt.absmax(),t.radius(tm)) if dt else None
                 ez=UP.multiply(dz.absmax(),z.radius(zm)) if dz else None
                 bound=DOWN.subtract(DOWN.subtract(fc.lo,et),ez) if dt else D('-Infinity')
                 if bound<=0:
                     if dt and et>=ez or (not dt and t.width()>=z.width()):
                         stack.extend([(I(t.lo,tm),z,depth+1),(I(tm,t.hi),z,depth+1)])
                     else:stack.extend([(t,I(z.lo,zm),depth+1),(t,I(zm,z.hi),depth+1)])
                     continue
        leaves+=1
        if bound>0:minmargin=bound if minmargin is None else min(minmargin,bound)
        digest.update(f'{t.lo},{t.hi},{z.lo},{z.hi},{bound}\n'.encode())
        now=time.monotonic()
        if now-last>15:
            print(json.dumps({'phase':'mixture','visited':n,'leaves':leaves,'pending':len(stack),'seconds':round(now-start,1)}),flush=True);last=now
    return {'status':'CERTIFIED','visited':n,'leaves':leaves,'edge_leaves':edges,'tangency_leaves':tans,'max_depth':maxdepth,'smallest_lower':str(minmargin),'leaf_sha256':digest.hexdigest(),'seconds':round(time.monotonic()-start,2)}


def main():
    print(json.dumps({'q_star':str(XSTAR),'C_star':str(CSTAR),'m':str(M)}),flush=True)
    selected=sys.argv[1:] or ['scalars','bridge','kernel','mixture']
    functions={'scalars':scalar_checks,'bridge':verify_bridge,'kernel':verify_kernel,'mixture':verify_mixture}
    for name in selected:
        result=functions[name]()
        assert name=='scalars' or result['status']=='CERTIFIED'
        with open(os.path.join(os.environ.get('VERIFY_OUT','.'),f'frankl_exact_cstar_{name}.json'),'w') as f:json.dump(result,f,indent=2)
        print(json.dumps({'phase':name,'result':result}),flush=True)


if __name__=='__main__':main()
