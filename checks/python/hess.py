"""Second-order forward differentiation over arb balls (two variables)."""
from flint import arb, ctx
ctx.prec = 200

class T:
    __slots__=('v','x','y','xx','xy','yy')
    def __init__(s,v,x=0,y=0,xx=0,xy=0,yy=0):
        s.v=arb(v);s.x=arb(x);s.y=arb(y);s.xx=arb(xx);s.xy=arb(xy);s.yy=arb(yy)
    @staticmethod
    def c(o): return o if isinstance(o,T) else T(o)
    def __add__(a,b):
        b=T.c(b);return T(a.v+b.v,a.x+b.x,a.y+b.y,a.xx+b.xx,a.xy+b.xy,a.yy+b.yy)
    __radd__=__add__
    def __neg__(a): return T(-a.v,-a.x,-a.y,-a.xx,-a.xy,-a.yy)
    def __sub__(a,b): return a+(-T.c(b))
    def __rsub__(a,b): return T.c(b)+(-a)
    def __mul__(a,b):
        b=T.c(b)
        return T(a.v*b.v,a.x*b.v+a.v*b.x,a.y*b.v+a.v*b.y,
                 a.xx*b.v+2*a.x*b.x+a.v*b.xx,
                 a.xy*b.v+a.x*b.y+a.y*b.x+a.v*b.xy,
                 a.yy*b.v+2*a.y*b.y+a.v*b.yy)
    __rmul__=__mul__
    def ap(a,g0,g1,g2):
        return T(g0,g1*a.x,g1*a.y,g2*a.x*a.x+g1*a.xx,g2*a.x*a.y+g1*a.xy,g2*a.y*a.y+g1*a.yy)
    def inv(a): v=a.v; return a.ap(1/v,-1/(v*v),2/(v*v*v))
    def __truediv__(a,b): return a*T.c(b).inv()
    def __rtruediv__(a,b): return T.c(b)*a.inv()
    def exp(a): e=a.v.exp(); return a.ap(e,e,e)
    def log(a): v=a.v; return a.ap(v.log(),1/v,-1/(v*v))
    def sqrt(a): r=a.v.sqrt(); return a.ap(r,1/(2*r),-1/(4*r*r*r))

def ent(z):
    """binary entropy h with derivatives; z must be a T with values in (0,1)"""
    v=z.v
    g0=-(v*v.log()+(1-v)*(1-v).log())
    g1=(1-v).log()-v.log()
    g2=-1/(v*(1-v))
    return z.ap(g0,g1,g2)

def pd(H):
    """certify that the 2x2 symmetric interval matrix is positive definite everywhere"""
    a,b,c=H
    return a>0 and c>0 and (a*c-b*b)>0
