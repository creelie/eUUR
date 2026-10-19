# check.jl -- the constants q*, C* and m in 256-bit BigFloat arithmetic.
#
# q* is the root in (0.69, 0.70) of Phi(q) = (1-q)ln(1-q) + q ln(1+q).  The script
# checks the sign change of Phi, the three expressions for C*,
#   1/2 - f(q*)/ln 2,  1/2 - (1-q*)ln(1+q*)/(2 ln 2),  1 - m with m = 1/2 + f(q*)/ln 2,
# where f(q) = q h(q) - h(q^2)/2, the identity r(q,q) = 1/2 on (1/2, 1/sqrt 2), and the
# gaps between C* and the earlier certified constants.
setprecision(BigFloat, 256)
h(x) = -(x * log(x) + (1 - x) * log(1 - x))
Phi(q) = (1 - q) * log(1 - q) + q * log(1 + q)
# Newton on Phi uses Phi'(q) = -ln(1-q) - 1 + ln(1+q) + q/(1+q)
q = BigFloat("0.69")
for _ in 1:40
    global q -= Phi(q) / (-log(1 - q) - 1 + log(1 + q) + q / (1 + q))
end
lo, hi = q - big"1e-70", q + big"1e-70"
@assert sign(Phi(lo)) != sign(Phi(hi)) "no sign change at q*"
f(x) = x * h(x) - h(x^2) / 2
L = log(BigFloat(2))
c1 = 1 / BigFloat(2) - f(q) / L
c2 = 1 / BigFloat(2) - (1 - q) * log(1 + q) / (2L)
m = 1 / BigFloat(2) + f(q) / L
@assert abs(c1 - c2) < big"1e-70"
@assert abs((1 - m) - c1) < big"1e-70"
a(x) = sqrt((1 - 2x^2) / (2x * (1 - x)))
for x in (BigFloat("0.55"), BigFloat("0.6"), q, BigFloat("0.7"))
    r = x^2 + a(x)^2 * (x - x^2)
    @assert abs(r - 1 / BigFloat(2)) < big"1e-70"
end
println("q* = ", string(q)[1:42])
println("C* = ", string(c1)[1:42])
println("m  = ", string(m)[1:42])
for (name, c) in (("Liu (numerical threshold)", big"0.382709087918735"),
                  ("Costa-Sadhu", big"0.3828852549667978"),
                  ("Jiang", big"1531541" / big"4000000"))
    println(rpad(name, 28), " C* - c = ", Float64(c1 - c))
end
println("Julia check passed")
