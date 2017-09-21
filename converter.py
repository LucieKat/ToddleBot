
#TODO: FIX PING

def convert(line):
    #Preventing crashes later on:
    if line == "":
        return("?")

    line = line[1:].split(":")
    roughText = line[0].split(" ")
    if roughText[0] == "ING":
        return("PING")
    username = roughText[0].split("!")[0]
    if username != "tmi.twitch.tv": #more crash prevention
        try:
            channel = roughText[2]
        except:
            return("?")

    if roughText[1] == "PRIVMSG":
        if line[1][0] == "!":
            return("COMMAND", username, channel, line[1][1:-1])
        else:
            return("MESSAGE", username, channel, line[1][:-1])

    elif roughText[1] == "JOIN":
        return("JOIN", username, channel[:-1])
    elif roughText[1] == "PART":
        return("PART", username, channel[:-1])
    else:
        return("?")
