# imports
from agent.covidagent import Agent
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
from PyCX import pycxsimulator

n = 100 # number of agents
r = 0.1 # neighbourhood radius
th = 0.5 # threshold for moving

def initialize():
    for i in range(n):
        ag = Agent()
        ag.x = random()
        ag.y = random()

def observe():
    cla()
    infected = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == True]
    healthy = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == False]
    plot([Agent.agentdict[ag]["x"] for ag in infected], [Agent.agentdict[ag]["y"] for ag in infected], 'ro')
    plot([Agent.agentdict[ag]["x"] for ag in healthy], [Agent.agentdict[ag]["y"] for ag in healthy], 'bo')
    axis('image')
    axis([0, 1, 0])

def update():
    pass

pycxsimulator.GUI().start(func=[initialize, observe, update])
