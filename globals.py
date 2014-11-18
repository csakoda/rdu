__author__ = 'ohell_000'


VERSION = 0
START_ROOM = "5700"

ENCODING_TYPE = "utf-8"

DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3
DIR_UP = 4
DIR_DOWN = 5

STATE_NAME1 = 0
STATE_NAME2 = 1
STATE_NEW_PASSWORD1 = 2
STATE_NEW_PASSWORD2 = 3
STATE_RACE = 4
STATE_CLASS = 5
STATE_ONLINE = 6
STATE_QUIT = 7
STATE_PASSWORD = 8

MAX_PASSWORDS = 3

WEAPON_SWORD = 0
WEAPON_AXE = 1
WEAPON_SPEAR = 2
WEAPON_DAGGER = 3
WEAPON_MACE = 4

WEAR_ARMS = 0
WEAR_BODY = 1
WEAR_FEET = 2
WEAR_FINGER = 3
WEAR_HAND = 4
WEAR_HEAD = 5
WEAR_LEGS = 6
WEAR_NECK = 7
WEAR_OFFHAND = 8
WEAR_TORSO = 9
WEAR_WAIST = 10
WEAR_WRIST = 11
WEAR_FLOAT = 12
WEAR_HELD = 13
WEAR_LIGHT = 14
WEAR_WEAPON = 15

WEAR_NECK2 = 16
WEAR_WRIST2 = 17
WEAR_FINGER2 = 18
WEAR_FLOAT2 = 19

POS_SLEEPING = 0
POS_RESTING = 1
POS_STANDING = 2
POS_FIGHTING = 3

LINKDEAD_TIMER = 4
NERVOUS_TIMER = 4

TARGET_SELF_ONLY = 0
TARGET_PREFER_SELF = 1
TARGET_PREFER_FIGHTING = 2
TARGET_TARGET_ONLY = 3
TARGET_IGNORE = 4
TARGET_TARGET_ANYWHERE = 5

MAX_CARRY = 5

class_list = ["cleric", "mage", "thief", "warrior", "runist"]

race_list = ["human", "elf", "giant", "dwarf", "troll"]

command_list = {}
command_list_sorted = []
skill_list = {}
skill_list_sorted = []
spell_list = {}
spell_list_sorted = []
affect_list = {}
affect_list_sorted = []

peers = []
mobiles = []

master_mobile_list = []

block_send = False

races = []
classes = []
areas = []
rooms = []
items = []

VALID_CHARS = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!/:;'%%{}\"[],+=@#$^&*<>"

LOGIN_MESSAGE = "REDEMPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDE\n\r\
MPTIONREDEMPTIONREDEMPTIONRE           PTIONREDEMPTIONREDEMPTION\n\r\
REDEMPTIONREDEMPTIONREDE       @@@@@        TIONREDEMPTIONREDEMP\n\r\
NIONREDEMPTIONREDEMPT                        ONTIONREDEMPTIONRED\n\r\
EMPTIONREDEMPTIONRE         @@@ @@@  @@        EPTIONREDEMPTIONR\n\r\
EDEMPTIONREDEMPTIO         @@@ @@@@@  @@        EDEMPTIONREDEMPT\n\r\
IONREDEMPTIONREDE         @@@ @@@@@@ @@@        IONREDEMPTIONRED\n\r\
EMPTIONREDEMPTIO          @@@ @@@@@@ @@@         EDEMPTIONREDEMP\n\r\
TIONREDEMPTIONR           @@@@ @@@@ @@@@          MPTIONREDEMPTI\n\r\
ONREDEMPTIONREDE        ^ @@@@@@@@@@@@@@  ^      MTIONREDEMPTION\n\r\
NTIONREDEMTIONRE        ^^ @@@@@@@@@@@@ ^ ^^ ^   MPTIONREDEMPTIO\n\r\
REDEMEPTIONREDEMP     ^^ ^^ @@@@@@@@@@ ^^ ^     IONREDEMPTIONRED\n\r\
REDEMPTIONREDEMPT    ^ ^^ ^ @@@@@@@@@ ^^ ^      NREDEMPTIONREDEM\n\r\
EMPTIONREDEMPTIONR     ^^ ^ @@@@@@@@@ ^^       PTIONREDEMTIONRED\n\r\
NREDEIPTIONREDEMPTI    ^^^^ @@@@@@@@@ ^^^^    TIONREDEMPTIONREDE\n\r\
MPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDEMPTI\n\r\
EMPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDEMPTIONREDEMPT\n\r\n\r\
By what name do you wish to be known? "


def send_to_room(message, room, named=[]):
    for c in peers:
        if c.player.get_room() == room:
            send_to_char(c, message, True, False, named)


def send_to_area_except(message, area, exceptions):
    for c in peers:
        if c.player.get_area() == area and c not in exceptions:
            send_to_char(c, message)


def send_to_room_except(message, room, exceptions, named=[]):
    for c in peers:
        if c.player.get_room() == room and c not in exceptions:
            send_to_char(c, message, True, False, named)


def send_to_all(message):
    for c in peers:
        send_to_char(c, message)


def send_to_all_except(message, exceptions):
    for c in peers:
        if c not in exceptions:
            send_to_char(c, message)


def send_to_buf(char, message):
    if char not in peers:
        return
    char.send_buffer += message


def send_buf_to_char(char, prompt=True):
    send_to_char(char, char.send_buffer, prompt)


def send_instruction(char, message):
    char.SOCKET.send(message)


def send_to_char(char, message, prompt=True, override=False, named=[]):
    # if char.online
    if char is None:
        return
    if char.state is not STATE_ONLINE and not override:
        return
    if char not in peers:
        return

    if len(named) > 0:
        message = message % tuple([n.get_name(char.player) for n in named])

    message = message[0].capitalize() + message[1:]
    
    if block_send:
        send_to_buf(char, message)
    elif not char.linkdead:
        if char.state == STATE_ONLINE and prompt:
            message += "\n\r" + char.player.get_prompt()
            #  Color stuff
            message = message.replace("{{", "{~")
            if char.player.get_color() == 1:
                message = message.replace("{x", "\033[0;37m")
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
            char.SOCKET.send(bytes(message, ENCODING_TYPE))
        except IOError as e:
            print(e)


def get_dir_string(direction):
    dir_string = ""

    if direction == DIR_NORTH:
        dir_string = "north"
    elif direction == DIR_EAST:
        dir_string = "east"
    elif direction == DIR_SOUTH:
        dir_string = "south"
    elif direction == DIR_WEST:
        dir_string = "west"
    elif direction == DIR_UP:
        dir_string = "up"
    elif direction == DIR_DOWN:
        dir_string = "down"

    return dir_string

def get_dir_constant(dir_string):
    if len(dir_string) == 0:
        return None
    dir_string = dir_string.lower()
    if dir_string[0] == 'n':
        return DIR_NORTH
    elif dir_string[0] == 'e':
        return DIR_EAST
    elif dir_string[0] == 's':
        return DIR_SOUTH
    elif dir_string[0] == 'w':
        return DIR_WEST
    elif dir_string[0] == 'u':
        return DIR_UP
    elif dir_string[0] == 'd':
        return DIR_DOWN
    return None
    
        