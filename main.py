import os

user = os.popen("echo $USER").read().strip()

while True:
    command = input(f"{user} λ ")
    if command == "exit":
        break
    os.system(command)

