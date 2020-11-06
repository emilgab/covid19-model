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
Agent.percentage_wearing_mask = 50
Agent.percentage_infected = 5
superspreader_threshold = 4

# Dictionary that contains the agents that are being deleted in the update function when an agent has crossed to the other side of our simulation
deleted_agents = {}

# Used to measure the window size of the terminal
rows, columns = os.popen('stty size','r').read().split()

# The following print statements are for decoration and the "welcome" screen for the simulation
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

# Creates a variable containing the names of the symptoms and weights that are also found in the Agent Class Attribute "symptoms_on_covid"
symptoms_on_covid = Agent.symptoms_on_covid

def infected_and_symptoms(agent_name):
    '''
    Determines if symptoms are to be developed in an infected agent.
    OUTPUT: returns a list of symptoms (which is empty if no symptoms).
    '''
    # Because not everyone that is infected develop symptoms, we want to calculate the odds of developing symptoms if infected.
    develop_symptoms = ranchoices([True, False],weights=(30.9,69.1))[0]
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
    # Creates different list containing infected and healthy agents that wears a mask and not (using list comprehension)
    infected_no_mask = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == True and Agent.agentdict[ag]["wears mask"] == False]
    infected_with_mask = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == True and Agent.agentdict[ag]["wears mask"] == True]
    healthy_no_mask = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == False and Agent.agentdict[ag]["wears mask"] == False]
    healthy_with_mask = [ag for ag in Agent.agentdict if Agent.agentdict[ag]["infected"] == False and Agent.agentdict[ag]["wears mask"] == True]
    # Plots each agent with different colors based on its status (infected, healthy, infected with mask, healthy with mask)
    plot([Agent.agentdict[ag]["x"] for ag in infected_no_mask], [Agent.agentdict[ag]["y"] for ag in infected_no_mask], 'ro')
    plot([Agent.agentdict[ag]["x"] for ag in infected_with_mask], [Agent.agentdict[ag]["y"] for ag in infected_with_mask], 'yo')
    plot([Agent.agentdict[ag]["x"] for ag in healthy_no_mask], [Agent.agentdict[ag]["y"] for ag in healthy_no_mask], 'bo')
    plot([Agent.agentdict[ag]["x"] for ag in healthy_with_mask], [Agent.agentdict[ag]["y"] for ag in healthy_with_mask], 'co')
    axis('image')
    axis([0, 1, 0, 1])

