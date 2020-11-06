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

f = 1 # frequency of spawning agents where 1 begin the most frequent
c = f
r = 0.1 # neighbourhood radius
Agent.percentage_wearing_mask = 0
Agent.percentage_infected = 5
superspreader_treshold = 4

deleted_agents = {}

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

symptoms_on_covid = {"fever":(87.9,12.1),
                    "dry cough":(67.7,32.3),
                    "fatigue":(38.1,61.9),
                    "sputum production":(33.4,66.6),
                    "shortness of breath":(18.6,81.4),
                    "myalgia":(14.8,85.2),
                    "sore throat":(13.9,86.1),
                    "headache":(13.6,86.4),
                    }

def infected_and_symptoms(agent_name):
    '''
    Calculates wether an agent is to be infected, and if so calculates if and which symptoms to appear.
    OUTPUT: (toople) returns a True/False value of infected and a list of symptoms (which is empty if not infected).
    '''
    # Because not everyone that is infected develop symptoms, we want to calculate the odds of developing symptoms if infected.
    develop_symptoms = ranchoices([True, False],weights=(100,0))[0]
    # Empty list which will be used to store symptoms if the agent is infected.
    symptoms = []
    # If our agent is infected and develops symptoms, we want to go over the probabilities of developing each symptom
    if develop_symptoms == True:
        for key,value in symptoms_on_covid.items():
            symptoms.append(ranchoices([key,None],weights=value)[0])
    return symptoms

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
    global n, c, deleted_agents
    # ag = ranchoice(list(Agent.agentdict.keys()))
    for ag in list(Agent.agentdict.keys()):
        neighbors = [nb for nb in Agent.agentdict if (Agent.agentdict[ag]["x"]-Agent.agentdict[nb]["x"])**2 + (Agent.agentdict[ag]["y"] - Agent.agentdict[nb]["y"])**2 < r**2 and nb != ag and "dry cough" in Agent.agentdict[nb]["symptoms"]]
        if len(neighbors) > 0:
            if neighbors[0] not in Agent.agentdict[ag]["encountered infected"]:
                Agent.agentdict[ag]["encountered infected"].append(neighbors[0])
                if Agent.agentdict[ag]["wears mask"] and Agent.agentdict[ag]["infected"] == False:
                    Agent.agentdict[ag]["infected"] = result = ranchoices([True,False],weights=(((60/100)*30),(abs((60/100)*30-100))))[0]
                    if result == True:
                        print(f"\n{ag} got infected and wore a mask.")
                        print(f"Possibly infected by {', '.join(neighbors)}")
                        Agent.agentdict[neighbors[0]]["infected other agents"].append(ag)
                        Agent.agentdict[ag]["infected by"] = ', '.join(neighbors)
                        symptom_function_results = infected_and_symptoms(ag)
                        Agent.agentdict[ag]["symptoms"] = ", ".join(filter(None,symptom_function_results)) if symptom_function_results else ""
                        if Agent.agentdict[ag]["symptoms"] != "":
                            print(f"{ag} developed the following symptoms: {Agent.agentdict[ag]['symptoms']}")
                        else:
                            print(f"No symptoms developed.")
                        Agent.newly_infected += 1
                        for x,y in Agent.agentdict[ag].items():
                            print(f"   {x}: {y}")
                elif Agent.agentdict[ag]["wears mask"] == False and Agent.agentdict[ag]["infected"] == False:
                    Agent.agentdict[ag]["infected"] = result = ranchoices([True,False],weights=(30,70))[0]
                    if result == True:
                        print(f"\n{ag} got infected and did not wear a mask")
                        print(f"Possibly infected by {', '.join(neighbors)}")
                        Agent.agentdict[neighbors[0]]["infected other agents"].append(ag)
                        Agent.agentdict[ag]["infected by"] = ', '.join(neighbors)
                        symptom_function_results = infected_and_symptoms(ag)
                        Agent.agentdict[ag]["symptoms"] = ", ".join(filter(None,symptom_function_results)) if symptom_function_results else ""
                        if Agent.agentdict[ag]["symptoms"] != "":
                            print(f"{ag} developed the following symptoms: {Agent.agentdict[ag]['symptoms']}")
                        else:
                            print(f"No symptoms developed.")
                        Agent.newly_infected += 1
                        for x,y in Agent.agentdict[ag].items():
                            print(f"   {x}: {y}")

        try:
            if Agent.agentdict[ag]["direction_positive"] == True:
                if Agent.agentdict[ag]["x"] < 0:
                    deleted_agents[ag] = Agent.agentdict[ag]
                    del Agent.agentdict[ag]
                Agent.agentdict[ag]["x"] -= 0.01
                rnd_op = ranchoice([add, sub, None])
                if rnd_op != None:
                    Agent.agentdict[ag]["y"] = rnd_op(Agent.agentdict[ag]["y"], 0.01)
            if Agent.agentdict[ag]["direction_negative"] == True:
                if Agent.agentdict[ag]["x"] > 1:
                    deleted_agents[ag] = Agent.agentdict[ag]
                    del Agent.agentdict[ag]
                Agent.agentdict[ag]["x"] += 0.01
                rnd_op = ranchoice([add, sub, None])
                if rnd_op is not None:
                    Agent.agentdict[ag]["y"] = rnd_op(Agent.agentdict[ag]["y"], 0.01)
        except:
            pass
    if c%f == 0:
        ag = Agent()
    c+=1

