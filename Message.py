from time import strftime, gmtime

class ChatAction:
    log_location = 'log.txt'
    def __init__(self, username, channel):
        self.username = username
        self.channel = channel
    
    def log(self):
        with open(self.log_location, 'a') as f:
            f.write("{} {:12} {:10}"
                    .format(strftime("%d %b %Y %H:%M:%S", gmtime()),
                            self.channel, self.username))
    def get_username(self):
        return self.username
    
    def get_channel(self):
        return self.channel

class Message(ChatAction):
    def __init__(self, username, channel, message):
        ChatAction.__init__(self, username, channel)
        self.message = message

    def log(self):
        ChatAction.log(self)
        with open(self.log_location, 'a') as f:
            f.write(": \t{} \n".format(self.message))

    def get_message(self):
        return self.message


class Command(Message):
    def __init__(self, username, channel, message, command):
        Message.__init__(self, username, channel, message)
        self.command = command

    def get_command(self):
        return self.command

    def log(self):
        ChatAction.log(self)
        with open(self.log_location, 'a') as f:
            f.write(": !{} {}\n"
                    .format(self.command, self.message))
    
class Join(ChatAction):
    def __init__(self, username, channel):
        ChatAction.__init__(self, username, channel)
    
    def log(self):
        ChatAction.log(self)
        with open(self.log_location, 'a') as f:
            f.write(" JOIN \n")

                   
class Part(ChatAction):
    def __init__(self, username, channel):
        ChatAction.__init__(self, username, channel)
    
    def log(self):
        ChatAction.log(self)
        with open(self.log_location, 'a') as f:
            f.write(" PART \n")
                 