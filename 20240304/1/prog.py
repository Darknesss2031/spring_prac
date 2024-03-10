import cowsay
import sys
from io import StringIO
import shlex

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

jgsbat = cowsay.read_dot_cow(StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""))

player = Player(0, 0)
custom_cows = {}
custom_cows['jgsbat'] = jgsbat

def encounter(x, y):
    if monsters[(x, y)][1] in custom_cows.keys():
        print(cowsay.cowsay(monsters[(x, y)][0], cowfile=custom_cows[monsters[(x, y)][1]]))
        return
    print(cowsay.cowsay(*monsters[(x, y)]))
print("<<< Welcome to Python-MUD 0.1 >>>")

while True:
    inp = ''
    try:
        inp = input('> ')
    except: pass
    if not inp: break

    command = shlex.split(inp)
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
                name = command[1]
            except:
                print('Invalid arguments')
                continue

            if name not in cowsay.list_cows():
                print('Invalid arguments')
                continue

            point = 2
            hp = 0
            hello = ''
            coords = [0, 0]
            popularity = [0] * 3
            invalidArgs = False

            if 'hello' not in command or 'hp' not in command or 'coords' not in command:
                print('Invalid arguments')
                continue

            while point < len(command):
                if command[point] == 'hp':
                    popularity[0] += 1
                    point += 1
                    try:
                        hp = int(command[point])
                    except:
                        invalidArgs = True
                        break
                elif command[point] == 'hello':
                    popularity[1] += 1
                    point += 1
                    try:
                        hello = command[point]
                    except:
                        invalidArgs = True
                        break
                elif command[point] == 'coords':
                    popularity[2] += 1
                    point += 1
                    try:
                        coords = [int(command[point]), int(command[point + 1])]
                    except:
                        invalidArgs = True
                        break
                    point += 1
                point += 1
            if invalidArgs or 0 in popularity:
                print('Invalid arguments')
                continue
        case _:
            print('Invalid command')
