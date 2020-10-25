# imports
import random

# CLASSES
class Agent:

    counter = 0
    agentdict = {}
    symptoms_on_covid = {"fever":(87.9,12.1),
                        "dry cough":(67.7,32.3),
                        "fatigue":(38.1,61.9),
                        "sputum production":(33.4,66.6),
                        "shortness of breath":(18.6,81.4),
                        "myalgia":(14.8,85.2),
                        "sore throat":(13.9,86.1),
                        "headache":(13.6,86.4),
                        }

    def __init__(self):
        '''
        Constructor function.
        '''
        self.gender = random.choice(["male","female"])
        self.unique_identifier = self.generate_unique_number()
        self.name = "agent" + str(self.unique_identifier.zfill(4))
        self.infected, self.symptoms = self.infected_and_symptoms()
        self.mask = random.choice([True,False])
        Agent.agentdict[self.name] = {"gender":self.gender,"infected":bool(self.infected),"symptoms":", ".join(filter(None,self.symptoms)) if self.symptoms else "no","wears mask":"yes" if self.mask else "no"}

    def generate_unique_number(self):
        Agent.counter += 1
        return str(Agent.counter)

    def infected_and_symptoms(self):
        infected = random.choices([True, False],weights=(90,10))
        develop_symptoms = random.choices([True, False],weights=(30.9,69.1))
        symptoms = []
        if infected and develop_symptoms:
            for key,value in self.symptoms_on_covid.items():
                symptoms.append(random.choices([key,None],weights=value)[0])
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
