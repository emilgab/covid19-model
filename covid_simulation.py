# imports
import random

# CLASSES
class Agent:

    counter = 0
    agentdict = {}

    def __init__(self):
        '''
        Constructor function.
        '''
        self.gender = self.assign_gender()
        self.unique_identifier = self.generate_unique_number()
        self.name = "agent" + str(self.unique_identifier.zfill(4))
        Agent.agentdict[self.name] = {"gender":self.gender}


    def assign_gender(self):
        return random.choice(["M","F"])

    def generate_unique_number(self):
        Agent.counter += 1
        return str(Agent.counter)

    def overview(self):
        for x,y in Agent.agentdict.items():
            print(f"{x}:")
            for x2,y2 in y.items():
                print(f"\t{x2}:{y2}")

x = Agent()
y = Agent()
x.overview()
