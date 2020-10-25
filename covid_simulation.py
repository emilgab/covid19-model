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
        self.gender = random.choice(["M","F"])
        self.unique_identifier = self.generate_unique_number()
        self.name = "agent" + str(self.unique_identifier.zfill(4))
        self.infected, self.symptoms = self.infected_and_symptoms()
        self.mask = random.choice([True,False])
        Agent.agentdict[self.name] = {"gender":self.gender,"infected":self.infected,"symptoms":self.symptoms if self.symptoms else "no","wears mask":"yes" if self.mask else "no"}

    def generate_unique_number(self):
        Agent.counter += 1
        return str(Agent.counter)

    def infected_and_symptoms(self):
        infected = random.choice([True, False])
        symptoms = []
        if infected:
            symptoms.append(random.choice(["fever","dry cough","fatigue","sputum","shortness of breath","sore throat","headache","myalgia"]))
        return infected, symptoms

    def overview(self):
        for x,y in Agent.agentdict.items():
            print(f"{x}:")
            for x2,y2 in y.items():
                print(f"   {x2}: {y2}")
            print("")

for i in range(6):
    x = Agent()

x.overview()
