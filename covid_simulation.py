import matplotlib
matplotlib.use('TkAgg')
from pylab import *

def initialize():
    global x
    pass

def observe():
    global x
    pass

def update():
    global x

from PyCX import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
