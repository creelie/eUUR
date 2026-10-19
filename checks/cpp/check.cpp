// check.cpp -- an independent long-double check of the tangency at (q*, q*).
//
// It computes q* by Newton's method, evaluates the gaps of (K) (both branches of
// min) and (M) near (q*, q*), and estimates value, gradient and Hessian there by
// central differences.  Expected: value and gradient near 0, and the Hessians
// close to the enclosures certified by checks/python/tangency.py:
//   (K): [[4.1700, 0.01125], [0.01125, 4.1700]]
//   (M): [[0.34257, -0.21396], [-0.21396, 0.34257]]
// both positive definite.  Floating point, so a cross-check and not a proof.
#include <cmath>
#include <cstdio>
#include <functional>

using R = long double;
static R QS, HS, KS, MW4;
static const R LN2 = std::log(2.0L);

static R h(R x) { return -(x * std::log(x) + (1 - x) * std::log(1 - x)); }
// On [1/2, 181/256] the profile is phi with D = ln 2, and psi = phi.
static R phi(R x) {
  R d = x - QS;
  return std::sqrt(LN2 * h(x) / HS) * std::exp(-KS * d - 0.7L * d * d);
}
static R acoef(R x) { return std::sqrt((1 - 2 * x * x) / (2 * x * (1 - x))); }
static R K1(R x, R y) { return h(x * y + acoef(x) * acoef(y) * (x - x * y)) - phi(x) * phi(y); }
static R K2(R x, R y) { return h(x * y + acoef(x) * acoef(y) * (y - x * y)) - phi(x) * phi(y); }
static R M(R x, R y) { return h(x * y) + 2 * MW4 * phi(x) * phi(y) - x * h(y) - y * h(x); }

int main() {
  QS = 0.69L;
  for (int i = 0; i < 80; i++) {
    R f1 = -((1 - QS) * std::log(1 - QS) + QS * std::log(1 + QS));
    R f2 = std::log((1 - QS) / (1 + QS)) + 1 / (1 + QS);
    QS -= f1 / f2;
  }
  HS = h(QS);
  KS = std::log((1 - QS) / QS) / (2 * HS);
  MW4 = (QS * h(QS) - h(QS * QS) / 2) / LN2;
  std::printf("q* = %.19Lf   C* = %.19Lf\n", QS, 0.5L - MW4);
  const R e = 1e-4L;
  struct Case { const char *name; std::function<R(R, R)> f; R hxx, hxy; };
  Case cases[] = {{"K, min = x", K1, 4.1700L, 0.011246L},
                  {"K, min = y", K2, 4.1700L, 0.011246L},
                  {"M", M, 0.34257L, -0.21396L}};
  int fail = 0;
  for (auto &c : cases) {
    auto f = c.f;
    R v = f(QS, QS);
    R gx = (f(QS + e, QS) - f(QS - e, QS)) / (2 * e);
    R gy = (f(QS, QS + e) - f(QS, QS - e)) / (2 * e);
    R hxx = (f(QS + e, QS) - 2 * v + f(QS - e, QS)) / (e * e);
    R hyy = (f(QS, QS + e) - 2 * v + f(QS, QS - e)) / (e * e);
    R hxy = (f(QS + e, QS + e) - f(QS + e, QS - e) - f(QS - e, QS + e) + f(QS - e, QS - e)) / (4 * e * e);
    std::printf("%-11s value %+.2Le grad (%+.2Le, %+.2Le) Hessian [[%.5Lf, %.5Lf], [%.5Lf, %.5Lf]]\n",
                c.name, v, gx, gy, hxx, hxy, hxy, hyy);
    bool ok = std::fabs(v) < 1e-15L && std::fabs(gx) < 1e-6L && std::fabs(gy) < 1e-6L &&
              std::fabs(hxx - c.hxx) < 1e-3L && std::fabs(hyy - c.hxx) < 1e-3L &&
              std::fabs(hxy - c.hxy) < 1e-3L && hxx > 0 && hxx * hyy - hxy * hxy > 0;
    if (!ok) fail = 1;
  }
  std::puts(fail ? "C++ check FAILED" : "C++ check passed");
  return fail;
}
