import numpy as np
import re
from typing import Callable

def let_f(du : str) -> Callable[[float, float], float] :
    du = du.replace("sqrt", "np.sqrt")
    du = du.replace("^", "**")
    du = re.sub(r"(\d)([A-Za-z])", r"\1*\2", du)
    
    def f(t, u):
        context = {"t" : t, "u" : u, "np" : np }
        return eval(du, context)

    return f

# calculates the improved euler's method
def improved_eulers_method_eqn(f : Callable[[float, float], float], t0 : float , u0 : float , h : float) -> float:

    t1 = t_next(t0, h);                             # step 1
    w = standard_eulers_method_eqn(f, t0, u0, h)        # step 2
    u1 = u0 + ((h * (f(t0, u0) + f(t1, w))))/ 2     # step 3
    return u1

def t_next(t0 : float , h : float) -> float:
    t1 = t0 + h 
    return t1 

def standard_eulers_method_eqn(f :  Callable[[float, float], float] , t0 : float , u0 : float, h : float) -> float:
    u1 = u0 + (h * (f(t0, u0))) 
    return u1

def improved_eulers_method(du : str, f : Callable[[float, float], float], t0 : float , u0 : float , h : float, n: int) -> None:
    print(f"\n\nSuppose u'(t) = {du}, u({t0}) = {u0}, and h = {h}.")
    points = [(t0, u0)]
    print("We will now preform the Modified Euler's Method to approximate u(t):")
    print("Therefore: ")
    for i in range(n):
        u0 = improved_eulers_method_eqn(f, t0, u0, h)
        t0 = t_next(t0, h)
        points.append((t0, u0))
        print(f"Step {i + 1} : u({t0}) = {u0}") 
    print(f"\n\nThus, u({t0}) ≈ {u0}\n\n")

def standard_eulers_method(du : str, f : Callable[[float, float], float], t0 : float , u0 : float , h : float, n: int) -> None:
    print(f"\n\nSuppose u'(t) = {du}, u({t0}) = {u0}, and h = {h}.")
    points = [(t0, u0)]
    print("We will now preform the Standard Euler's Method to approximate u(t):")
    print("Therefore: ")
    for i in range(n):
        u0 = standard_eulers_method_eqn(f, t0, u0, h)
        t0 = t_next(t0, h)
        points.append((t0, u0))
        print(f"Step {i + 1} : u({t0}) = {u0}")
    print(f"\n\nThus, u({t0}) ≈ {u0}\n\n")

def change_question(du : str, f : Callable[[float, float], float], t0 : float , u0 : float , h : float, n: int) :
    selection = 0
    while True:
        match selection:
            case 0:
                print("Select an option to update: ")
                print("\t1. Differential Equation u'(t)")
                print("\t2. Initial Condition u(t0) = u0")
                print("\t3. Step Size h") 
                print("\t4. Number of Steps n")
                print("\t5. all of the above")
                print("\t6. Exit")
                selection = int(input("Selection: "))
                print("\n\n")
            case 1:

                du = input("Enter your differential equation in terms of u and t: ") # should add a verificaton
                f = let_f(du)

                selection = 0
            case 2:
                # given initial condition u(t0) = u0
                u0 = float(input("Enter initial value u: "))
                t0 = float(input("Enter initial time t: "))

                selection = 0
            case 3:
                # given step value h
                h = float(input("Enter the step value h: "))

                selection = 0
            case 4:
                # number of steps n
                n = int(input("Enter in the number of steps: "))

                selection = 0
            case 5:
                # given differential equation u'(t)
                du = input("Enter your differential equation in terms of u and t: ") # should add a verificaton
                f = let_f(du)

                # given initial condition u(t0) = u0
                u0 = float(input("Enter initial value u: "))
                t0 = float(input("Enter initial time t: "))

                # given step value h
                h = float(input("Enter the step value h: "))
                
                # number of steps n
                n = int(input("Enter in the number of steps: "))
                selection = 0
            case 6:
                return  (du, f, t0, u0, h, n)
            case _:
                selection = 0

if __name__ == "__main__":
   
    # given differential equation u'(t)
    du = input("Enter your differential equation in terms of u and t: ") # should add a verificaton
    f = let_f(du)
    
    # given initial condition u(t0) = u0
    u0 = float(input("Enter initial value u: "))
    t0 = float(input("Enter initial time t: "))

    # given step value h
    h = float(input("Enter the step value h: "))
    
    # number of steps n
    n = int(input("Enter in the number of steps: "))
    
    
    selection = 0
    while True:
        match selection:
            case 0:
                print("Select an option: ")
                print("\t1. Standard Euler's Method")
                print("\t2. Modified Euler's Method")
                print("\t3. Standard vs Modified") 
                print("\t4. Update Question")
                print("\t5. Exit")
                selection = int(input("Selection: "))
            case 1:
                standard_eulers_method(du, f, t0, u0, h, n)
                selection = 0
            case 2:
                improved_eulers_method(du, f, t0, u0, h, n)
                selection = 0
            case 3:
                print("Feature coming soon.")
                selection = 0
            case 4:
                (du, f, t0, u0, h, n) = change_question(du, f, t0, u0, h, n)
                selection = 0
            case 5:
                break
            case _:
                selection = 0
