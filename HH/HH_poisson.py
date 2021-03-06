import scipy as sp
import pylab as plt
from scipy.integrate import odeint
import seaborn
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import moviepy.editor as mp 

Poisson_random_dev = sp.random.poisson(1,10)

pos_Poisson = abs(Poisson_random_dev) # positive values only
pos_Poisson = sp.sort(pos_Poisson)

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
    runner = HodgkinHuxley()
    runner.t = pos_Poisson
    main = runner.Main()
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    plt.title('Hodgkin-Huxley - Poisson')
    line, = ax.plot(runner.t, main, 'k')
    plt.ylabel('Membrane Potential (mV)')
    plt.xlabel('Time (s)')
    def update(i):
        label = 'Time (s), timestep {0}'.format(i)
        print(label)
        print(pos_Poisson[i])

        line.set_xdata(runner.t*i)
        # Update the line and the axes (with a new xlabel). Return a tuple of
        # "artists" that have to be redrawn for this frame.
        ax.set_xlabel(label)
        return runner.t, ax
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=5, metadata=dict(artist='Fernando Espinosa'))
    anim = FuncAnimation(fig, update, frames=sp.arange(1, len(pos_Poisson)), interval=100)
    anim.save('HH_Poisson.mp4', writer=writer)
    clip = mp.VideoFileClip('HH_Poisson.mp4')
    clip.write_gif('HH_Poisson.gif')
