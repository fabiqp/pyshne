import os

user = os.popen("echo $USER").read().strip()
hostname = os.popen("cat /etc/hostname").read().strip()

while True:
    command = input(f"{user} on {hostname} λ ")
    if command == "exit":
        break
    os.system(command)

