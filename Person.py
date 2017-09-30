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


def personFromString(inString):
    inString = inString.split('\t')
    return Person(inString[0], inString[1], int(inString[2]), int(inString[3]))

def main():
    pass

if __name__ == '__main__':
    main()