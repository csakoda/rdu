__author__ = 'ohell_000'


import player


class Account():
    def __init__(self):
        self.player = player.Player()
        self.peer = None

        self.players = []
        self.gold = 0

        self.name = ""
        self.password = "test123"

    def set_gold(self, amount):
        self.gold = max(0, amount)

    def save(self):
        import os
        if not os.path.exists('accounts'):
            os.makedirs('accounts')
        f = open("accounts/" + self.name + ".dat","w")
        f.write("password:^:%s\n" % self.password)
        f.write("gold:^:(*int)%i\n" % self.gold)
        f.write("players:^:%s\n" % " ".join(self.players))
        f.close()

    def load(self, name):
        from globals import strip_load_line

        try:
            f = open("accounts/" + name + ".dat", "r")
            print("Account %s found." % name)
            lines = f.readlines()
            for l in lines:
                l = strip_load_line(l)
                if l[0] == "password":
                    self.password = l[1]
                elif l[0] == "players":
                    for p in l[1].split(" "):
                        self.players.append(p)
                elif l[0] == "gold":
                    self.gold = int(l[1][6:])
        except FileNotFoundError:
            print("Account not found.")
            return False
        f.close()
        return True