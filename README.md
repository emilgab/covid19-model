# Covid-19 Model 🦠
_Using Artificial Intelligence to model the Covid-19 pandemic_

_This project is using [PyCX](https://github.com/hsayama/PyCX), revisioned by [Hiroki Sayama](https://github.com/hsayama)_


### Introduction
This project attempts to create a realistic Agent-Based Model to simulate how COVID-19 spreads from person to person.

### Project goal
The model will aim towards a most accurate representation of how the Covid-19 Virus behaves in how infection spreads from person to person. Furthermore, parameters will be added that optimizes the realism, e.g. if a person is wearing a surgical mask.

### The model
I have chosen to create an epidemic model based on the Agent-Based model. Each agent will represent a person that is either infected or not infected with COVID-19.
Persons that interact, or come close, to an infected agent has the possibility to be infected as well (when themselves are not infected).
