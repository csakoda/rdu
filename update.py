__author__ = 'ohell_000'


import globals as _
import threading
import combat
import time


def do_update():
    from admin import parse_command
    for c in _.peers:
        #  Handle command lag and the command buffer
        if c.player.lag > 0:
            c.player.lag = max(c.player.lag - 0.25, 0)
        elif len(c.command_buf) > 0:
            parse_command(c, c.command_buf[0])
            c.command_buf.pop(0)
        #  Slowly time out linkdead players -- NOT IMPLEMENTED
        # if c.linkdead:
        #     if c.linkdead_count <= 0:
        #         c.state == _.STATE_QUIT
        #     else:
        #         c.linkdead_count -= 1
        #  Tick down nervous
        if c.nervous_count > 0:
            c.nervous_count -= 0.25
            if c.nervous_count <= 0:
                _.send_to_char(c, "You are no longer nervous.\n\r")

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
            a.resetTimer = 60
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