__author__ = 'ohell_000'


import globals as _
import player
import admin
import threading

class Peer(threading.Thread):
    def __init__(self, socket, address, lock):
        threading.Thread.__init__(self)
        self.state = _.STATE_NAME1
        self.SOCKET = socket
        self.ADDRESS = address
        self.input_buffer = ""
        self.linkdead = False
        self.linkdead_count = 0
        self.command_buf = []
        self.lock = lock
        self.send_buffer = ""
        self.password_count = 0
        self.nervous_count = 0

        self.player = player.Player()

    def custom_decode(self, data):
        return str(data)[2:len(str(data)) - 1]

    def run(self):
        #  import telnetlib

        #  _.send_instruction(self, telnetlib.IAC + telnetlib.WILL + telnetlib.ECHO)
        self.lock.acquire()
        _.peers.append(self)
        self.lock.release()
        print("Connected ", self.ADDRESS)
        _.send_to_char(self, _.LOGIN_MESSAGE, False, True)

        # main loop
        while self.state is not _.STATE_QUIT:
            try:
                data=self.SOCKET.recv(1024)
            except TimeoutError:
                print("Connection timed out.")
                continue
            except (ConnectionResetError, ConnectionAbortedError):
                print("Connection failed.")
                self.state = _.STATE_QUIT  # -Rework- to include linkdead
                continue
            self.linkdead = False
            if not data:
                break
            decodedMessage = self.custom_decode(data)

            # hack for now: if command starts with a \, simply ignore it
            if decodedMessage[0:2] == '\\x':
                continue

            # Check to see if it ends in a newline
            if len(decodedMessage) >= 2:
                if decodedMessage[len(decodedMessage) - 4:] == '\\r\\n' \
                    or decodedMessage[len(decodedMessage) - 2:] == '\\n':
                    self.input_buffer += decodedMessage[:len(decodedMessage) - 4] if \
                        decodedMessage[len(decodedMessage) - 4:] == '\\r\\n' else \
                        decodedMessage[:len(decodedMessage) - 2]
                    # After a newline is received, input_string_buffer is the command sent by the peer if it's not empty
                    if len(self.input_buffer) > 0:
                        # Check state to handle login input_string
                        if self.state == _.STATE_NAME1:
                            admin.parse_name1(self, self.input_buffer)
                        elif self.state == _.STATE_NAME2:
                            admin.parse_name2(self, self.input_buffer)
                        elif self.state == _.STATE_PASSWORD:
                            admin.parse_password(self, self.input_buffer)
                        elif self.state == _.STATE_NEW_PASSWORD1:
                            admin.parse_new_password1(self, self.input_buffer)
                        elif self.state == _.STATE_NEW_PASSWORD2:
                            admin.parse_new_password2(self, self.input_buffer)
                        elif self.state == _.STATE_RACE:
                            admin.parse_race(self, self.input_buffer)
                        elif self.state == _.STATE_CLASS:
                            admin.parse_class(self, self.input_buffer)
                        elif self.state == _.STATE_ONLINE:
                            if len(self.command_buf) == 0 and self.player.lag == 0:
                                if admin.parse_command(self, self.input_buffer): # returns true if not found
                                    _.send_to_char(self,"Huh?\n\r")
                            else:
                                self.command_buf.append(self.input_buffer)
                    self.input_buffer = ""
                else:
                    self.input_buffer += decodedMessage
            else:
                self.input_buffer += decodedMessage
        quit()

    def quit(self):
        self.state = _.STATE_QUIT
        self.SOCKET.close()
        print("Disconnected ", self.ADDRESS)
        try:
            _.mobiles.remove(self.player)
        except ValueError:
            print("Player disconnected before being added to mobiles list")
        self.lock.acquire()
        _.peers.remove(self)
        self.lock.release()