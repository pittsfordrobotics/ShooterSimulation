# 67
import numpy as np

dt = 0.01 # s
G = 9.81 # m / s^2
rho_air = 1.2250 # kg / m^3
drag_sphere = .47 # dimensionless
r = 0.15 # meters
a = np.pi*(r**2)

def find_drag(v: np.ndarray, drag_coefficient, A):
    return .5 * rho_air * np.linalg.norm(v) * drag_coefficient * A * v

def calculate_next(x: np.ndarray, v: np.ndarray):
    return x + dt * v, v - dt * (G+find_drag(v, drag_sphere, a))

def find_landing(height, v: np.ndarray):
    x = np.array([0]*3)
    while x[1] < height:
        
        print("Hello World!")
    return None # no landing. ball is too fast for this world