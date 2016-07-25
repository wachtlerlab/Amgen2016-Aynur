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

def plot_multiple_analog_signals(timeunit="ms", *signals):
    for s in signals:
        s.times.units=timeunit
        plt.plot(s.times, s.magnitude, label=s.name)
    plt.xlabel("time, "+timeunit)
    plt.ylabel("value, unit")
    plt.legend()

def show():
    plt.show()

def subplot(w, h, n):
    plt.subplot(w*100+h*10+n)