from gui.gui import EulerMethods
import tkinter as tk

def main():
    root = tk.Tk()
    app = EulerMethods(root)
    root.mainloop()

if __name__ == "__main__":
    main()
