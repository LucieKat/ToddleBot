import cfg
from time import sleep, time
import converter
import handler
with open('testlog.txt','w') as f:
    f.write("NEW TEST")


def chat(_, msg, channel):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    with open('testlog.txt', 'a') as f:
        f.write("OUT = " + msg + "\n")


lastChatted = time()
lastChecked = time()
chat("Empty", "HeyGuys", "#toddle_bot")

inFile = open('testin.txt', 'r')
while True:
    response = inFile.readline()
    if time() - lastChecked > 1:
        lastChecked = time()
        handler.handle("DISTRIBUTE")
    line = response
    print(line)
    with open('testlog.txt', 'a') as f:
        f.write("IN = " + line + '\r\n')
        neatline = converter.convert(line)
    done = handler.handle(neatline)
    if done == "Success" or done == "?":
        pass
    elif "MSG" in done[0]:
        chat("", done[0][4:], done[1])
        lastChatted = time()
        pass # TODO: Betere error handling.
        #s.send(("PRIVMSG #toddle_bot :" + done + "\r\n").encode())

    parts = line.split(":")
    sleep(1/cfg.RATE)