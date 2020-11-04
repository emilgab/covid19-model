# imports
from agent.covidagent import Agent
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
from PyCX import pycxsimulator
from random import choice as ranchoice, choices as ranchoices
from operator import add, sub
# imports for CLI
import string
import os
# imports for saving files in formats
import json
from datetime import datetime

n = 1 # frequency of spawning agents where 1 begin the most frequent
c = n
r = 0.1 # neighbourhood radius
th = 0.3 # threshold for moving

rows, columns = os.popen('stty size','r').read().split()

print("\n"*int(rows))
decorations = "--*-- ~ * ~ --*--"
decorations = decorations.center(int(columns))
hello = "The following outputs are the results of the simulation."
hello = hello.center(int(columns))
safe = "Stay safe and healthy."
safe = safe.center(int(columns))
covid = "🦠"
covid = covid.center(int(columns))
print(decorations)
print(hello)
print(safe)
print(covid)
print("-"*(int(columns)))

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
    global n, c
    # ag = ranchoice(list(Agent.agentdict.keys()))
    for ag in list(Agent.agentdict.keys()):
        neighbors = [nb for nb in Agent.agentdict if (Agent.agentdict[ag]["x"]-Agent.agentdict[nb]["x"])**2 + (Agent.agentdict[ag]["y"] - Agent.agentdict[nb]["y"])**2 < r**2 and nb != ag and "dry cough" in Agent.agentdict[nb]["symptoms"]]
        if len(neighbors) > 0:
            if Agent.agentdict[ag]["wears mask"] and Agent.agentdict[ag]["infected"] == False:
                Agent.agentdict[ag]["infected"] = result = ranchoices([True,False],weights=(((60/100)*30),(abs((60/100)*30-100))))[0]
                if result == True:
                    print(f"\n{ag} got infected and wore a mask")
                    Agent.newly_infected += 1
                    for x,y in Agent.agentdict[ag].items():
                        print(f"   {x}: {y}")
            elif Agent.agentdict[ag]["wears mask"] == False and Agent.agentdict[ag]["infected"] == False:
                Agent.agentdict[ag]["infected"] = result = ranchoices([True,False],weights=(30,70))[0]
                if result == True:
                    print(f"\n{ag} got infected and did not wear a mask")
                    Agent.newly_infected += 1
                    for x,y in Agent.agentdict[ag].items():
                        print(f"   {x}: {y}")
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
    if c%n == 0:
        ag = Agent()
    c+=1

pycxsimulator.GUI().start(func=[initialize, observe, update])
print("-"*(int(columns)))
final_data = {
            "total_agents":Agent.counter,
            "total_infected":len([x for x in list(Agent.agentdict.keys()) if Agent.agentdict[x]['infected'] == True]),
            "total_newly_infected":Agent.newly_infected,
            "developed_symptoms":len([x for x in list(Agent.agentdict.keys()) if Agent.agentdict[x]['symptoms'] != '']),
            "total_healthy_wearing_masks":len([x for x in list(Agent.agentdict.keys()) if Agent.agentdict[x]['wears mask'] == True and Agent.agentdict[x]['infected'] == False])
            }
print(f"Total agents: {final_data['total_agents']}")
print(f"Total infected: {final_data['total_infected']}")
print(f"Total newly infected: {final_data['total_newly_infected']}")
print(f"Agents showing symptoms: {final_data['developed_symptoms']}")
print(f"Total healthy agents wearing masks and not getting infected: {final_data['total_healthy_wearing_masks']}")
print("-"*(int(columns)))

while True:
    save_data = input("Do you want to save data on each of the agents in a JSON format? (data will be saved to the same location as the program) (y/n) ")
    if save_data.lower()[0] == "y":
        print("Writing JSON file...")
        filename = datetime.now().strftime("COV-19-results_%Y-%m-%d-%H-%M-%S")
        with open(f"{filename}.json", 'w') as f:
            json.dump(Agent.agentdict, f, indent=4)
        print("JSON file successfully saved!")
        break
    elif save_data.lower()[0] == "n":
        break
