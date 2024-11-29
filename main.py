import os
import readline

#dir suggestion function
def file_completer(text, state):
    path = os.getcwd()
    suggestions = [
        name + ("/" if os.path.isdir(os.path.join(path, name)) else "")
        for name in os.listdir(path)
        if name.startswith(text)
    ]
    return suggestions[state] if state < len(suggestions) else None

# setting readline to execute file_copleter fun on tab
readline.set_completer(file_completer)
readline.parse_and_bind("tab: complete")


def file_completer(text, state):
    paths = os.environ["PATH"].split(":")
    executables = set()

    for path in paths:
        if os.path.exists(path):
            executables.update(
                name for name in os.listdir(path)
                if os.access(os.path.join(path, name), os.X_OK) and name.startswith(text)
            )

    suggestions = sorted(executables)
    return suggestions[state] if state < len(suggestions) else None

readline.set_completer(file_completer)
readline.parse_and_bind("tab: complete")



user = os.popen("echo $USER").read().strip()
hostname = os.popen("cat /etc/hostname").read().strip()

while True:
    path = os.getcwd()
    command = input(f"{user} on {hostname} λ {path} ")
    if command == "exit":
        break
    if command.startswith("cd "):
        new_path = command[3:].strip()
        if new_path == "":
            os.chdir(f"/home/{user}/")
        else:
            os.chdir(os.path.abspath(new_path))

    elif command == "listdir":
        print(os.listdir())
    else:
        os.system(command)

