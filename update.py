__author__ = 'ohell_000'


import globals as _
import threading
import combat
import time


def do_update():
    for p in _.peers:
        #  Handle command lag and the command buffer
        if p.account.player.lag > 0:
            p.account.player.lag = max(p.account.player.lag - 0.25, 0)
        elif len(p.command_buf) > 0:
            parse_command(p, p.command_buf[0])
            p.command_buf.pop(0)
        #  Slowly time out linkdead players -- NOT IMPLEMENTED
        # if p.linkdead:
        #     if p.linkdead_count <= 0:
        #         p.game_state == _.STATE_QUIT
        #     else:
        #         p.linkdead_count -= 1
        #  Tick down nervous
        if p.nervous_count > 0:
            p.nervous_count -= 0.25
            if p.nervous_count <= 0:
                p.peer_send("You are no longer nervous.\n\r")

    #  Update and remove affects
    for m in _.mobiles:
        if len(m.affects) == 0:
            continue
        for a in m.affects:
            if a.duration == 0:
                a.remove_affect()
            else:
                a.duration -= 0.25

    for a in _.areas:
        a.resetTimer -= 0.25
        if a.resetTimer <= 0:
            a.resetTimer = 360
            a.reset()


class UpdateLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        i = 0
        while True:
            #  Do an update round every quarter of a second
            do_update()
            #  Do a combat round every three seconds
            if i == 12:
                combat.do_full_round()
                i = 0
            else:
                i += 1
            time.sleep(0.25)


def parse_command(peer, input_string):
    if input_string != ''.join(p for p in input_string if p in _.VALID_CHARS):
        return True
    command = input_string.split()
    if len(command) > 0:
        command = command[0]
    args = input_string[len(command) + 1:]
    for p in _.command_list_sorted:
        #  First check commands
        if len(p) >= len(command):
            if command == p[:len(command)]:
                _.command_list[p].execute_command(peer, args)
                break
    else:
        #  Then check skills
        for s in _.skill_list_sorted:
            if s not in peer.account.player.get_skills():
                continue
            if len(s) >= len(command):
                if command == s[:len(command)]:
                    _.skill_list[s].execute_skill(peer, args)
                    break
        else:
            return True  #  command not found