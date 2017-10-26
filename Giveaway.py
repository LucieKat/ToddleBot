from random import choice
from time import time

class Giveaway:
    ID = 0
    def __init__(self, channel, textLocation):
        self.ID = Giveaway.ID
        Giveaway.ID += 1
        self.channel = channel
        self.personList = []
        self.price = 100
        self.startingTime = time()
        self.textLocation = textLocation

    def addPerson(self, person):
        self.personList.append(person)

    def end(self):
        return choice(self.personList)

    def getText(self):
        with open(self.textLocation, 'r') as f:
            return(f.readline())