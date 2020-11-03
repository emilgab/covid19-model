# imports
from agent.covidagent import Agent
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
from PyCX import pycxsimulator
from random import choice as ranchoice
from operator import add, sub

n = 100 # number of agents
r = 0.1 # neighbourhood radius
th = 0.5 # threshold for moving

def initialize():
    pass

def observe():
    cla()
    infected = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == True]
    healthy = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == False]
    plot([Agent.agentdict[ag]["x"] for ag in infected], [Agent.agentdict[ag]["y"] for ag in infected], 'ro')
    plot([Agent.agentdict[ag]["x"] for ag in healthy], [Agent.agentdict[ag]["y"] for ag in healthy], 'bo')
    axis('image')
    axis([0, 1, 0, 1])

def update():
    # ag = ranchoice(list(Agent.agentdict.keys()))
    for ag in list(Agent.agentdict.keys()):
        # neighbors = [nb for nb in Agent.agentdict if (Agent.agentdict[ag]["x"]-Agent.agentdict[nb]["x"])**2 + (Agent.agentdict[ag]["y"] - Agent.agentdict[nb]["y"])**2 < r**2 and nb != ag]
        # if len(neighbors) > 0:
        #     q = len([nb for nb in neighbors if Agent.agentdict[nb]["infected"] == Agent.agentdict[ag]["infected"]]) \
        #     / float(len(neighbors))
        #     if q < th:
        #         Agent.agentdict[ag]["x"], Agent.agentdict[ag]["y"] = random(), random()
        try:
            if Agent.agentdict[ag]["direction_positive"] == True:
                if Agent.agentdict[ag]["x"] < 0:
                    del Agent.agentdict[ag]
                Agent.agentdict[ag]["x"] -= 0.01
                rnd_op = ranchoice([add, sub, None])
                if rnd_op != None:
                    Agent.agentdict[ag]["y"] = rnd_op(Agent.agentdict[ag]["y"], 0.01)
            if Agent.agentdict[ag]["direction_negative"] == True:
                if Agent.agentdict[ag]["x"] > 1:
                    del Agent.agentdict[ag]
                Agent.agentdict[ag]["x"] += 0.01
                rnd_op = ranchoice([add, sub, None])
                if rnd_op is not None:
                    Agent.agentdict[ag]["y"] = rnd_op(Agent.agentdict[ag]["y"], 0.01)

        except:
            pass
    ag = Agent()

pycxsimulator.GUI().start(func=[initialize, observe, update])
print(Agent.overview())
