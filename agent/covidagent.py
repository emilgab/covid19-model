import random
from pylab import random as lbrandom
class Agent:

    # "counter" is a class attribute used to keep track of the number of agent.
    # This is used as part of the naming scheme for each agent
    counter = 0
    # A dictionary containing each agent.
    # KEY: Name of an agent, e.g.: agent0001
    # VALUE: Gender(str), Infected(i/o), symptoms(str), wears mask(str).
    agentdict = {}
    # "symptoms_on_covid" is a dictionary containing the diseases.
    # KEY: Name of the symptom
    # VALUE: Toople containing weights used in chance.
    #   - First float: Chance of getting the symptom.
    #   - Second float: Chance of not getting the symptom.
    symptoms_on_covid = {"fever":(87.9,12.1),
                        "dry cough":(67.7,32.3),
                        "fatigue":(38.1,61.9),
                        "sputum production":(33.4,66.6),
                        "shortness of breath":(18.6,81.4),
                        "myalgia":(14.8,85.2),
                        "sore throat":(13.9,86.1),
                        "headache":(13.6,86.4),
                        }

    # Class attributes that contain the percentages of an agent wearing a mask, infected at initialisation and a counter that keeps track of newly infected.
    percentage_wearing_mask = 0
    percentage_infected = 0
    newly_infected = 0

    def __init__(self):
        '''
        Constructor function.
        This construct an agent with the following attributes:
        - gender: (str) "male" or "female"
        - unique_identifier: (str) an identifier that uniquely identifies that agent with a number (e.g. agent0001)
        - infected: (bool) on if the agent is infected from before
            - (if infected is True) symptoms: (str) listing the symptoms
        - mask: (bool) on if the agent wears a surgical mask (with earloops)
        '''
        self.gender = random.choice(["male","female"])
        self.name = "agent" + str(self.generate_unique_number().zfill(4))
        self.infected = random.choices([True, False],weights=(Agent.percentage_infected,100-Agent.percentage_infected))[0] # Indexing because random.choices() returns a list, we want to access the first element that is picked.
        self.mask = random.choices([True, False],weights=(Agent.percentage_wearing_mask,(100-Agent.percentage_wearing_mask)))[0]
        # Creates a dictionary in our agentdict where the key is the name of the agent and the value is the following dictionary.
        Agent.agentdict[self.name] = {
                                        "gender":self.gender,
                                        "infected":bool(self.infected),
                                        "symptoms":"",
                                        "wears mask":self.mask,
                                        "x":random.choice([0,1]),
                                        "y":lbrandom(),
                                        "direction_positive":False,
                                        "direction_negative" :False,
                                        "encountered infected" :[],
                                        "infected other agents" :[]
                                    }
        if Agent.agentdict[self.name]["x"] == 1:
            Agent.agentdict[self.name]["direction_positive"] = True
        if Agent.agentdict[self.name]["x"] == 0:
            Agent.agentdict[self.name]["direction_negative"] = True
        self.symptoms_results = self.infected_and_symptoms()
        # Assigns a string with symptoms to the "symptoms" entry in the agents dictionary.
        # The symptoms are returned from the function infected_and_symptoms()
        Agent.agentdict[self.name]["symptoms"] = ", ".join(filter(None,self.symptoms_results)) if self.symptoms_results else ""

    def generate_unique_number(self):
        '''
        Generates the unique number for the agent.
        Takes the class attribute "counter" and increment it by one for each agent created.
        OUTPUT: (str) returns the counter attribute incremented by one and changes the class attribute.
        '''
        Agent.counter += 1
        return str(Agent.counter)

    def infected_and_symptoms(self):
        '''
        Determines if symptoms are to be developed in an infected agent.
        OUTPUT: returns a list of symptoms (which is empty if no symptoms).
        '''
        # Because not everyone that is infected develop symptoms, we want to calculate the odds of developing symptoms if infected.
        if self.infected == True:
            develop_symptoms = random.choices([True, False],weights=(30.9,69.1))[0]
        else:
            develop_symptoms = False
        # Empty list which will be used to store symptoms if the agent is infected.
        symptoms = []
        # If our agent is infected and develops symptoms, we want to go over the probabilities of developing each symptom
        if self.infected == True and develop_symptoms == True:
            for key,value in self.symptoms_on_covid.items():
                symptoms.append(random.choices([key,None],weights=value)[0])
        return symptoms
