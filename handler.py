import random

import cfg
from Person import Person, personFromString
from Message import Join, Part, Message, Command


current_viewers = [] # each person represented as Persoonclass
gHublist = [] # each person represented as ["name", #points]
MOD_LIST = ["toddle_bot", "mst_toddle"] #TODO: Verplaats dit naar een logischer locatie.

def load():
    with open("ghublist.txt", "r") as f:
        line = f.readline()
        while line != "":
            gHublist.append(personFromString(line))
            line = f.readline()


# TODO: Import viewerlist from start text line
def handle(neatline):
    # constant string handling
    if neatline == "?":
        return "?"
    # TODO: Handle this.
    if neatline == "DISTRIBUTE":
        return distribute()
    if neatline == "PING":
        return "PING"
    
    
    if isinstance(neatline, list):
        channel = neatline[0].get_channel()
        for join in neatline:
            join.log()
            username = join.get_username()
            join_channel(username, channel)
        return "Success"
    
    username = neatline.get_username()
    channel = neatline.get_channel()
    neatline.log()
    if isinstance(neatline, Join):
        return join_channel(username, channel)

    if isinstance(neatline, Part):
        return part_channel(username, channel)

    if isinstance(neatline, Command):
        command = neatline.get_command()
        message = neatline.get_message()
        if command == "gamble":
            return gamble(message, username, channel)
        if command == "bonus":
            return bonus(message, username, channel)
        if command == "bonusall":
            return bonusall(message, username, channel)
        if command == "points" or command.lower() == cfg.CURRENCY:
            return points(username, channel)
        if command == "give":
            return give(message, username, channel)
        #default case:
        print("Err: Command + " + command + " not recognized")
        return "Err: Command + " + command + " not recognized"

        # TODO: bonusall (game specific commands),  bet/poll (outputs to text), duel, giveaway, lief (nonary, unary), nietlief, about, ranking, commands, speurtocht(maybe real)
        # TODO: questions, gamble tracking

    if isinstance(neatline, Message):
        return "Success"

    return "?"

def distribute():
    for viewer in current_viewers:
        viewer.addPoints(10)
    cfg.SAVE += 1
    if cfg.SAVE == 1:
        cfg.SAVE = 0
        with open('ghublist.txt', 'w') as f:
            for viewer in gHublist:
                f.write(str(viewer) + "\n")
    return "Success"

def findperson(value, personlist):
    for person in personlist:
        if value == person.name:
            return person
    return "notFound"

def gamble(message, username, channel):
    line = message.split(" ", 1)
    try:
        value = int(line[0])
    except ValueError:
        return ["MSG: Wel een getal invullen, grapjas", channel]
    if value < 1:
        return ["MSG: Wel een getal invullen, grapjas", channel]
    person = findperson(username, current_viewers)
    if person == "notFound":
        join_channel(username, channel)
        bonus(username + " 10", "toddle_bot", channel)
        return(gamble(message, username, channel))
    if person.points < value:
        return ["MSG: Je hebt maar {} {}!"
                .format(person.points, cfg.CURRENCY), channel]
    roll = random.randint(1, 100)
    if roll < 60:
        person.points -= value
        return ["MSG: Helaas, {}, je rolde {}! Je hebt nog {} {}!"
                .format(username, roll, person.points, cfg.CURRENCY), channel]
    if roll == 100:
        person.points += 2*value
        return ["MSG: Wow, {}, 100! Je hebt nu {} {}!"
                .format(username, person.points, cfg.CURRENCY), channel]
    person.points += value
    return ["MSG: Gefeliciteerd, {}, je rolde {}! Je hebt nu {} {}!"
            .format(username, roll, person.points, cfg.CURRENCY), channel]

def bonus(message, username, channel):
    line = message.split(" ")

    gifted = line[0]
    try:
        value = int(line[1])
    except IndexError:
        value = 100
    if username in MOD_LIST:
        person = findperson(gifted, gHublist)
        if person == "notFound":
            join_channel(username, channel)
            return bonus(message, username, channel)
        person.points += value
        return ["MSG: {p.name} heeft nu {p.points} {}!"
                .format(cfg.CURRENCY, p = person), channel]
    return ["MSG: Nee, je bent geen mod.", channel]

def bonusall(message, username, channel):
    try:
        line = message.split(" ", 1)
        value = int(line[0])
    except IndexError:
        value = 100
    if username in MOD_LIST:
        for person in current_viewers:
            if person.channel == channel:
                person.points += value
        return ["MSG: HET REGENT {} {}!"
                .format(value, cfg.CURRENCY).upper(), channel]
    return ["MSG: Nee, je bent geen mod.", channel]

def points(username, channel):
    person = findperson(username, gHublist)
    if person == "notFound":
        join_channel(username, channel)
        return points(username, channel)
    return ["MSG: Je hebt nu {} {}!"
            .format(person.points, cfg.CURRENCY), channel]

def give(message, username, channel):
    line = message.split(" ", 1)
    name = line[0]
    try:
        value = int(line[1])
    except ValueError:
        return ["MSG: Je hebt geen hoeveelheid ingevuld!", channel]
    giver = findperson(username, gHublist)
    if giver == "notFound":
        join_channel(username, channel)
        return give(message, username, channel)
    receiver = findperson(name, gHublist)
    if receiver == "notFound":
        return ["MSG: Het lijkt er op dat we \"{}\" niet kennen!"
                .format(name), channel]
    if value <= 0:
        return ["MSG: Goede poging, maar nee.", channel]
    if giver.points < value:
        return ["MSG: Je hebt niet genoeg {}!"
                .format(cfg.CURRENCY), channel]
    giver.points -= value
    receiver.points += value
    return ["MSG: {} heeft {} {} aan {} gegeven!"
            .format(username, value, cfg.CURRENCY, receiver.name), channel]
    
def join_channel(username, channel):
    foundperson = findperson(username, current_viewers)
    if foundperson == "notFound":
        foundperson = findperson(username, gHublist)
        if foundperson == "notFound":
            newperson = Person(username, channel)
            current_viewers.append(newperson)
            gHublist.append(newperson)
        else:
            current_viewers.append(foundperson)
    else:
        foundperson.channel = channel
    return "Success"

def part_channel(username, _):
    foundperson = findperson(username, current_viewers)
    if foundperson == "notFound":
        return "Err: Player " + username + " not found!"
    current_viewers.remove(foundperson)
    return "Success"