def update():
    global n, c, deleted_agents
    # Iterates each available agent
    for ag in list(Agent.agentdict.keys()):
        # Uses list comprehension to create a list of neighbours around our agent that is infected and has "dry cough"
        neighbors = [nb for nb in Agent.agentdict if (Agent.agentdict[ag]["x"]-Agent.agentdict[nb]["x"])**2 + (Agent.agentdict[ag]["y"] - Agent.agentdict[nb]["y"])**2 < r**2 and nb != ag and "dry cough" in Agent.agentdict[nb]["symptoms"]]
        # If the length of infected neighbours (and with "dry cough") is more than 0, we want to determine if our healthy agent is infected.
        if len(neighbors) > 0:
            # We want to keep track of wether an agent has encountered the infected agent before to stop repeating the process more than once
            if neighbors[0] not in Agent.agentdict[ag]["encountered infected"]:
                # If the infected agent has not been encountered before, we want to add the name of the agent to our agents "encountered infected" entry.
                Agent.agentdict[ag]["encountered infected"].append(neighbors[0])
                # If our agent wears a mask and is not infected, we execute this code block.
                if Agent.agentdict[ag]["wears mask"] and Agent.agentdict[ag]["infected"] == False:
                    # Calculates, based on probability of getting infected by using a mask, if our agent is not infected.
                    Agent.agentdict[ag]["infected"] = result = ranchoices([True,False],weights=(((60/100)*30),(abs((60/100)*30-100))))[0]
                    # If infected, we want to print an output about this and calculate if symptoms are developed.
                    if result == True:
                        print(f"\n{ag} got infected and wore a mask.")
                        print(f"Possibly infected by {', '.join(neighbors)}")
                        # Appends the name of our agent to the infected agent to say that that agent has infected our healthy agent.
                        Agent.agentdict[neighbors[0]]["infected other agents"].append(ag)
                        # Adds the information that our agent has been infected by the infected agent.
                        Agent.agentdict[ag]["infected by"] = neighbors[0]
                        # Stores the results of our function to determine if they develop any symptoms.
                        symptom_function_results = infected_and_symptoms(ag)
                        # Stores the symptoms in our agents dictionary
                        Agent.agentdict[ag]["symptoms"] = ", ".join(filter(None,symptom_function_results)) if symptom_function_results else ""
                        # Prints out information on the symptoms
                        if Agent.agentdict[ag]["symptoms"] != "":
                            print(f"{ag} developed the following symptoms: {Agent.agentdict[ag]['symptoms']}")
                        else:
                            # if no symptoms, we print out that no symptoms developed
                            print(f"No symptoms developed.")
                        # increments the count of newly infected agents with 1
                        Agent.newly_infected += 1
                        # prints out the information about our agent that became infected.
                        for x,y in Agent.agentdict[ag].items():
                            print(f"   {x}: {y}")
                # This if statement is pretty similar to the one above.
                # The only difference is that is checks if the agent is not wearing a mask.
                # If the agent is not wearing a mask, the chance of getting infected is changed.
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

        # A try/except that will move our agents to the opposite side of our visualisation.
        # If our agent has crossed over, then we delete that agent and adds the information to our deleted_agents dictionary
        # We want to randomly add or subtract a value from the y-axis in order to create some random behaviour because humans does not entirely move in a straigt line.
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
    # This if statement creates a new instance of our agent class based on the frequency.
    if c%f == 0:
        ag = Agent()
        c = 0
    c+=1

pycxsimulator.GUI().start(func=[initialize, observe, update])
# merges the dictionaries deleted_agents, and the Agent.agentdict for output and JSON purposes.
merged_dictionaries = {**deleted_agents, **Agent.agentdict}
def summary():
    '''
    Prints out a short summary of the simulation
    '''
    print("")
    print("-"*(int(columns)))
    print("Summary")
    print("-"*(int(columns)))
    # This dictionary goes through the merged dictionary to create data on the simulation.
    final_data = {
                # Uses the Agent Class Attribute Counter
                "total_agents":Agent.counter,
                # Uses list comprehension inside a len() to count the instances that were infected.
                "total_infected":len([x for x in list(merged_dictionaries.keys()) if merged_dictionaries[x]['infected'] == True]),
                # Uses the newly_infected counter
                "total_newly_infected":Agent.newly_infected,
                # Calculates how many superspreaders by using list comprehension
                "num_of_superspreaders":len([x for x in list(merged_dictionaries.keys()) if len(merged_dictionaries[x]["infected other agents"]) >= superspreader_threshold]),
                # Calculates how many agents that developed any symptoms.
                "developed_symptoms":len([x for x in list(merged_dictionaries.keys()) if merged_dictionaries[x]['symptoms'] != '']),
                # Calculates how many healthy agents that wore a mask, and did not get infected.
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

# Menu code block that list options at the end.
while True:
    menu_items = input("Menu options:\n- Output data on every agent (show)\n- Store data as a JSON file in current path (json)\n- Show summary again (summary)\n- Continue simulation (con)\n- Exit (q)\n: ")
    if menu_items.lower() == "show":
        # Prints out all of the information on every agent
        for x,y in merged_dictionaries.items():
            print(f"{x}: ")
            for x2,y2 in y.items():
                print(f"   {x2}: {y2}")
            print("")
    elif menu_items.lower() == "con":
        # Continues the simulation and opens the GUI
        pycxsimulator.GUI().start(func=[initialize, observe, update])
    elif menu_items.lower() == "json":
        # Dumps the merged dictionary to a JSON file that will be stored in the same dictionary as this program
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
