#This function contains an implementation of the 
#Hodgkin-Huxley model
#and the FitzHugh-Nagumo model
import time;
import pylab;
import numpy as np

#External current function (for pacing)
#It could be used for sensor input later on
def readExternal():
    return 0; 

def fitzhughNagumo(t_end):
    #time step
    tstep = 0.01;
    #initial values of v and w
    v = 2.0; 
    w = 0.0; 
    I_ext = 0; 
    tc = 1.0;
    #parameters
    a = 1; b = 0.0; c = 0.8;
    eps = 10;
    #time scale used to shift the model
    t_sc = 10; 
    #end of parameters
    inc = 0; 
    vs = []; 
    ts = [];
    t_now = 0; 
    ts.append(t_now); 
    vs.append(v); 
    while(t_now < t_end):
        #calculate the rate of change
        I_ext = readExternal();
        dv = t_sc*(v - v**3/3 - w + I_ext)
        dw = t_sc*(1.0/eps*(a*v+b-c*w));
        #calculate the value of v based on the rate of change
        v = v+tstep*dv; 
        w = w+tstep*dw;     
        t_now = t_now+tstep;
        
        ts.append(t_now); 
        vs.append(v);
        
    pylab.plot(ts, vs);
    pylab.xlabel('time in seconds');
    pylab.ylabel('Voltage in Volts'); 
