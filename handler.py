import cfg
import random
from Person import Person
from Person import personFromString

currentViewers = [] # each person represented as Persoonclass
saveCounter = 0
gHublist = [] # each person represented as ["name", #points]

# neatline = (type, username, channel, [message])

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
            f.write("MESSAGE = " + username + ": " + neatline[3] + " "+ channel + "\r\n")
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
        # TODO: Fix
        try:
            currentViewers.remove(neatline[1])
            return "Success"
        except:
            return "Err: Player " + username + " not found!"
    #the problem
    elif messageType == "COMMAND":
        neatCommand = neatline[3].split(' ')
        if neatCommand[0] == "gamble":
            try:
                neatCommand[1] = int(neatCommand[1])
            except:
                return ["MSG: Wel een getal invullen grapjas", channel]
            foundperson = findperson(username, currentViewers)
            if foundperson == "notFound":
                return ["MSG: Even geduld, je kan zo pas gamblen!", channel]
            else:
                if foundperson.points < neatCommand[1]:
                    return ["MSG: Je hebt maar " + str(foundperson.points) + " GHubbies!", channel]
                else:
                    value = random.randint(1,100)
                    if value < 66:
                        foundperson.points -= neatCommand[1]
                        return ["MSG: Helaas, je rolde " + str(value) + "! Je hebt nog " + str(foundperson.points) + " GHubbies!", channel]
                    elif value == 100:
                        foundperson.points += 2*neatCommand[1]
                        return ["MSG: Wow, 100! Je hebt nu " + str(foundperson.points) + " GHubbies!", neatline[2]]
                    else:
                        foundperson.points += neatCommand[1]
                        return ["MSG: Gefeliciteerd, je rolde " + str(value) + "! Je hebt nu " + str(foundperson.points) + " GHubbies!", channel]

        return "Success"
        # TODO: check command in a list of commands, then return appropriate text
        # TODO: bonus, bonusall (game specific commands), points, bet/poll (outputs to text), give, duel, giveaway, lief (nonary, unary), nietlief, about, ranking, commands, speurtocht(maybe real)
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