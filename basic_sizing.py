from math import *
import numpy as np
import matplotlib.pyplot as plt
from sympy import *


# (23-10)
# Very basic initial sizing for the centrifugal impeller
# Design parameters: output pressure, mass flow rate, outlet height, diameter
# Outputs: Output temperature T2, angular velocity, shaft power, axial thrust, head

# Key Assumptions:
# (1) Isentropic process + ideal gas throughout --> use of isentropic relations
# (2) Standard conditions (temp+pressure) at entry
# (3) * Radial speed = 0.5 x tangential tip speed * from vibes

T1 = 298
P1 = 1.013*10**5
R = 287 # of air
mdot = 0.1 # kg/s
Cp = 1010 # for air

class Impeller:
    def __init__(self,P2,mdot,D1,D2,h):
        self.P2 = P2
        self.mdot = mdot
        self.D1 = D1
        self.D2 = D2
        self.h = h

    def T2(self):
        return T1*(self.P2/P1)**(0.4/1.4)
    
    def rho(self):
        return self.P2/(R*self.T2())

    def head(self):
        # https://www.engineeringtoolbox.com/pump-head-pressure-d_663.html
        # 0.00121 is specific gravity of air
        return ((self.P2-P1)/10**5)/(0.0981*0.00121)
    
    def omega(self):
        return 4*self.mdot/(self.D2**2*self.rho()*self.h*3.1416) # rad/s
    
    def omegaRPM(self):
        return self.omega()*60/(2*3.1416)
    
    def C1(self):
        return self.mdot/(self.rho()*3.1416*(self.D1/2)**2)
    
    def C2(self):
        return 0.25*self.D2*self.omega()

    def power(self):
        # note: C2 here is a guestimate of the radial component (strictly it should be Cr2), not abs. velocity, 
        # but power from enthalpy should be the main component anyways
        return -self.mdot*(Cp*(self.T2()-T1)+0.5*self.C2()**2-0.5*self.C1()**2)

    def axialthrust(self):
        return self.mdot*self.C1()
    
    

D2s = np.arange(0.05,0.21,0.005)
n = len(D2s)

#assuming D1 = D2/3
D1s = [D2s[i]/3 for i in range(n)]


omegas = np.zeros(n)
powers = np.zeros(n)
thrusts = np.zeros(n)

for i in range(n):
    test = Impeller(P2=1.5*10**5,mdot=mdot,D1=D1s[i],D2=D2s[i],h=0.005)
    omegas[i] = test.omegaRPM()
    powers[i] = test.power()
    thrusts[i] = test.axialthrust()


plt.plot(D2s,omegas)
#plt.plot(D2s,powers)
#plt.plot(D2s,thrusts)

plt.xlabel("Impeller Diameter (m)")

plt.ylabel("angular velocity (RPM) required for 0.1 kg/s")
#plt.ylabel("Shaft power (W)")
#plt.ylabel("Axial Thrust (N)")

plt.grid()
plt.show()

test2 = Impeller(P2=1.5*10**5,mdot=mdot,D1=D1s[i],D2=D2s[i],h=0.005)

