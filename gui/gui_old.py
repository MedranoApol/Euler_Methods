import tkinter as tk
from tkinter import messagebox
from methods import standard_eulers_method, improved_eulers_method, let_f, plot_comparison

class EulerMethods:
    def __init__(self, master):
        self.master = master
        master.title("Euler's Method Solver")

        # Labels and input fields
        tk.Label(master, text="Enter u'(t):").grid(row=0, column=0)
        self.du_entry = tk.Entry(master)
        self.du_entry.grid(row=0, column=1)

        tk.Label(master, text="Initial t (t0):").grid(row=1, column=0)
        self.t0_entry = tk.Entry(master)
        self.t0_entry.grid(row=1, column=1)

        tk.Label(master, text="Initial u (u0):").grid(row=2, column=0)
        self.u0_entry = tk.Entry(master)
        self.u0_entry.grid(row=2, column=1)

        tk.Label(master, text="Step Size (h):").grid(row=3, column=0)
        self.h_entry = tk.Entry(master)
        self.h_entry.grid(row=3, column=1)

        tk.Label(master, text="Number of Steps (n):").grid(row=4, column=0)
        self.n_entry = tk.Entry(master)
        self.n_entry.grid(row=4, column=1)

        # Buttons
        tk.Button(master, text="Standard Euler", command=lambda: self.run_euler_method(standard_eulers_method)).grid(row=5, column=0)
        tk.Button(master, text="Improved Euler", command=lambda: self.run_euler_method(improved_eulers_method)).grid(row=5, column=1)
        tk.Button(master, text="Compare Methods", command=self.compare_methods).grid(row=6, column=0, columnspan=2)

    def run_euler_method(self, method):
        """Runs the selected Euler method and plots the results."""
        try:
            du = self.du_entry.get()
            t0 = float(self.t0_entry.get())
            u0 = float(self.u0_entry.get())
            h = float(self.h_entry.get())
            n = int(self.n_entry.get())

            f = let_f(du)
            method(du, f, t0, u0, h, n)  # Calls the numerical method

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def compare_methods(self):
        """Runs both Euler methods and plots them on the same graph for comparison."""
        try:
            du = self.du_entry.get()
            t0 = float(self.t0_entry.get())
            u0 = float(self.u0_entry.get())
            h = float(self.h_entry.get())
            n = int(self.n_entry.get())

            f = let_f(du)
            t_std, u_std = standard_eulers_method(du, f, t0, u0, h, n, plot=False)
            t_imp, u_imp = improved_eulers_method(du, f, t0, u0, h, n, plot=False)
            
            plot_comparison(t_std, u_std, t_imp, u_imp)  # Calls the new comparison plot function

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

