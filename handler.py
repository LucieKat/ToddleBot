import cfg
import random
currentViewers = [] # each person represented as ["name", "channel", #points]
saveCounter = 0
gHublist = [] # each person represented as ["name", #points]

# neatline = (type, username, channel, [message])
def handle(neatline):


    # constant string handling
    if neatline == "?":
        return("?")
    elif neatline == "DISTRIBUTE":
        for viewer in currentViewers:
            viewer[2]+= 10
        cfg.SAVE += 1
        if cfg.SAVE == 5:
            cfg.SAVE = 0
            for viewer in currentViewers:
                viewerFound = False
                for savedPerson in gHublist:
                    print(viewer[0], savedPerson[0])
                    if viewer[0] == savedPerson[0]:
                        savedPerson[1] = viewer[2]
                        viewerFound = True
                    if viewerFound:
                        break
                if not viewerFound:
                    gHublist.append([viewer[0], viewer[2]])
        # TODO: write away gHublist to .txt
        print(currentViewers)
        print(gHublist)
        return "Success"
    elif neatline == "PING":
        return "PING"

    # simple string handling
    if neatline[0] == "MESSAGE":
        pass #TODO: maybe log, probably language filter
        return "Success"
    elif neatline[0] == "JOIN":
        viewerFound = False
        for viewer in gHublist:
            if viewer[0] == neatline[1]:
                currentViewers.append([viewer[0], neatline[2], viewer[1]])
                viewerFound = True
            if viewerFound:
                break
        if not viewerFound:
            currentViewers.append([neatline[1], neatline[2], 10])
        return "Success"
    elif neatline[0] == "PART":
        try:
            currentViewers.remove(neatline[1])
            return "Success"
        except:
            return "Err: Player " + neatline[1] + " not found!"
    #the problem
    elif neatline[0] == "COMMAND":
        neatCommand = neatline[3].split(' ')
        print(neatCommand)
        if neatCommand[0] == "gamble":
            try:
                neatCommand[1] = int(neatCommand[1])
            except:
                return ["MSG: Wel een getal invullen grapjas", neatline[2]]
            for viewer in currentViewers:
                if neatline[1] == viewer[0]:
                    if viewer[2] < neatCommand[1]:
                        return ["MSG: Je hebt maar " + str(viewer[2]) + " GHubbies!", neatline[2]]
                    else:
                        value = random.randint(1,100)
                        if value < 66:
                            viewer[2] -= neatCommand[1]
                            return ["MSG: Helaas, je rolde " + str(value) + "! Je hebt nog " + str(viewer[2]) + " GHubbies!", neatline[2]]
                        elif value == 100:
                            viewer[2] += 2*neatCommand[1]
                            return ["MSG: Wow, 100! Je hebt nu " + str(viewer[2]) + " GHubbies!", neatline[2]]
                        else:
                            viewer[2] += neatCommand[1]
                            return ["MSG: Gefeliciteerd, je rolde " + str(value) + "! Je hebt nu " + str(viewer[2]) + " GHubbies!", neatline[2]]
            return ["MSG: Even geduld, je kan zo pas gamblen!", neatline[2]]
        return "Success"
        # TODO: check command in a list of commands, then return appropriate text
        # TODO: bonus, bonusall, points, bet, give, duel, giveaway, lief (nonary, unary), nietlief, about, ranking, commands, speurtocht


    #error catching
    else:
        print("Err: Command + " + neatline + " not recognized")
        return "Err: Command + " + neatline + " not recognized"
