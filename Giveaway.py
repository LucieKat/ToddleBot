class Person:
    def __init__(self, name, channel, lastBet = 0, points = 10):
        self.name = name
        self.channel = channel
        self.lastBet = lastBet
        self.points = points

    def addPoints(self, change):
        self.points += change

    def __str__(self):
        return self.name + "\t" + self.channel + "\t" + str(self.lastBet) + "\t" + str(self.points) + "\n"
