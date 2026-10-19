/* check.c -- an independent floating-point check of the construction at C*.
 *
 * It recomputes q*, C*, m, the profile psi, the sampling coefficient a and the
 * two gaps
 *   K(x,y) - psi(x)psi(y)                         (inequality (K))
 *   2m[w0 h(xy) + w4 psi(x)psi(y)] - x h(y) - y h(x)   (inequality (M), m w0 = 1/2)
 * on a 1601 x 1601 grid of [0,1]^2 and reports the smallest values and where they
 * occur.  This is a sanity check in double precision, not a proof: the proof is the
 * interval program checks/python/verify_exact.py with checks/python/tangency.py.
 * Expected: both gaps are >= -1e-12 everywhere; (M) vanishes on the boundary and its
 * minimum over [0.02, 0.98]^2 is within 1e-12 of 0 next to (q*, q*); (K) vanishes at
 * (q*, q*) and, by the equality case h(x^2) = s(x)^2, on the diagonal above x = 0.721.
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double QS, HS, KS, MW4, LN2;
static const double A = 0.716, B = 0.721, Z = 181.0 / 256.0;

static double h(double x) {
  if (x <= 0.0 || x >= 1.0) return 0.0;
  return -(x * log(x) + (1 - x) * log(1 - x));
}
static double fprime(double q) { return -((1 - q) * log(1 - q) + q * log(1 + q)); }
static double fsecond(double q) { return log((1 - q) / (1 + q)) + 1 / (1 + q); }
static double Dfun(double x) {
  if (x <= 0.5) return h(x);
  if (x <= Z) return LN2;
  return LN2 * h(x * x) / h(Z * Z);
}
static double E(double x) { double d = x - QS; return -KS * d - 0.7 * d * d; }
static double phi(double x) { return sqrt(Dfun(x) * h(x) / HS) * exp(E(x)); }
static double s(double x) { return sqrt(h(x * x)); }
static double psi(double x) {
  if (x <= A) return phi(x);
  if (x >= B) return s(x);
  double t = (x - A) / (B - A);
  return (1 - t) * phi(x) + t * s(x);
}
static double acoef(double x) {
  if (x <= 0.5) return 1.0;
  if (x * x >= 0.5) return 0.0;
  return sqrt((1 - 2 * x * x) / (2 * x * (1 - x)));
}
static double Kgap(double x, double y) {
  double mn = x < y ? x : y;
  double r = x * y + acoef(x) * acoef(y) * (mn - x * y);
  return h(r) - psi(x) * psi(y);
}
static double Mgap(double x, double y) {
  return h(x * y) + 2 * MW4 * psi(x) * psi(y) - x * h(y) - y * h(x);
}

int main(void) {
  LN2 = log(2.0);
  QS = 0.69;
  for (int i = 0; i < 60; i++) QS -= fprime(QS) / fsecond(QS);
  HS = h(QS);
  KS = log((1 - QS) / QS) / (2 * HS); /* h'(q*)/(2h(q*)) */
  double f = QS * h(QS) - h(QS * QS) / 2;
  MW4 = f / LN2;
  double cstar = 0.5 - MW4;
  double closed = 0.5 - (1 - QS) * log(1 + QS) / (2 * LN2);
  printf("q*  = %.16f\nC*  = %.16f (closed form %.16f)\nm   = %.16f\n", QS, cstar, closed, 1 - cstar);
  int fail = 0;
  if (fabs(cstar - closed) > 1e-15 || fabs(cstar - 0.3828852599667978) > 1e-14) fail = 1;

  const int n = 1600;
  double kmin = 1e9, mmin = 1e9, kx = 0, ky = 0, mx = 0, my = 0;
  for (int i = 0; i <= n; i++)
    for (int j = 0; j <= n; j++) {
      double x = (double)i / n, y = (double)j / n;
      double k = Kgap(x, y), m = Mgap(x, y);
      if (k < kmin) { kmin = k; kx = x; ky = y; }
      /* (M) vanishes on the boundary of the square; locate its interior minimum */
      if (i >= n / 50 && j >= n / 50 && i <= n - n / 50 && j <= n - n / 50 && m < mmin) { mmin = m; mx = x; my = y; }
      if (m < -1e-12) fail = 1;
    }
  /* the tangency point itself */
  double k0 = Kgap(QS, QS), m0 = Mgap(QS, QS);
  printf("grid minimum of (K) gap %.3e at (%.4f, %.4f)\n", kmin, kx, ky);
  printf("interior minimum of (M) gap %.3e at (%.4f, %.4f)\n", mmin, mx, my);
  printf("gaps at (q*, q*): (K) %.3e, (M) %.3e\n", k0, m0);
  if (kmin < -1e-12 || mmin < -1e-12 || fabs(k0) > 1e-12 || fabs(m0) > 1e-12) fail = 1;
  if (fabs(mx - QS) > 0.01 || fabs(my - QS) > 0.01) fail = 1;
  puts(fail ? "C check FAILED" : "C check passed");
  return fail;
}
