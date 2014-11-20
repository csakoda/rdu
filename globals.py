__author__ = 'ohell_000'


VERSION = 0
START_ROOM = "5700"

ENCODING_TYPE = "utf-8"

SEPARATOR = ":^:"

DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3
DIR_UP = 4
DIR_DOWN = 5

# Game states
STATE_ONLINE = 0
STATE_QUIT = 1
STATE_LOGIN = 2

# Login states
LOGIN_NAME1 = 0
LOGIN_NAME2 = 1
LOGIN_RACE = 4
LOGIN_CLASS = 5
LOGIN_PASSWORD = 8
LOGIN_LIST_CHARS = 13
LOGIN_ACCOUNT1 = 9
LOGIN_ACCOUNT2 = 10
LOGIN_NEW_PASSWORD1 = 11
LOGIN_NEW_PASSWORD2 = 12

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
Enter your account name: "


def send_to_room(message, room, named=[]):
    for c in peers:
        if c.account.player.get_room() == room:
            c.peer_send(message, True, False, named)


def send_to_area_except(message, area, exceptions):
    for c in peers:
        if c.account.player.get_area() == area and c not in exceptions:
            c.peer_send(message)


def send_to_room_except(message, room, exceptions, named=[]):
    for c in peers:
        if c.account.player.get_room() == room and c not in exceptions:
            c.peer_send(message, True, False, named)


def send_to_all(message):
    for c in peers:
        c.peer_send(message)


def send_to_all_except(message, exceptions):
    for c in peers:
        if c not in exceptions:
            c.peer_send(message)





def send_buf_to_char(peer, prompt=True):
    peer.peer_send(peer.send_buffer, prompt)


def send_instruction(peer, message):
    peer.SOCKET.send(message)


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

def strip_load_line(input_string):
    return input_string.strip().split(SEPARATOR)