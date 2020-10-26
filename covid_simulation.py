# imports
from agent.covidagent import Agent
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
from PyCX import pycxsimulator
from random import choice as ranchoice

n = 1000 # number of agents
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
    axis([0, 1, 0, 1])

def update():
    ag = ranchoice(list(Agent.agentdict.keys()))
    neighbors = [nb for nb in Agent.agentdict if (Agent.agentdict[ag]["x"]-Agent.agentdict[nb]["x"])**2 + (Agent.agentdict[ag]["y"] - Agent.agentdict[nb]["y"])**2 < r**2 and nb != ag]
    if len(neighbors) > 0:
        q = len([nb for nb in neighbors if Agent.agentdict[nb]["infected"] == Agent.agentdict[ag]["infected"]]) \
        / float(len(neighbors))
        if q < th:
            Agent.agentdict[ag]["x"], Agent.agentdict[ag]["y"] = random(), random()

pycxsimulator.GUI().start(func=[initialize, observe, update])
