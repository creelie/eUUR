"""Certify the tangency of (K) and (M) at (q*, q*).

At the point (q*, q*) both gaps and their gradients vanish (exactly, by the identities in the
paper; here as balls of radius below 1e-30).  On every subbox of an n x n subdivision of
[q*-R, q*+R]^2 the Hessian is enclosed by second-order forward differentiation over arb balls
and certified positive definite.  A function with a positive definite Hessian on a convex set,
zero value and zero gradient at an interior point, is nonnegative there.
Usage: python3 tangency.py [R] [n]   (default 0.008 40). Requires python-flint.
"""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, ctx
from hess import T, ent, pd
ctx.prec=200
LN2=arb(2).log()
def fprime(q): return -((1-q)*(1-q).log()+q*(1+q).log())
# isolate q*: f' > 0 then < 0 (unique root by Jiang's argument)
lo,hi=arb('0.69'),arb('0.6911')
assert fprime(lo)>0 and fprime(hi)<0
for _ in range(120):
    mid=(lo+hi)/2; mid=arb(mid.mid())
    s=fprime(mid)
    if s>0: lo=mid
    elif s<0: hi=mid
    else: break
QS=lo.union(hi)
def hh(z): return -(z*z.log()+(1-z)*(1-z).log())
HSTAR=hh(QS); KSTAR=((1-QS).log()-QS.log())/(2*HSTAR)
fq=QS*hh(QS)-hh(QS*QS)/2
MW4=fq/LN2          # m*w4 = m-1/2 = 1/2 - C*
CSTAR=arb(1)/2-MW4
print('q* =',QS.str(30)); print('C* =',CSTAR.str(30))
def phi(x):   # valid for x in [1/2, 181/256]
    d=x-QS
    E=-KSTAR*d-arb('0.7')*d*d
    return (LN2*ent(x)/HSTAR).sqrt()*E.exp()
def acoef(x): return ((1-2*x*x)/(2*x*(1-x))).sqrt()
def Kgap(x,y,which):
    mn = x if which==1 else y
    r=x*y+acoef(x)*acoef(y)*(mn-x*y)
    return ent(r)-phi(x)*phi(y)
def Mgap(x,y):
    return ent(x*y)+2*MW4*phi(x)*phi(y)-x*ent(y)-y*ent(x)
def check(F,R,n):
    c=QS.mid(); bad=0; worst=None
    for i in range(n):
        for j in range(n):
            xl=c-R+2*R*i/n; xh=c-R+2*R*(i+1)/n
            yl=c-R+2*R*j/n; yh=c-R+2*R*(j+1)/n
            X=T(arb(xl).union(arb(xh)),1,0); Y=T(arb(yl).union(arb(yh)),0,1)
            v=F(X,Y)
            if not pd((v.xx,v.xy,v.yy)):
                bad+=1
    return bad
if __name__=='__main__':
    R=arb(sys.argv[1]) if len(sys.argv)>1 else arb('0.008'); n=int(sys.argv[2]) if len(sys.argv)>2 else 40
    # values at the tangency point
    X=T(QS,1,0);Y=T(QS,0,1)
    for name,F in [('K1',lambda x,y:Kgap(x,y,1)),('K2',lambda x,y:Kgap(x,y,2)),('M',Mgap)]:
        v=F(X,Y); print(name,'value',v.v.str(5),'grad',v.x.str(5),v.y.str(5),'hess',v.xx.str(5),v.xy.str(5),v.yy.str(5))
        assert v.v.contains(0) and v.x.contains(0) and v.y.contains(0), name
        assert abs(v.v).upper() < arb('1e-30') and abs(v.x).upper() < arb('1e-30') and abs(v.y).upper() < arb('1e-30'), name
        bad=check(F,R,n)
        print(name,'non-PD subboxes:',bad)
        assert bad==0, name
    print('tangency: (K) for both branches of min and (M) are convex on [q*-R, q*+R]^2 with R =', R.str(5))
