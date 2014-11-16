__author__ = 'ohell_000'


import socket
import threading
import admin
import peer


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('localhost', 51234))
s.listen(4)

lock = threading.Lock()

admin.start_game()

while True:
    temp_socket, temp_address = s.accept()
    peer.Peer(temp_socket, temp_address, lock).start()