pycxsimulator.GUI().start(func=[initialize, observe, update])
merged_dictionaries = {**deleted_agents, **Agent.agentdict}
def summary():
    print("")
    print("-"*(int(columns)))
    print("Summary")
    print("-"*(int(columns)))
    final_data = {
                "total_agents":Agent.counter,
                "total_infected":len([x for x in list(merged_dictionaries.keys()) if merged_dictionaries[x]['infected'] == True]),
                "total_newly_infected":Agent.newly_infected,
                "num_of_superspreaders":len([x for x in list(merged_dictionaries.keys()) if len(merged_dictionaries[x]["infected other agents"]) > superspreader_treshold]),
                "developed_symptoms":len([x for x in list(merged_dictionaries.keys()) if merged_dictionaries[x]['symptoms'] != '']),
                "total_healthy_wearing_masks":len([x for x in list(merged_dictionaries.keys()) if merged_dictionaries[x]['wears mask'] == True and merged_dictionaries[x]['infected'] == False])
                }
    print(f"Total agents: {final_data['total_agents']}")
    print(f"Total infected: {final_data['total_infected']}")
    print(f"Total newly infected: {final_data['total_newly_infected']}")
    print(f"Total superspreaders: {final_data['num_of_superspreaders']}")
    print(f"Agents showing symptoms: {final_data['developed_symptoms']}")
    print(f"Total healthy agents wearing masks and not getting infected: {final_data['total_healthy_wearing_masks']}")
    print("-"*(int(columns)))
summary()

while True:
    menu_items = input("Menu options:\n- Output data on every agent (show)\n- Store data as a JSON file in current path (json)\n- Show summary again (summary)\n- Continue simulation (con)\n- Exit (q)\n: ")
    if menu_items.lower() == "show":
        for x,y in merged_dictionaries.items():
            print(f"{x}: ")
            for x2,y2 in y.items():
                print(f"   {x2}: {y2}")
            print("")
    elif menu_items.lower() == "con":
        pycxsimulator.GUI().start(func=[initialize, observe, update])
    elif menu_items.lower() == "json":
        print("")
        print("-"*(int(columns)))
        print("Writing JSON file...")
        filename = datetime.now().strftime("COV-19-results_%Y-%m-%d-%H-%M-%S")
        with open(f"{filename}.json", 'w') as f:
            json.dump(merged_dictionaries, f, indent=4)
        print("JSON file successfully saved!")
        print("-"*(int(columns)))
    elif menu_items.lower() == "summary":
        summary()
    elif menu_items.lower() == "q":
        break
