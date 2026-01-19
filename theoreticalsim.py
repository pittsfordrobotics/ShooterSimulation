import math
import numpy as np

H = 1.84
MAXTHETA = 70
G = 9.81

def getX(theta, v):
    s = math.sin(theta)
    c = math.cos(theta)
    if ((c**2 * v**2) - (2*G*H)) <= 0:
        return -1
    return ((s*v)*(math.sqrt((c**2 * v**2) - (2*G*H)) + c*v))/G

def calculateV(theta, r):
    a = r / math.cos(theta)
    b = G / (a*math.sin(theta) - H)
    return a * math.sqrt(b/2)

# input r, get theta and v
# bruteforce different thetas, get a small change for v
def getIdeal(r):
    mintheta = int(math.degrees(math.atan(r/H))) + 1
    min_squaresum = 9999999999
    ideal_v = 0
    ideal_theta = 0
    for i in range(mintheta, MAXTHETA+1):
        theta = math.radians(i)
        v = calculateV(theta, r)
        x2 = getX(theta+0.01, v)
        dxdtheta = (r-x2)/(0.01)
        x2 = getX(theta, v+0.1)
        dxdv = (r-x2)/(0.1)

        sq_sum = dxdtheta**2 + dxdv**2
        if (sq_sum<min_squaresum):
            min_squaresum = sq_sum
            ideal_v = v
            ideal_theta = theta
    
    return [ideal_v, math.degrees(ideal_theta)]

# - 5 variables: theta, phi, v0, r
# - goal: needs landing position SD 1/5 width of hub (~4 sigma)
# - simulate for testing:
#     - f(r) -> calculate expected theta, phi, v0
#     - use SD of theta, phi, v0, (r) + add randomness using normal dist (_r)
#     - g(theta_r, phi_r, v0_r, r_r) -> x in hub
#     - use this to find SD of x
# - Getting data v0:
#     - shoot horizontally on table with set h
#     - measure distance to calculate
# - getting data theta (with hood):
#     - set hood to set angle
#     - use high speed slomo camera
#     - get theta from straight line from closest moment leave hood and 0.1s later from that frame
#     - repeat with other set angles?
# - around 20 trials for each
def getSimulatedSDx(r, sd_t, sd_v, n = 30):
    id = getIdeal(r)
    v_expected = id[0]
    theta_expected = id[1]

    res_x = []
    for i in range(n):
        theta_experimental = np.random.normal(theta_expected, sd_t)
        v_experimental = np.random.normal(v_expected, sd_v)
        res_x.append(r - getX(theta_experimental, v_experimental))

    return float(np.std(res_x))

if __name__ == "__main__":
    r = float(input("enter distance from target (m): "))
    # h = input("enter target height")
    # if h == "":
    #     h = 1.84 # meters
    # else: 
    #     h = int(h)
    print("ideal v, theta: ")
    print(getIdeal(r))
    sd_t = float(input("enter standard deviation of theta: "))
    sd_v = float(input("enter standard deviation of v: "))
    sim = getSimulatedSDx(r, sd_t, sd_v)
    print("simulated sd of landing location: " + str(sim))
    print("                           = " + str((sim/1.059942)*100) + "% of hub, goal ~20%")