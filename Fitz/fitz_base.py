#This function contains an implementation of the 
#Hodgkin-Huxley model
#and the FitzHugh-Nagumo model
import time
import pylab
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import moviepy.editor as mp 

class fitzhughNagumo():
    #time step
    tstep = None
    t_end = 20
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
    def Main(self):
        t_now = self.t_now
        t_end = self.t_end
        t_sc = self.t_sc
        vs = self.vs
        ts = self.ts 
        tstep = self.tstep 
        v = self.v
        w = self.w
        eps = self.eps
        a,b,c = self.a,self.b,self.c
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
        return ts, vs

if __name__ == '__main__':
    runner = fitzhughNagumo()
    runner.tstep = .01
    main = runner.Main()
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    plt.title('Fitzhugh-Nagumo - Even increments')
    line, = ax.plot(main[0], main[1], 'k')
    plt.ylabel('Membrane Potential (V)')
    plt.xlabel('Time (s)')
    def update(i):
        label = 'Time (s), timestep {0}'.format(i)
        print(label)
        line.set_xdata([x*i for x in main[0]])
        print(len(main[0]*i))
        # Update the line and the axes (with a new xlabel). Return a tuple of
        # "artists" that have to be redrawn for this frame.
        ax.set_xlabel(label)
        plt.show()
        return main[0], ax
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=5, metadata=dict(artist='Fernando Espinosa'))
    anim = FuncAnimation(fig, update, frames=np.arange(1, 10), interval=100)
    anim.save('Fitz_even_linear.mp4', writer=writer)
    clip = mp.VideoFileClip('Fitz_even_linear.mp4')
    clip.write_gif('Fitz_base.gif')