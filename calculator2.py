from sympy import sympify, Eq, solve, diff, integrate, symbols, limit, Sum
from scipy.integrate import quad, odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

x = symbols("x")

def choice():
    choice = input("\nWhat do you want to do?\n1. Algebra\n2. Derivative\n3. Integral\n4. Graph\n5. Limit\n6. Sum\n7. ODE\nResponse: ")
    
    if choice == "1" or choice.lower() == "algebra":
        def algebra():
            left = sympify(input("Left side of equation (eg x**2, 2*x): "))
            right = sympify(input("Right side of equation (eg 2, x**0.5): "))
            equation = Eq(left, right)
            solution = solve(equation)
            print(f"The solutions/s to the equation is/are {solution}")
        algebra()

    elif choice == "2" or choice.lower() == "derivative":
        def derivative():
            function = sympify(input("Function to take the derivative of: "))
            deriv = diff(function, x)
            print(f"The derivative of {function} is {deriv}")
        derivative()

    elif choice == "3" or choice.lower() == "integral":
        def integral():
            choice = input("Do you want to take the indefinite integral or definite integral? (1 or 2): ")
            if choice == "1":
                function = sympify(input("Function to take the integral of: "))
                indef_integral = integrate(function, x)
                print(f"The integral of {function} is", indef_integral, "+ c")
            elif choice == "2":
                function = sympify(input("Function to take the integral of: "))
                a = float(input("Lower bound: "))
                b = float(input("Upper bound: "))
                new_function = lambda val: float(function.subs(x, val))
                def_integral = quad(new_function, a, b) #quad() only accepts lambda functions
                print(f"The definite integral of {function} from [{a},{b}] is {def_integral}")
        integral()

    elif choice == "4" or choice.lower() == "graph":
        def graph():
            x = np.linspace(-20, 20, 1000)
            y = x
            plt.plot(x, y)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Wave Function')
            plt.grid(True)
            plt.show()
        graph()

    elif choice == "5" or choice.lower() == "limit":
        def the_limit():
            limit_function = sympify(input("Function to take limit of: "))
            a = sympify(input("Value that f approaches: "))
            lim = limit(limit_function, x, a)
            print(f"The limit of {limit_function} as it approaches {a} is {lim}")
        the_limit()
    
    elif choice == "6" or choice.lower() == "sum":
        def summation():
            a_x = sympify(input("Function a_x: "))
            start = sympify(input("Number to start at (typically 0 or 1): "))
            end = sympify(input("Number to stop at (can be oo as well!): "))
            the_sum = Sum(a_x, (x, start, end)).doit() #.n() approximates while .doit() gives exact answer
            print(f"{a_x}, starting at {start}, ending at {end}, gives {the_sum}")
        summation()
    
    elif choice == "7" or choice.lower() == "ode":
        def ordinary():
            
            def lorenz(t, state, sigma, beta, rho):
                x, y, z = state
                dx = sigma * (y - x) #Differential equations
                dy = x * (rho - z) - y
                dz = x * y - beta * z
                return [dx, dy, dz]
            
            x = sympify(input("x: "))
            y = sympify(input("y: "))
            z = sympify(input("z: "))
            y0 = [x, y, z] #Initial conditions

            #Ed Lorenz used these values for the parameters.
            sigma = 10
            beta = 8 / 3
            rho = 28
            p = (sigma, beta, rho) #parameters

            t = np.arange(0.0, 30.0, 0.01)

            ode_sol = odeint(lorenz, y0, t, p, tfirst = True) #odeint() returns values for x, y, and z over t. 
            #[ [x, y, z] [ode_sol[:1, 0] ode_sol[:1, 1] ode_sol[:1, 2]] ... [ode_sol[1:2, 0] ode_sol[1:2, 1] ode_sol[1:2, 2]] ]

            fig = plt.figure()
            ax = fig.add_subplot(1, 2, 1, projection = "3d") #1x2 grid at position 1. 3D projection
            ax.plot(ode_sol[:, 0], #Each of the x-values
                    ode_sol[:, 1], #Each of the y-values
                    ode_sol[:, 2], color = 'white') #Each of the z-values
            ax.set_title(f"dx/dt = σ(y - x)\ndy/dt = x(ρ - z) - y\ndz/dt = xy - βz\nx =  {x}\ny =  {y}\nz =  {z}")

            line_color = input("Color of line: ")
            line, = ax.plot([], [], [], lw = 0.7, color = f'{line_color}')

            def initial(): #Starts with no line
                line.set_data([], [])
                line.set_3d_properties([])
                return line,

            def update(frame): #Updates the line for each of the 30 frames
                line.set_data(ode_sol[:frame, 0], ode_sol[:frame, 1])
                line.set_3d_properties(ode_sol[:frame, 2])
                return line,

            animation = FuncAnimation(fig, update, frames = len(t), init_func = initial, interval = 1, blit = True) 
            plt.show()

        ordinary()

def restart():
    restart = input("Want to do another operation? (y or n): ")
    if restart.lower() == "y" or restart.lower() == "yes":
        return True
    else:
        return False

choice()

while restart():
    choice()
