# Covid-19 Model 🦠
_Using Artificial Intelligence to model the Covid-19 pandemic_

_This project is using [PyCX](https://github.com/hsayama/PyCX), revisioned by [Hiroki Sayama](https://github.com/hsayama)_


### Introduction
As part of the OsloMet Course: "ACIT4610: Evolutionary artificial intelligence and robotics", this project will try to create a realistic epidemic model based on complex system models.

### Project goal
The model will aim towards a most accurate representation of how the Covid-19 Virus behaves in regards of infection rate, recovery rate and spread. Furthermore, parameters will be added that optimizes the realism, e.g. if a person is wearing a surgical mask.

### The model
I have chosen to create an epidemic model based on the Agent-Based model. Each agent will represent a person that is either infected or not infected with COVID-19.
Persons that interact, or come close, to an infected agent has the possibility to be infected as well (when themselves are not infected)
