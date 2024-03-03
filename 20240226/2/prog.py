import cowsay
import sys

# class Monster:
#     def __init__(self, x, y, greet):
#         self.x = x
#         self.y = y
#         self.greet = greet


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def up(self): self.y = (self.y - 1) % 10
    def down(self): self.y = (self.y + 1) % 10
    def left(self): self.x = (self.x - 1) % 10
    def right(self): self.x = (self.x + 1) % 10

    def getPos(self): return (self.x, self.y)


monsters = {}
def encounter(x, y):
    print(cowsay.cowsay(monsters[(x, y)]))

player = Player(0, 0)

while True:
    inp = ''
    try:
        inp = input('> ')
    except: pass
    if not inp: break

    command = inp.split()
    match command[0]:
        case 'up':
            player.up()
            coords = player.getPos()
            print('Moved to', coords)
            if coords in monsters.keys():
                encounter(*coords)
        case 'down':
            player.down()
            coords = player.getPos()
            print('Moved to', coords)
            if coords in monsters.keys():
                encounter(*coords)
        case 'left':
            player.left()
            coords = player.getPos()
            print('Moved to', coords)
            if coords in monsters.keys():
                encounter(*coords)
        case 'right':
            player.right()
            coords = player.getPos()
            print('Moved to', coords)
            if coords in monsters.keys():
                encounter(*coords)
        case 'addmon':
            try:
                command[3] = int(command[1])
                command[2] = int(command[2])
            except:
                print('Invalid arguments')
                continue
            if command[3] < 0 or command[3] > 9 or command[2] < 0 or command[2] > 9 or len(command) != 5 or command[1] not in cowsay.list_cows(): print('Invalid arguments')
            else:
                existed = False
                if (command[2], command[3]) in monsters.keys(): existed = True
                monsters[(command[2], command[3])] = command[4]
                print('Added monster', command[1], 'to', str((command[2], command[3])), 'saying', command[4])
                if existed: print('Replaced the old monster')
        case _:
            print('Invalid command')
