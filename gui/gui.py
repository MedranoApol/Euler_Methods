import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from methods import standard_eulers_method, improved_eulers_method, let_f, plot_comparison

class EulerMethods:
    def __init__(self, master):
        self.master = master
        master.title("Euler's Method Solver")
        
        tk.Label(master, text="Euler's Method Solver").grid(row=0, column=0, stick="ew")
        tk.Label(master, text="").grid(row=1, column=0)
        # Labels and input fields
        tk.Label(master, text="Enter u'(t):").grid(row=2, column=0)
        self.du_entry = tk.Entry(master)
        self.du_entry.grid(row=2, column=1)

        tk.Label(master, text="Initial t (t0):").grid(row=3, column=0)
        self.t0_entry = tk.Entry(master)
        self.t0_entry.grid(row=3, column=1)

        tk.Label(master, text="Initial u (u0):").grid(row=4, column=0)
        self.u0_entry = tk.Entry(master)
        self.u0_entry.grid(row=4, column=1)

        tk.Label(master, text="Step Size (h):").grid(row=5, column=0)
        self.h_entry = tk.Entry(master)
        self.h_entry.grid(row=5, column=1)

        tk.Label(master, text="Number of Steps (n):").grid(row=6, column=0)
        self.n_entry = tk.Entry(master)
        self.n_entry.grid(row=6, column=1)

        # Buttons
        tk.Button(master, text="Graph of Standard Euler's Method", command=lambda: self.run_euler_method(standard_eulers_method)).grid(row=7, column=0)
        tk.Button(master, text="Graph of Modified Euler's Method", command=lambda: self.run_euler_method(improved_eulers_method)).grid(row=7, column=1)
        tk.Button(master, text="Compare Graph of Methods", command=self.compare_methods).grid(row=8, column=0, columnspan=2)

        # Buttons for showing computation steps
        tk.Button(master, text="Show Standard Euler Steps", command=lambda: self.show_steps(standard_eulers_method)).grid(row=9, column=0)
        tk.Button(master, text="Show Modified Euler Steps", command=lambda: self.show_steps(improved_eulers_method)).grid(row=9, column=1)

        # Frame for the plot
        self.plot_frame = tk.Frame(master)
        self.plot_frame.grid(row=10, column=0, columnspan=2)

        # Frame for the steps
        self.steps_frame = tk.Frame(master)
        self.steps_frame.grid(row=10, column=0, columnspan=2) 

        # Dictionary to store export buttons for graphs and steps
        self.export_buttons = None

        # Initialize figure and method for exporting
        self.current_figure = None
        self.current_method = None

    def run_euler_method(self, method):
        """Runs the selected Euler method and plots the results."""

        # Clear any existing plot in the plot_frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # If steps_frame has been destroyed, recreate it
        if not self.steps_frame.winfo_exists():
            self.steps_frame = tk.Frame(self.master)
            self.steps_frame.grid(row=10, column=0, columnspan=2)

        # Clear any existing steps
        for widget in self.steps_frame.winfo_children():
            widget.destroy()

        try:
            du = self.du_entry.get()
            t0 = float(self.t0_entry.get())
            u0 = float(self.u0_entry.get())
            h = float(self.h_entry.get())
            n = int(self.n_entry.get())

            f = let_f(du)
            t_vals, u_vals = method(du, f, t0, u0, h, n, plot=False)  # Get values without plotting

            self.plot_results(t_vals, u_vals, method)  # Call to display results in Tkinter 
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def show_steps(self, method):
        """Displays the steps for the selected Euler method."""
        # Clear any existing plot in the plot_frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        try:
            du = self.du_entry.get()
            t0 = float(self.t0_entry.get())
            u0 = float(self.u0_entry.get())
            h = float(self.h_entry.get())
            n = int(self.n_entry.get())

            f = let_f(du)
            steps = method(du, f, t0, u0, h, n, plot=False, return_steps=True)  # Get steps without plotting

            # If steps_frame has been destroyed, recreate it
            if not self.steps_frame.winfo_exists():
                self.steps_frame = tk.Frame(self.master)
                self.steps_frame.grid(row=10, column=0, columnspan=2)

             # If steps_frame exists, destroy it first
            for widget in self.steps_frame.winfo_children():
                widget.destroy()  # Remove existing widgets, if any

            intro1 = f"\n\nSuppose u'(t) = {du}, u({t0}) = {u0}, and h = {h}."
            intro2 = "We will now preform Euler's Method to approximate u(t)."
            intro3 = "Therefore:"

            tk.Label(self.steps_frame, text= intro1).grid(row=0, column=0, sticky="w")
            tk.Label(self.steps_frame, text= intro2).grid(row=1, column=0, sticky="w")
            tk.Label(self.steps_frame, text="").grid(row=2, column=0, sticky="w") 
            tk.Label(self.steps_frame, text= intro3).grid(row=3, column=0, sticky="w")
            # Display the steps below the input fields
            for idx, step in enumerate(steps):
                tk.Label(self.steps_frame, text=f"Step {idx}:\t t{idx} = {step[0] : 5f},\t u{idx} = {step[1]: 5f}").grid(row=idx+4, column=0, sticky="w")
            tk.Label(self.steps_frame, text="" ).grid(row=len(steps) + 4, column=0, sticky="w")
            tk.Label(self.steps_frame, text=f"Hence, u({steps[-1][0]}) ≈ {steps[-1][1]}" ).grid(row=len(steps) + 5, column=0, sticky="w")
            tk.Label(self.steps_frame, text="" ).grid(row=len(steps) + 6, column=0, sticky="w")
            self.export_buttons = tk.Button(self.steps_frame, text="Export Steps", command=lambda: self.export_steps(str(method.__name__), steps))
            self.export_buttons.grid(row=len(steps) + 7, column=0)
 
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")


    def compare_methods(self):
        """Runs both Euler methods and plots them on the same graph for comparison.""" 
        # Clear any existing plot in the plot_frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # If steps_frame has been destroyed, recreate it
        if not self.steps_frame.winfo_exists():
            self.steps_frame = tk.Frame(self.master)
            self.steps_frame.grid(row=10, column=0, columnspan=2)

        try:
            du = self.du_entry.get()
            t0 = float(self.t0_entry.get())
            u0 = float(self.u0_entry.get())
            h = float(self.h_entry.get())
            n = int(self.n_entry.get())

            f = let_f(du)
            t_std, u_std = standard_eulers_method(du, f, t0, u0, h, n, plot=False)
            t_imp, u_imp = improved_eulers_method(du, f, t0, u0, h, n, plot=False)

            self.plot_comparison(t_std, u_std, t_imp, u_imp)  # Plot comparison in Tkinter

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def plot_results(self, t_vals, u_vals, method):
        """Displays the results on the Tkinter window."""
        # Clear any existing plot in the plot_frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Clear any existing steps
        for widget in self.steps_frame.winfo_children():
            widget.grid_forget()

        # Only destroy the steps_frame if it exists and is not already destroyed
        if self.steps_frame.winfo_exists():
            self.steps_frame.destroy()  # Remove the steps_frame completely

        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if method == standard_eulers_method:
            ax.plot(t_vals, u_vals, marker='o', linestyle='-', label="Standard Euler")
        elif method == improved_eulers_method:
            ax.plot(t_vals, u_vals, marker='x', linestyle='--', label="Modified Euler", color='orange')

        ax.set_xlabel("t")
        ax.set_ylabel("u(t)")
        ax.set_title(f"{method.__name__.replace('_', ' ').title()} Approximation")
        ax.legend()
        ax.grid()

        # Embed the plot into Tkinter using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()

        # Place the canvas on the Tkinter window
        canvas.get_tk_widget().grid()

        # Add export button dynamically (clear any existing buttons first)
        for widget in self.plot_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()  # This will remove any existing export buttons

        # Add export button dynamically
        export_button = tk.Button(self.plot_frame, text="Export Graph", command=lambda: self.export_graph(str(method.__name__)))
        export_button.grid(row=9, column=0)

        # Store figure for exporting
        self.current_figure = fig
        self.current_method = method

        # Close the figure after embedding
        plt.close(fig)

    def plot_comparison(self, t_std, u_std, t_imp, u_imp):
        """Displays the comparison of both Euler methods on the Tkinter window."""
        # Clear any existing plot in the plot_frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Clear any existing steps
        for widget in self.steps_frame.winfo_children():
            widget.grid_forget()

        # Only destroy the steps_frame if it exists and is not already destroyed
        if self.steps_frame.winfo_exists():
            self.steps_frame.destroy()  # Remove the steps_frame completely

        # Create the comparison plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(t_std, u_std, marker='o', linestyle='-', label="Standard Euler")
        ax.plot(t_imp, u_imp, marker='x', linestyle='--', label="Improved Euler")
        ax.set_xlabel("t")
        ax.set_ylabel("u(t)")
        ax.set_title("Euler's Method Comparison")
        ax.legend()
        ax.grid()

        # Embed the comparison plot into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()

        # Place the canvas on the Tkinter window
        canvas.get_tk_widget().grid()

        # Add export button dynamically (clear any existing buttons first)
        for widget in self.plot_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()  # This will remove any existing export buttons
        
        # Add an "Export Graph" button dynamically
        export_button = tk.Button(self.plot_frame, text="Export Graph", command=lambda: self.export_graph("comparison"))
        export_button.grid()

        # Close the figure after embedding
        plt.close(fig)

    def export_graph(self, method):
        """Exports the current graph as a JPG file."""
        if self.current_figure is None:
            messagebox.showerror("Error", "No graph to export.")
            return

        try:
            # Determine the filename based on method string
            filename = f"{method}_graph.jpg"

            self.current_figure.savefig(filename, format='jpg')
            messagebox.showinfo("Export Successful", f"Graph saved as {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {e}")
    
    def export_steps(self, method, steps):
        """Exports the steps as a text file."""
        filename = f"{method}_steps.txt"
        with open(filename, 'w') as f:
            for idx, step in enumerate(steps):
                f.write(f"\tStep {idx}: \tt{idx} = {step[0]}, \tu{idx} = {step[1]}\n")
        
        messagebox.showinfo("Export Successful", f"Steps saved as {filename}")

