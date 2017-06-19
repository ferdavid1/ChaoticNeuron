import scipy as sp
import pylab as plt
from scipy.integrate import odeint
import seaborn
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import moviepy.editor as mp 
import pynamical
from pynamical import simulate, bifurcation_plot, save_fig
import pandas as pd, numpy as np, IPython.display as display, matplotlib.pyplot as plt, matplotlib.cm as cm


class HodgkinHuxley():
    """Full Hodgkin-Huxley Model implemented in Python"""

    C_m  =   1.0
    """membrane capacitance, in uF/cm^2"""

    g_Na = 120.0
    """Sodium (Na) maximum conductances, in mS/cm^2"""

    g_K  =  36.0
    """Postassium (K) maximum conductances, in mS/cm^2"""

    g_L  =   0.3
    """Leak maximum conductances, in mS/cm^2"""

    E_Na =  20.0
    """Sodium (Na) Nernst reversal potentials, in mV"""

    E_K  = -10.0
    """Postassium (K) Nernst reversal potentials, in mV"""

    E_L  = -77.387
    """Leak Nernst reversal potentials, in mV"""

    t = None
    """ The time to integrate over """

    def alpha_m(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.1*(V+40.0)/(1.0 - sp.exp(-(V+40.0) / 10.0))

    def beta_m(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 4.0*sp.exp(-(V+65.0) / 18.0)

    def alpha_h(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.07*sp.exp(-(V+65.0) / 20.0)

    def beta_h(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 1.0/(1.0 + sp.exp(-(V+35.0) / 10.0))

    def alpha_n(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.01*(V+55.0)/(1.0 - sp.exp(-(V+55.0) / 10.0))

    def beta_n(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.125*sp.exp(-(V+65) / 80.0)

    def I_Na(self, V, m, h):
        """
        Membrane current (in uA/cm^2)
        Sodium (Na = element name)

        |  :param V:
        |  :param m:
        |  :param h:
        |  :return:
        """
        return self.g_Na * m**3 * h * (V - self.E_Na)

    def I_K(self, V, n):
        """
        Membrane current (in uA/cm^2)
        Potassium (K = element name)

        |  :param V:
        |  :param h:
        |  :return:
        """
        return self.g_K  * n**4 * (V - self.E_K)
    #  Leak
    def I_L(self, V):
        """
        Membrane current (in uA/cm^2)
        Leak

        |  :param V:
        |  :param h:
        |  :return:
        """
        return self.g_L * (V - self.E_L)

    def I_inj(self, t):
        """
        External Current

        |  :param t: time
        |  :return: step up to 10 uA/cm^2 at t>100
        |           step down to 0 uA/cm^2 at t>200
        |           step up to 35 uA/cm^2 at t>300
        |           step down to 0 uA/cm^2 at t>400
        """
        return 10*(t>100) - 10*(t>200) + 35*(t>300) - 35*(t>400)

    @staticmethod
    def dALLdt(X, t, self):
        """
        Integrate

        |  :param X:
        |  :param t:
        |  :return: calculate membrane potential & activation variables
        """
        V, m, h, n = X

        dVdt = (self.I_inj(t) - self.I_Na(V, m, h) - self.I_K(V, n) - self.I_L(V)) / self.C_m
        dmdt = self.alpha_m(V)*(1.0-m) - self.beta_m(V)*m
        dhdt = self.alpha_h(V)*(1.0-h) - self.beta_h(V)*h
        dndt = self.alpha_n(V)*(1.0-n) - self.beta_n(V)*n
        return dVdt, dmdt, dhdt, dndt

    def Main(self):
        """
        Main demo for the Hodgkin Huxley neuron model
        """
        X = odeint(self.dALLdt, [-50, 0.05, 0.6, 0.32], self.t, args=(self,))
        V = X[:,0]
        m = X[:,1]
        h = X[:,2]
        n = X[:,3]
        ina = self.I_Na(V, m, h)
        ik = self.I_K(V, n)
        il = self.I_L(V)
        return V

if __name__ == '__main__':
    # run the logistic model for 20 generations for 7 growth rates between 0.5 and 3.5 then view the output
    pops = simulate(num_gens=1000, rate_min=0.5, rate_max=3.5, num_rates=7)
    pops = np.array(pops)
    pops.flatten()
    pops = np.sort(pops)
        
    # g1 = []; g2 = []; g3 = []; g4 = []; g5 = []; g6 = [];
    # gen_count = 0
    # for gen in pops:
    #     gen_count += 1
    #     if gen_count == 1:
    #         for y in gen:
    #             g1.append(y)
    #     if gen_count == 2:
    #         for y in gen:
    #             g2.append(y)
    #     if gen_count == 3:
    #         for y in gen:
    #             g3.append(y)
    #     if gen_count == 4:
    #         for y in gen:
    #             g4.append(y)
    #     if gen_count == 5:
    #         for y in gen:
    #             g5.append(y)
    #     if gen_count == 6:
    #         for y in gen:
    #             g6.append(y)
    # generations = [g2, g3, g4, g5, g6] # we're gonna ignore the first generation as they all have the same values
    count = 0
    for x in range(1, len(pops)):
        count +=1
        runner = HodgkinHuxley()
        runner.t = [val for val in pops[x]]
        main = runner.Main()
        fig, ax = plt.subplots()
        fig.set_tight_layout(True)

        plt.title('Hodgkin-Huxley - Chaotic (gen ' + str(count) + ')')
        line, = ax.plot(runner.t, main, 'k')
        plt.ylabel('Membrane Potential (mV)')
        plt.xlabel('Time (ms)')

        def update(i):
            label = 'Time (ms), timestep {0}'.format(i)
            print(label)

            line.set_xdata(np.multiply(runner.t, i))
            # Update the line and the axes (with a new xlabel). Return a tuple of
            # "artists" that have to be redrawn for this frame.
            ax.set_xlabel(label)
            return runner.t, ax
        print(runner.t)
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=5, metadata=dict(artist='Fernando Espinosa'))
        anim = FuncAnimation(fig, update, frames=sp.arange(1, len(generations[x])), interval=100)
        anim.save('HH_chaotic' + str(count) + '.mp4', writer=writer)
        clip = mp.VideoFileClip('HH_chaotic' + str(count) + '.mp4')
        try:
            clip.write_gif('HH_chaotic' + str(count) + '.mp4')
        except TypeError:
            pass
