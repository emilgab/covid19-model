# imports
from agent.covidagent import Agent
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
from PyCX import pycxsimulator
from random import choice as ranchoice, choices as ranchoices
from operator import add, sub

n = 50 # number of agents
r = 0.1 # neighbourhood radius
th = 0.5 # threshold for moving

def initialize():
    pass

def observe():
    cla()
    infected_no_mask = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == True and Agent.agentdict[ag]["wears mask"] == False]
    infected_with_mask = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == True and Agent.agentdict[ag]["wears mask"] == True]
    healthy_no_mask = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == False and Agent.agentdict[ag]["wears mask"] == False]
    healthy_with_mask = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == False and Agent.agentdict[ag]["wears mask"] == True]
    plot([Agent.agentdict[ag]["x"] for ag in infected_no_mask], [Agent.agentdict[ag]["y"] for ag in infected_no_mask], 'ro')
    plot([Agent.agentdict[ag]["x"] for ag in infected_with_mask], [Agent.agentdict[ag]["y"] for ag in infected_with_mask], 'yo')
    plot([Agent.agentdict[ag]["x"] for ag in healthy_no_mask], [Agent.agentdict[ag]["y"] for ag in healthy_no_mask], 'bo')
    plot([Agent.agentdict[ag]["x"] for ag in healthy_with_mask], [Agent.agentdict[ag]["y"] for ag in healthy_with_mask], 'co')
    axis('image')
    axis([0, 1, 0, 1])

def update():
    # ag = ranchoice(list(Agent.agentdict.keys()))
    for ag in list(Agent.agentdict.keys()):
        neighbors = [nb for nb in Agent.agentdict if (Agent.agentdict[ag]["x"]-Agent.agentdict[nb]["x"])**2 + (Agent.agentdict[ag]["y"] - Agent.agentdict[nb]["y"])**2 < r**2 and nb != ag]
        if len(neighbors) > 0:
            q = len([nb for nb in neighbors if Agent.agentdict[nb]["infected"] == Agent.agentdict[ag]["infected"]]) \
            / float(len(neighbors))
            if q < th:
                if Agent.agentdict[ag]["wears mask"] and Agent.agentdict[ag]["infected"] == False:
                    Agent.agentdict[ag]["infected"] = ranchoices([True,False],weights=(((60/100)*30),(abs((60/100)*30-100))))[0]
                elif Agent.agentdict[ag]["wears mask"] == False and Agent.agentdict[ag]["infected"] == False:
                    Agent.agentdict[ag]["infected"] = ranchoices([True,False],weights=(30,70))[0]
                # Agent.agentdict[ag]["infected"] = True
                # Agent.agentdict[ag]["symptoms"] = Agent.agentdict[ag]["symptoms"]
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
    #print(ag.overview())

pycxsimulator.GUI().start(func=[initialize, observe, update])
