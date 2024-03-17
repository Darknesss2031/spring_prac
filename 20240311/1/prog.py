import cmd
import cowsay
from io import StringIO
import shlex


class Monster:
    def __init__(self, name, hp, greet):
        self.name = name
        self.hp = hp
        self.hello = greet

    def attackFor(self, damage):
        givenDamage = min(damage, self.hp)
        self.hp = max(0, self.hp - damage)
        return self.hp, givenDamage


class Player:
    weapons = {
        'sword': 10,
        'spear': 15,
        'axe': 20
    }

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

custom_cows = {}
custom_cows['jgsbat'] = jgsbat

available_cows = cowsay.list_cows() + list(custom_cows.keys())

player = Player(0, 0)


def encounter(x, y):
    monster = monsters[(x, y)]
    name = monster.name
    hello = monster.hello
    if name in custom_cows.keys():
        print(cowsay.cowsay(hello, cowfile=custom_cows[name]))
        return
    print(cowsay.cowsay(hello, name))


print("<<< Welcome to Python-MUD 0.1 >>>")


class cmdLine(cmd.Cmd):
    prompt = '> '

    def do_up(self, _):
        player.up()
        coords = player.getPos()
        print('Moved to', coords)
        if coords in monsters.keys():
            encounter(*coords)

    def do_down(self, _):
        player.down()
        coords = player.getPos()
        print('Moved to', coords)
        if coords in monsters.keys():
            encounter(*coords)

    def do_left(self, _):
        player.left()
        coords = player.getPos()
        print('Moved to', coords)
        if coords in monsters.keys():
            encounter(*coords)

    def do_right(self, _):
        player.right()
        coords = player.getPos()
        print('Moved to', coords)
        if coords in monsters.keys():
            encounter(*coords)

    def do_addmon(self, args):
        command = shlex.split(args)
        try:
            name = command[0]
        except:
            print('Invalid arguments')
            return

        if name not in cowsay.list_cows() and name not in custom_cows.keys():
            print('Invalid arguments')
            return

        point = 1
        hp = 0
        hello = ''
        coords = [0, 0]
        popularity = [0] * 3
        invalidArgs = False

        if 'hello' not in command or 'hp' not in command or 'coords' not in command:
            print('Invalid arguments')
            return

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
            return
        x = coords[0]
        y = coords[1]

        if x < 0 or x > 9 or y < 0 or y > 9 or len(command) != 8:
            print('Invalid arguments')
            return

        existed = False
        if (x, y) in monsters.keys(): existed = True
        monsters[(x, y)] = Monster(name, hp, hello)
        print('Added monster', name, 'with', hp, 'hp to', str((x, y)), 'saying', hello)
        if existed: print('Replaced the old monster')

    def do_attack(self, params):
        coords = player.getPos()
        weapon = 'sword'

        args = shlex.split(params)

        if len(args) < 1 or args[0] not in available_cows:
            print("Invalid monster name")
            return

        name = args[0]

        if coords not in monsters.keys() or monsters[coords].name != name:
            print(f"No {name} here")
            return

        if len(args) > 1 and args[1] == 'with':
            if len(args) < 3 or args[2] not in player.weapons.keys():
                print("Unknown weapon")
                return
            weapon = args[2]

        damage = player.weapons[weapon]

        hp, givenDamage = monsters[coords].attackFor(damage)
        print(f"Attacked {monsters[coords].name}, damage {givenDamage} hp")

        if hp:
            print(f"{monsters[coords].name} now has {hp} hp")
        else:
            print(monsters[coords].name, 'died')
            monsters.pop(coords)

    def complete_attack(self, text, line, begidx, endidx):
        args = shlex.split(line)
        if len(args) == 1:
            return available_cows
        if len(args) == 2 and args[1] not in available_cows:
            return [c for c in available_cows if c.startswith(text)]
        elif len(args) == 2 and line[line.find(args[1][0]):].count(' ') > 0:
            return ['with']
        elif len(args) == 3 and 'with'.startswith(text) and text:
            return ['with']
        elif len(args) == 3 and not 'with'.startswith(text): return []
        elif len(args) == 3 and args[2] == 'with' and line[line.rfind('h'):].count(' ') > 0:
            return [c for c in player.weapons.keys()]
        elif len(args) == 4 and text:
            return [c for c in player.weapons.keys() if c.startswith(text)]
        return []


if __name__ == "__main__":
    cmdLine().cmdloop()