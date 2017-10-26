with open("testin.txt", "w") as f:
    f.write(":tmi.twitch.tv 001 toddle_bot :Welcome, GLHF!\n")

def join(username, channel):
    with open("testin.txt", "a") as f:
        f.write(":" + username + "!" + username + "@" + username + ".tmi.twitch.tv JOIN " + channel + "\n")

def part(username, channel):
    with open("testin.txt", "a") as f:
        f.write(":" + username + "!" + username + "@" + username + ".tmi.twitch.tv PART " + channel + "\n")

def message(username, channel, msg):
    with open("testin.txt", "a") as f:
        f.write(":" + username + "!" + username + "@" + username + ".tmi.twitch.tv PRIVMSG " + channel + " :"
                + msg + "\n")


join("mst_toddle", "#toddle_bot")
join("moswarm", "#toddle_bot")
join("caught", "#toddle_bot")
join("creabeaa", "#toddle_bot")
join("rukkiducky", "#toddle_bot")
