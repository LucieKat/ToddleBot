import cfg
from time import sleep, time
import socket
import converter
import handler

def chat(sock, msg, channel):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    # TODO: Create better timer interface in bot.py
    if time() - lastChatted > 60:
        sock.send("PRIVMSG #toddle_bot : PogChamp\r\n".encode())
    with open('outlog.txt', 'a') as f:
        f.write("OUT = " + msg + "\n")
    sock.send("PRIVMSG {} :{}\r\n".format(channel, msg).encode())

with open('log.txt', 'w') as f:
    f.write("Channels = " + str(cfg.CHAN) + "\r\n")
with open('outlog.txt', 'w') as f:
    f.write("Time =" + str(time()))
s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("CAP REQ : twitch.tv/commands twitch.tv/membership \r\n".encode())

s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
for channel in cfg.CHAN:
    s.send("JOIN {}\r\n".format(channel).encode("utf-8"))

lastChatted = time()
lastChecked = time()
chat(s, "HeyGuys", "#toddle_bot")


while True:
    response = s.recv(4096).decode("utf-8").split("\n")
    if time() - lastChecked > 60:
        lastChecked = time()
        handler.handle("DISTRIBUTE")
    for line in response:
        with open('log.txt', 'a') as f:
            f.write("IN = " + line + '\r\n')
            neatline = converter.convert(line)
        done = handler.handle(neatline)
        if done == "PING":
            s.send("PONG :tmi.twitch.tv \r\n".encode())
        elif done == "Success" or done == "?":
            pass
        elif "MSG" in done[0]:
            chat(s, done[0][4:], done[1])
            lastChatted = time()
            pass # TODO: Betere error handling.
            #s.send(("PRIVMSG #toddle_bot :" + done + "\r\n").encode())

        parts = line.split(":")
        if parts[0] == "PING ":
            s.send(("PONG :" + parts[1]).encode("utf-8"))
            print("PONGED")
    sleep(1/cfg.RATE)