import numpy as np
import re
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple

def let_f(du: str) -> Callable[[float, float], float]:
    """Parses a string equation into a callable function."""
    du = du.replace("sqrt", "np.sqrt").replace("^", "**")
    du = re.sub(r"(\d)([A-Za-z])", r"\1*\2", du)  # Ensure multiplication is explicit

    def f(t, u):
        return eval(du, {"t": t, "u": u, "np": np})

    return f

def standard_eulers_method(du, f, t0, u0, h, n, plot=True, return_steps=False):
    t_vals = [t0]
    u_vals = [u0]
    steps = [(t0, u0)]  # To store the steps

    for i in range(1, n + 1):
        t_new = t_vals[-1] + h
        u_new = u_vals[-1] + h * f(t_vals[-1], u_vals[-1])
        
        t_vals.append(t_new)
        u_vals.append(u_new)
        
        steps.append((t_new, u_new))  # Save each step

    if return_steps:
        return steps  # Return the steps if needed

    if plot:
        plot_results(t_vals, u_vals, "Standard Euler's Method")  # Plot if needed
    return t_vals, u_vals


def improved_eulers_method(du: str, f: Callable[[float, float], float], t0: float, u0: float, h: float, n: int, plot=True, return_steps=False) -> Tuple[List[float], List[float]]:
    """Runs the improved Euler’s method and returns computed points."""
    t_values, u_values = [t0], [u0]
    steps = [(t0, u0)]  # To store the steps

    for _ in range(n):
        w = u0 + h * f(t0, u0)  # Predictor step
        u0 = u0 + (h / 2) * (f(t0, u0) + f(t0 + h, w))  # Corrector step
        t0 += h
        t_values.append(t0)
        u_values.append(u0)

        steps.append((t0, u0))

    if return_steps:
        return steps  # Return the steps if needed

    if plot:
        plot_results(t_values, u_values, "Improved Euler's Method")
    return t_values, u_values

def plot_results(t_values: List[float], u_values: List[float], title: str):
    """Plots the computed numerical results."""
    plt.figure(figsize=(8, 5))
    plt.plot(t_values, u_values, marker='o', linestyle='-', label="Approximation")
    plt.xlabel("t")
    plt.ylabel("u(t)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_comparison(t_std: List[float], u_std: List[float], t_imp: List[float], u_imp: List[float]):
    """Plots both Euler methods for comparison on the same graph."""
    plt.figure(figsize=(8, 5))
    plt.plot(t_std, u_std, marker='o', linestyle='-', label="Standard Euler")
    plt.plot(t_imp, u_imp, marker='s', linestyle='--', label="Improved Euler", color='r')
    plt.xlabel("t")
    plt.ylabel("u(t)")
    plt.title("Comparison: Standard vs. Improved Euler's Method")
    plt.legend()
    plt.grid(True)
    plt.show()

