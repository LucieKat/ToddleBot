from time import sleep, time
import socket
from time import strftime, gmtime
import cfg
import converter
import handler

def chat(sock, msg, channel = None):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    # TODO: Create better timer interface in bot.py
    if channel is not None: 
        if time() - last_chatted > 60:
            sock.send("PRIVMSG #toddle_bot : PogChamp\r\n".encode())
        with open('outlog.txt', 'a') as f:
            f.write("OUT = " + msg + "\n")
        sock.send("PRIVMSG {} :{}\r\n".format(channel, msg).encode())
    elif msg.get_username() == "OUT":
        if time() - last_chatted > 60:
            sock.send("PRIVMSG #toddle_bot : PogChamp\r\n".encode())
        with open('outlog.txt', 'a') as f:
            f.write("OUT = " + msg.get_message() + "\n")
        sock.send("PRIVMSG {} :{}\r\n".format(msg.get_channel(), msg.get_message()).encode())
    else: 
        print("Something went horribly wrong here.")
    



with open('log.txt', 'w') as g:
    g.write("Channels = " + str(cfg.CHAN) + "\r\n")
with open('outlog.txt', 'w') as g:
    g.write("Time = {}".format(strftime("%d %b %Y %H:%M:%S", gmtime())))
s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("CAP REQ : twitch.tv/commands twitch.tv/membership \r\n".encode())

s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
for chan in cfg.CHAN:
    s.send("JOIN {}\r\n".format(chan).encode("utf-8"))
handler.load()
last_chatted = time()
last_checked = time()
chat(s, "HeyGuys", "#toddle_bot")


while True:
    response = s.recv(4096).decode("utf-8").split("\n")
    if time() - last_checked > 60:
        last_checked = time()
        handler.handle("DISTRIBUTE")
    for line in response:
        with open('log.txt', 'a') as f:
            try: 
                f.write("IN = " + line + '\r\n')
            except UnicodeEncodeError:
                break
        neatline = converter.convert(line)
        done = handler.handle(neatline)
        if done == "PING":
            s.send("PONG :tmi.twitch.tv \r\n".encode())
        elif done == "Success" or done == "?":
            pass
        elif "MSG" in done[0]:
            chat(s, done[0][4:], done[1])
            last_chatted = time()

        parts = line.split(":")
        if parts[0] == "PING ":
            s.send(("PONG :" + parts[1]).encode("utf-8"))
            print("PONGED")
    sleep(1/cfg.RATE)
    