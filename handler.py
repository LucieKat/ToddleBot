import cfg
import random
from Person import Person
from Person import personFromString
from Giveaway import Giveaway

currentViewers = [] # each person represented as Persoonclass
saveCounter = 0
gHublist = [] # each person represented as ["name", #points]
modList = ["toddle_bot", "mst_toddle", "gamershuba", "gamershubb", "gamershubc"]
# neatline = (type, username, channel, [message])
giveawayList = []
with open('log.txt', 'a') as f:
    f.write("Ayy")


def handle(neatline):

    # constant string handling
    if neatline == "?":
        return "?"
    elif neatline == "DISTRIBUTE":
        print("gHublist")
        for person in gHublist:
            print(person)
        print("currentViewers")
        for person in currentViewers:
            print(person)
        for viewer in currentViewers:
            viewer.addPoints(10)
        cfg.SAVE += 1
        if cfg.SAVE == 1:
            cfg.SAVE = 0
            with open('ghublist.txt', 'w') as f:
                for viewer in currentViewers:
                    f.write(str(viewer))
            # TODO: Import viewerlist from file
        return "Success"
    elif neatline == "PING":
        return "PING"

    # simple string handling
    [messageType, username, channel] = neatline[:3]
    if messageType == "MESSAGE":
        with open('log.txt', 'a') as f:
            f.write("MESSAGE = " + username + ": " + neatline[3] + " "+ channel + "\n")
        return "Success"
    elif messageType == "JOIN":
        foundperson = findperson(username, currentViewers)
        if foundperson == "notFound":
            foundperson = findperson(username, gHublist)
            if foundperson == "notFound":
                newPerson = Person(username, channel)
                currentViewers.append(newPerson)
                gHublist.append(newPerson)
                # TODO: adopt save to join multiple persons with same name
            else:
                currentViewers.append(foundperson)
        else:
            foundperson.channel = channel
        return "Success"
    elif neatline[0] == "PART":

        try:
            foundperson = findperson(username, currentViewers)
            currentViewers.remove(foundperson)
            return "Success"
        except:
            return "Err: Player " + username + " not found!"
    #the problem
    elif messageType == "COMMAND":
        with open('log.txt', 'a') as f:
            f.write("COMMAND = " + username + ": " + neatline[3] + " "+ channel + "\n")
        neatCommand = neatline[3].split(' ')
        if neatCommand[0] == "gamble":
            return gamble(neatCommand, username, channel)
        elif neatCommand[0] == "bonus":
            return bonus(neatCommand, username, channel)
        elif neatCommand[0] == "bonusall":
            return bonusall(neatCommand, username, channel)
        elif neatCommand[0] == "points":
            return points(username, channel)
        elif neatCommand[0] == "give":
            return give(neatCommand, username, channel)

        return "Success"
        # TODO: check command in a list of commands, then return appropriate text
        # TODO: bonusall (game specific commands),  bet/poll (outputs to text), duel, giveaway, lief (nonary, unary), nietlief, about, ranking, commands, speurtocht(maybe real)
        # TODO: TEST: bonus, bonusall, points, give,
        # TODO: questions, gamble tracking
        # TODO: Moderation


    #error catching
    else:
        print("Err: Command + " + neatline + " not recognized")
        return "Err: Command + " + neatline + " not recognized"


def findperson(value, list):
    for person in list:
        if value == person.name:
            return person
    return "notFound"

def gamble(neatCommand, username, channel):
    try:
        value = int(neatCommand[1])
    except:
        return ["MSG: Wel een getal invullen grapjas", channel]
    person = findperson(username, currentViewers)
    if person == "notFound":
        return ["MSG: Even geduld, je kan zo pas gamblen!", channel]
    elif person.points < value:
        return ["MSG: Je hebt maar " + str(person.points) + " GHubbies!", channel]
    else:
        roll = random.randint(1,100)
        if roll < 66:
            person.points -= value
            return ["MSG: Helaas, " + username + ", je rolde " + str(roll) + "! Je hebt nog " + str(person.points) + " GHubbies!", channel]
        elif roll == 100:
            person.points += 2*value
            return ["MSG: Wow, " + username + ", 100! Je hebt nu " + str(person.points) + " GHubbies!", channel]
        else:
            person.points += value
            return ["MSG: Gefeliciteerd, " + username + ", je rolde " + str(roll) + "! Je hebt nu " + str(person.points) + " GHubbies!", channel]


def bonus(neatCommand, username, channel):
    gifted = neatCommand[1]
    try:
        value = int(neatCommand[2])
    except IndexError:
        value = 100
    if username in modList:
        person = findperson(gifted, gHublist)
        if person == "notFound":
            return ["MSG: Ik kan " + gifted + " niet vinden!", channel]
        else:
            person.points += value
            return ["MSG: " + person.name + " heeft nu " + str(person.points) + " GHubbies!", channel]
    else:
        print(username)
        return ["MSG: Nee, je bent geen mod.", channel]

def bonusall(neatCommand, username, channel):
    try:
        value = int(neatCommand[1])
    except IndexError:
        value = 100
    if username in modList:
        for person in currentViewers:
            if person.channel == channel:
                person.points += value
        return ["MSG: HET REGENT " + str(value) + " GHUBBIES!", channel]
    else:
        return ["MSG: Nee, je bent geen mod.", channel]

def points(username, channel):
    person = findperson(username, gHublist)
    if person == "notFound":
        return ["MSG: Het lijkt er op dat je nog geen GHubbies hebt!", channel]
    else:
        return ["MSG: Je hebt nu " + person.points + "GHubbies!", channel]

def give(neatCommand, username, channel):
    userReceiver = neatCommand[1]
    try:
        value = int(neatCommand[2])
    except:
        return ["MSG: Je hebt geen hoeveelheid ingevuld!", channel]
    giver = findperson(username, gHublist)
    if giver == "notFound":
        return ["MSG: Het lijkt er op dat je nog geen GHubbies hebt!", channel]
    else:
        receiver = findperson(userReceiver, gHublist)
        if receiver == "notFound":
            return ["MSG: Het lijkt er op dat we je ontvanger niet kennen!", channel]
        elif value <= 0:
            return ["MSG: Goede poging, maar nee.", channel]
        elif giver.points < value:
            return ["MSG: Je hebt niet genoeg GHubbies!", channel]
        else:
            giver.points -= value
            receiver.points += value
            return ["MSG: " + username + " heeft " + str(value) + " GHubbies aan " + receiver.name + " gegeven!", channel]

def giveaway(neatCommand, username, channel):
    for giveaway in giveawayList:
        if giveaway.channel == channel:
            return ["MSG: " + giveaway.getText()]
    if username in modList:
        location = neatCommand[1]
        try:
            channel = neatCommand[2]
            try:
                duration = neatCommand[3]
            except IndexError:
                duration = 3600
        except IndexError:
            pass
        giveaway = Giveaway(channel, location)
        giveawayList.append(giveaway)
        return ["ACT: Giveaway " + str(giveaway.ID) + ' ' + str(giveaway.startingTime) + ' ' + str(giveaway.duration)]
        # TODO: Make bot responsive to ACT, in the right way, too.
        # TODO: Make ticket purchase + giveaway end work
    else:
        return ["MSG: Er is op het moment geen giveaway bezig!", channel]

