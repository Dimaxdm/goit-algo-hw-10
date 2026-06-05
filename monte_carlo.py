"""
Calculation of a definite integral using the Monte Carlo method
Function: f(x) = x^2, boundaries: [0, 2]
"""
import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
 
# Parameters
np.random.seed(42)
 
def f(x: float | int) -> float | int:
    return x ** 2
 
a = 0           # lower bound 
b = 2           # upper bound
N = 1_000_000   # number of random points
 
# Monte-Carlo methods
x_random = np.random.uniform(a, b, N)
y_random = np.random.uniform(0, f(b), N)
 
under_curve = y_random <= f(x_random)
 
area_rectangle = (b - a) * f(b)     # area of the bounding rectangle
monte_carlo_result = area_rectangle * np.sum(under_curve) / N 
 
# Comparing methods
quad_result, quad_error = spi.quad(f, a, b)
analytical_result = (b**3 - a**3) / 3        # ∫x^2 dx = x^3/3
 
# Results presentation
print(f"Monte-Carlo method (N={N:,}): {monte_carlo_result:.6f}")
print(f"SciPy quad:                       {quad_result:.6f}  (error: {quad_error:.2e})")
print(f"Analytically (x^3/3) from 0 to 2: {analytical_result:.6f}\n")

diff = abs(monte_carlo_result - analytical_result)
print(f"Absolute error of the MC:         {diff:.6f}")
print(f"Relative error of MC:             {diff/analytical_result*100:.4f}%")

 
# Plots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('#0f0f1a')
 
# Plot 1: function +  scattered points
ax = axes[0]
ax.set_facecolor('#0f0f1a')
x = np.linspace(-0.5, 2.5, 400)
ax.plot(x, f(x), color='#ff6b6b', linewidth=2.5, label='f(x) = x²')
ix = np.linspace(a, b, 300)
ax.fill_between(ix, f(ix), color='#6bcfff', alpha=0.25, label='The area under the integral')
 
n_show = 5000
xs, ys = x_random[:n_show], y_random[:n_show]
mask = ys <= f(xs)
ax.scatter(xs[mask],  ys[mask],  s=0.5, color='#6bcfff', alpha=0.4)
ax.scatter(xs[~mask], ys[~mask], s=0.5, color='#ff6b6b',  alpha=0.2)
ax.axvline(x=a, color='#aaa', linestyle='--', alpha=0.6)
ax.axvline(x=b, color='#aaa', linestyle='--', alpha=0.6)
ax.set_xlim([-0.5, 2.5]); ax.set_ylim([0, f(b)+0.2])
ax.set_xlabel('x', color='white') 
ax.set_ylabel('f(x)', color='white')
ax.set_title('Monte-Carlo method\nf(x) = x² from 0 to 2', color='white', fontweight='bold')
ax.tick_params(colors='white')
ax.spines[:].set_color('#333355')
ax.legend(facecolor='#1a1a2e', edgecolor='#444466', labelcolor='white')
info = f'MC ≈ {monte_carlo_result:.4f}\nAnalytical results = {analytical_result:.4f}\nΔ = {diff:.4f}'
ax.text(0.65, 0.97, info, transform=ax.transAxes, verticalalignment='top',
        color='#6bcfff', bbox=dict(facecolor='#1a1a2e', edgecolor='#444466', alpha=0.8))
 
# Figure 2: Convergence
ax2 = axes[1]
ax2.set_facecolor('#0f0f1a')
sizes = np.logspace(1, 6, 60).astype(int)
estimates = [area_rectangle * np.sum(np.random.uniform(0, f(b), n) <= f(np.random.uniform(a, b, n))) / n
             for n in sizes]
ax2.semilogx(sizes, estimates, color='#6bcfff', linewidth=1.5, label='MC assessment')
ax2.axhline(analytical_result, color='#ff6b6b', linestyle='--', linewidth=2,
            label=f'Analytical result = {analytical_result:.4f}')
ax2.fill_between(sizes, analytical_result*0.98, analytical_result*1.02, color='#ff6b6b', alpha=0.1)
ax2.set_xlabel('Number of points (log)', color='white') 
ax2.set_ylabel('Assessment', color='white')
ax2.set_title('Convergence of the Monte Carlo method', color='white', fontweight='bold')
ax2.tick_params(colors='white')
ax2.spines[:].set_color('#333355')
ax2.legend(facecolor='#1a1a2e', edgecolor='#444466', labelcolor='white')
 
plt.tight_layout(pad=2)
plt.show()