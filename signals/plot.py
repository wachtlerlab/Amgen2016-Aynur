from astropy.visualization import quantity_support
quantity_support()
from matplotlib import pylab as plt
import neo

def plot_single_analog_signal(signal):
    x = signal.times
    y = signal.magnitude
    plt.plot(x, y, label=signal.name)
    plt.xlabel(signal.times.units)
    plt.ylabel(signal.units)
    plt.legend()
    plt.show()

def show():
    plt.legend()
    plt.show()