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
    

def HH_model(t_end):
    #parameters of the HH model
    ENa = 115; gNa = 120; 
    EK  = -12; gK  = 36; 
    EL  = 10.6; gL = 0.3; 
    C = 1;
    tstep = 0.01; 
    t_sc = 10;
    v=0; m=0; n=0; h=0; 
    vs = [];
    vs.append(v); 
    t_now = 0; 
    ts = []; 
    ts.append(t_now); 
    while(t_now < t_end):
        INa = gNa*m**3*h*(v-ENa);
        IK  = gK*n**4*(v-EK);
        IL  = gL*(v-EL);
        I_ext = readExternal(); 
        
        dv = -1.0/C*(INa+IK+IL+I_ext);
        dv = dv*t_sc;

        
        a_n = (0.1-0.01*v)/(np.exp(1-0.1*v)-1);
        b_n = (0.125)*np.exp(-v/80); 
        
        a_m = (2.5-0.1*v)/(np.exp(2.5-0.1*v)-1); 
        b_m = 4*np.exp(-v/18);
        
        a_h = (0.07*np.exp(-v/20));
        b_h = 1/(np.exp(3-0.1*v)+1); 
        
        dm = a_m*(1-m)-b_m*m;
        dm = dm*t_sc;
        
        dn = a_n*(1-n)-b_n*n; 
        dn = dn*t_sc;
        
        dh = a_h*(1-h)-b_h*h; 
        dh = dh*t_sc;
        
        v = v+tstep*dv; 
        m = m+tstep*dm; 
        n = n+tstep*dn; 
        h = h+tstep*dh; 
        
        t_now = t_now+tstep;
        ts.append(t_now);
        vs.append(v); 
        
    pylab.plot(ts,vs); 

#Run the HH model    
pylab.figure(1);        
fitzhughNagumo(10);
pylab.figure(2);
HH_model(10);