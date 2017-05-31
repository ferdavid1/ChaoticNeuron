import time
import pylab
import numpy as np

mu, sigma = 0, 1
gaussian_random_dev = np.random.normal(mu, sigma, 9)

pos_gaussian = abs(gaussian_random_dev) # positive values only
pos_gaussian = np.sort(pos_gaussian)
print(pos_gaussian)


def fitzhughNagumo(tstep, t_end):
    #time step
    tstep = tstep
    #initial values of v and w
    v = 2.0 
    w = 0.0 
    I_ext = 0 
    tc = 1.0
    #parameters
    a = 1 
    b = 0.0 
    c = 0.8
    eps = 10
    #time scale used to shift the model
    t_sc = 10 
    #end of parameters
    inc = 0 
    vs = [] 
    ts = []
    t_now = 0 
    ts.append(t_now) 
    vs.append(v) 
    while(t_now < t_end):
        #calculate the rate of change
        dv = t_sc*(v - v**3/3 - w)
        dw = t_sc*(1.0/eps*(a*v+b-c*w))
        #calculate the value of v based on the rate of change
        v = v+tstep*dv 
        w = w+tstep*dw     
        t_now = t_now+tstep
        
        ts.append(t_now) 
        vs.append(v)
        
    pylab.plot(ts*100, vs)
    pylab.xlabel('time in milliseconds')
    pylab.ylabel('Voltage in Volts') 
    pylab.show()
for x in range(10):
	fitzhughNagumo(0.1*x, 20)