__author__ = 'ohell_000'


import socket
import threading
import start
import peer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', 51234))
s.listen(4)

lock = threading.Lock()

start.start_game()

while True:
    temp_socket, temp_address = s.accept()
    peer.Peer(temp_socket, temp_address, lock).start()

s.close


def start_game():
    print("Loading mobiles...")
    mobile.initialize_mobiles()
    print("Loading areas...")
    area.initialize_area()
    print("Loading items...")
    item.initialize_items()
    print("Loading races...")
    races.initialize_races()
    print("Loading classes...")
    classes.initialize_classes()
    print("Initializing commands...")
    commands.initialize_commands()
    print("Initializing skills...")
    skills.initialize_skills()
    print("Initializing spells...")
    spells.initialize_spells()
    print("Initializing affects...")
    affects.initialize_affects()
    print("Seeding random...")
    random.seed()
    #  Sort dictionaries
    _.race_list = sorted(r.get_name() for r in _.races)
    _.class_list = sorted(c.get_name() for c in _.classes)
    #  Initialize combat loop
    update.UpdateLoop().start()

    for r in _.rooms:  # -Debug-
        temp_item = item.Item("", "", "", "", "")
        temp_item = copy.deepcopy(random.choice(_.items))
        r.add_item(temp_item)