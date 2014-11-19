__author__ = 'ohell_000'


import globals as _
import player
import login
import threading
import account

class Peer(threading.Thread):
    def __init__(self, socket, address, lock):
        threading.Thread.__init__(self)
        self.game_state = _.STATE_LOGIN
        self.login_state = _.LOGIN_ACCOUNT1
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

        self.account = account.Account()
        self.block_send = False

    def custom_decode(self, data):
        return str(data)[2:len(str(data)) - 1]

    def run(self):
        #  import telnetlib
        from update import parse_command

        #  _.send_instruction(self, telnetlib.IAC + telnetlib.WILL + telnetlib.ECHO)
        self.lock.acquire()
        _.peers.append(self)
        self.lock.release()
        print("Connected ", self.ADDRESS)
        self.peer_send(_.LOGIN_MESSAGE, False, True)

        # main loop
        while self.game_state is not _.STATE_QUIT:
            try:
                data=self.SOCKET.recv(1024)
            except TimeoutError:
                print("Connection timed out.")
                continue
            except (ConnectionResetError, ConnectionAbortedError):
                print("Connection failed.")
                self.game_state = _.STATE_QUIT  # -Rework- to include linkdead
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
                        if self.game_state == _.STATE_ONLINE:
                            if len(self.command_buf) == 0 and self.account.player.lag == 0:
                                if parse_command(self, self.input_buffer): # returns true if not found
                                    self.peer_send("Huh?\n\r")
                            else:
                                self.command_buf.append(self.input_buffer)
                        elif self.game_state == _.STATE_LOGIN:
                            login.handle_login(self, self.input_buffer)
                    self.input_buffer = ""
                else:
                    self.input_buffer += decodedMessage
            else:
                self.input_buffer += decodedMessage
        quit()

    def quit(self):
        self.game_state = _.STATE_QUIT
        self.SOCKET.close()
        print("Disconnected ", self.ADDRESS)
        try:
            _.mobiles.remove(self.account.player)
        except ValueError:
            print("Player disconnected before being added to mobiles list")
        self.lock.acquire()
        _.peers.remove(self)
        self.lock.release()

    def peer_send(self, message, prompt=True, override=False, named=[]):
        if len(named) > 0:
            message = message % tuple([n.get_name(self.account.player) for n in named])

        message = message[0].capitalize() + message[1:]

        if self.block_send:
            self.send_to_buf(self, message)
        elif not self.linkdead:
            if self.game_state == _.STATE_ONLINE and prompt:
                message += "\n\r" + self.account.player.get_prompt()
                #  Color stuff
                message = message.replace("{{", "{~")
                if self.account.player.get_color() == 1:
                    message = message.replace("{x", "\033[0;39m")
                    message = message.replace("{r", "\033[0;31m")
                    message = message.replace("{b", "\033[0;34m")
                    message = message.replace("{g", "\033[0;32m")
                    message = message.replace("{c", "\033[0;36m")
                    message = message.replace("{m", "\033[0;35m")
                    message = message.replace("{y", "\033[0;33m")
                    message = message.replace("{w", "\033[0;37m")

                    message = message.replace("{d", "\033[1;30m")
                    message = message.replace("{D", "\033[1;30m")
                    message = message.replace("{R", "\033[1;31m")
                    message = message.replace("{B", "\033[1;34m")
                    message = message.replace("{G", "\033[1;32m")
                    message = message.replace("{C", "\033[1;36m")
                    message = message.replace("{M", "\033[1;35m")
                    message = message.replace("{Y", "\033[1;33m")
                    message = message.replace("{W", "\033[1;37m")
                else:
                    message = message.replace("{x", "")
                    message = message.replace("{r", "")
                    message = message.replace("{b", "")
                    message = message.replace("{g", "")
                    message = message.replace("{c", "")
                    message = message.replace("{m", "")
                    message = message.replace("{y", "")
                    message = message.replace("{w", "")

                    message = message.replace("{d", "")
                    message = message.replace("{D", "")
                    message = message.replace("{R", "")
                    message = message.replace("{B", "")
                    message = message.replace("{G", "")
                    message = message.replace("{C", "")
                    message = message.replace("{M", "")
                    message = message.replace("{Y", "")
                    message = message.replace("{W", "")
                message = message.replace("{~", "{")
                #  end color stuff
            # noinspection PyArgumentList
            try:
                self.SOCKET.send(bytes(message, _.ENCODING_TYPE))
            except IOError as e:
                print(e)

    def send_to_buf(self, message):
        self.peer.send_buffer += message


# TEMPORARY STATIC FUNCTIONS

