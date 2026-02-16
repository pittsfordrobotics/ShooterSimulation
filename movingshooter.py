import math
import numpy as np
import matplotlib.pyplot as plt

# all units: 
# meters
# radians
# seconds
# 
# y is up
# spherical coords: theta is v to y axis, phi is projected to x axis

G = 9.81

def getVelocityY(r, y, vr):
    if 2*y*vr*vr>r*r*G: 
        raise Exception(f"nyoom r: {r}, y: {y}, vr: {vr}")
    t = r / vr
    return (y/t)+(G*t/2)

# has to be in cartesian
def getLandingPosition(y, v):
    t = (v[1]+math.sqrt(v[1]*v[1]-2*G*y))/G
    return (t*v[0], t*v[2])

def sphereToCart(r, theta, phi):
    return (r*math.sin(theta)*math.cos(phi), r*math.cos(theta), r*math.sin(theta)*math.sin(phi))

def cartToSphere(p):
    (x,y,z) = p
    r = math.sqrt(x*x+y*y+z*z)
    return [r, math.acos(y/r), math.atan2(z, x)]

def add(a, b):
    if type(a) == tuple:
        return tuple(a[i] + b[i] for i in range(len(a)))
    else:
        return [a[i] + b[i] for i in range(len(a))]

def mult(c, a):
    if type(a) == tuple:
        return tuple([c*k for k in a])
    else:
        return [c*k for k in a]

def sub(a, b):
    return add(a, mult(-1, b))


if __name__ == "__main__":
    print(getLandingPosition(1.84, (3, 10.73, 4)))
    sta = input("search tightness angle")
    if sta == "":
        sta = 0.01
    else:
        sta = float(sta)
    sts = input("search tightness speed")
    if sts == "":
        sts = 0.01
    else:
        sts = float(sts)
    inX = input("input dx")
    inZ = input("input dz")
    inX = float(inX)
    inZ = float(inZ)
    inRsq = inX**2+inZ**2
    inR = math.sqrt(inRsq)
    inY = input("input height (default: 1.84 m)")
    if inY == "":
        inY = 1.84
    else:
        inY = float(inY)
    inVelX = input("input vx")
    if inVelX == "-":
        inVelX = 0
        inVelZ = 0
    else:
        if inVelX == "":
            inVelX = 0
        else:
            inVelX = float(inVelX)
        inVelZ = input("input vz")
        if inVelZ == "":
            inVelZ = 0
        else:
            inVelZ = float(inVelX)
    vel = (inVelX, 0, inVelZ)

    
    maxVR = math.sqrt(inRsq*G/(2*inY))
    print(maxVR)
    ds = []
    for i in range(1, 100):
        vR = maxVR*i/100
        ideal = (vR*inX/inR, getVelocityY(inR, inY, vR), vR*inZ/inR)
        print(ideal)

        ideal = sub(ideal, vel)
        idealSphere = cartToSphere(ideal)
        print(idealSphere)
        print(getLandingPosition(inY, add(ideal, vel)))
        delt = [0] * 3
        delt[1] = sta
        d = add(idealSphere, delt)

        e = sub(idealSphere, delt)
        cd = sphereToCart(*d)
        ce = sphereToCart(*e)
        try:
            ld = getLandingPosition(inY, add(cd, vel))
            le = getLandingPosition(inY, add(ce, vel))
        except:
            ds.append(0)
            continue
        print(ld, le)
        dist = sub(le, ld)
        print(dist)
        dist = dist[0]**2 + dist[1]**2
        print(dist)
        ds.append(dist/sta/2)

    print(ds)
    vrs = [maxVR*i/100 for i in range(1, 100)]
    plt.plot(vrs, ds)
    plt.show()