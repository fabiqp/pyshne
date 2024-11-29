import os

user = os.popen("echo $USER").read().strip()
hostname = os.popen("cat /etc/hostname").read().strip()

while True:
    path = os.getcwd()
    command = input(f"{user} on {hostname} λ {path} ")
    if command == "exit":
        break
    if command.startswith("cd "):
        if command == "cd":
            os.chdir(f"/home/{user}/")
        os.chdir(f"{path}/{command[3:]}")
    else:
        os.system(command)

