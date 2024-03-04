import shlex

# while True:
#     s = input()
#     res = shlex.split(s)
#     print(res)

# inp = input()
# print(shlex.join(shlex.split(inp)))

fio = input()
place = input()
print(shlex.join(['register', fio, place]))