
from sympy import symbols, Eq, solve
import numpy as np
import math

def angle_between(center, p1, p2):
    v1 = np.array(p1) - np.array(center)
    v2 = np.array(p2) - np.array(center)
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return angle

def solve_for_intersection(k, plus=True): 
    x, y = symbols('x y')
    cx, cy = -1.0/k, -1.0/k

    plus_value = 0.5

    if not plus:
        plus_value = -0.5

    r = (k+plus_value)/k

    circle_eq = Eq((x-cx)**2 + (y-cy)**2, r**2)

    if r*r < 1.0/(k*k):
        return 0

    q = -1.0/(k) + math.sqrt(r*r - 1.0/(k*k))

    if q < 0:
        return 0
    points = [(q, 0), (0, q)]


    theta = angle_between((cx, cy), points[0], points[1])

    area = 0.5*(points[0][0]*points[1][1]) + (r*r)*0.5*(theta - math.sin(theta))

    #print(area)
    return area


sum = 0
for i in range(1, 100001):
    if i%10000 == 0:
        print("solved ", i)
    sum += i*(solve_for_intersection(i, True) - solve_for_intersection(i, False))


print(sum)