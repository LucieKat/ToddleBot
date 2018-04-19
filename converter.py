from Message import Message, Join, Part, Command
def convert(line):
    #Preventing crashes later on:
    if line == "":
        return "?"
    line = line[1:].split(":", 1)
    rough_text = line[0].split(" ")
    if rough_text[0] == "ING":
        return "PING"
    if rough_text[0] == "toddle_bot.tmi.twitch.tv":
        if rough_text[3] == "=":
            channel = rough_text[4]
            usernames = line[1].split(" ")
            username_list = []
            for username in usernames:
                username = "".join(username.split())
                username_list.append(Join(username, channel))
            return(username_list)
        return "?"
    username = rough_text[0].split("!")[0]
    if username != "tmi.twitch.tv": #more crash prevention
        try:
            channel = rough_text[2]
        except IndexError:
            print("Error in convert: couldn't parse {}".format(line))
            return "?"

    if rough_text[1] == "PRIVMSG":
        if line[1][0] == "!":
            out_line = line[1].split(None, 1)
            out_line.append("")
            return Command(username, channel, out_line[1], out_line[0][1:])
        return Message(username, channel, line[1][:-1])

    if rough_text[1] == "JOIN":
        return Join(username, channel[:-1])
    if rough_text[1] == "PART":
        return Part(username, channel[:-1])
    return "?"
