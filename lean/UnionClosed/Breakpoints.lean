/-!
# The rational breakpoints of the construction

The profile and the sampling coefficient of the paper change form at the rational
breakpoints `z = 181/256`, `A = 179/250`, `B = 721/1000`, `L = 1/16`, `U = 15/16`.
The analytic arguments use the order relations below; each is a statement about
natural numbers, checked by the Lean kernel with `decide`.  The tangency square
`[q* - 0.008, q* + 0.008]` lies in `(0.682, 0.699)` because `0.690 < q* < 0.691`.
-/

namespace UnionClosed

/-- `z^2 + z > 1` for `z = 181/256`: used to show `D(x) ≥ h(x)` on `[z, 1]`. -/
theorem z_sq_add_z_gt_one : 256 * 256 < 181 * 181 + 181 * 256 := by decide

/-- `z < 1/√2`, i.e. `2 z^2 < 1`. -/
theorem z_lt_inv_sqrt_two : 2 * (181 * 181) < 256 * 256 := by decide

/-- `A > 1/√2`, i.e. `2 A^2 > 1`, so `a = 0` on `[A, 1]`. -/
theorem A_gt_inv_sqrt_two : 250 * 250 < 2 * (179 * 179) := by decide

/-- `U > 1/√2`, so `a = 0` on the upper strip. -/
theorem U_gt_inv_sqrt_two : 16 * 16 < 2 * (15 * 15) := by decide

/-- `1/2 < A < B < 1`. -/
theorem A_B_order : 500 < 716 ∧ 716 < 721 ∧ 721 < 1000 := by decide

/-- The tangency square lies in `[1/2, z]`: `0.682 > 1/2` and `0.699 < 181/256`. -/
theorem tangency_square_in_middle : 500 < 682 ∧ 699 * 256 < 181 * 1000 := by decide

/-- The tangency square lies below `A`: `0.699 < 0.716`. -/
theorem tangency_square_below_A : 699 < 716 := by decide

/-- `1/√2 < 0.7072 < B`, so `ψ = s` (the upper tail) only where `a = 0`. -/
theorem inv_sqrt_two_lt_B : 10000 * 10000 < 2 * (7072 * 7072) ∧ 7072 < 7210 := by decide

end UnionClosed
