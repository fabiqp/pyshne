import os
import readline
import configparser
from colorama import Fore, Style, init

# Checking if config file exist
config_path = os.path.expanduser("~/.config/pyshne/pyshne.conf")

if os.path.exists(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    theme = config['theme']['theme']
    symbol = config['theme']['symbol']
    user_color = config['colors']['username_color']
    hostname_color = config['colors']['hostname_color']
    symbol_color = config['colors']['symbol_color']

else:
    os.makedirs(os.path.expanduser("~/.config/pyshne"), exist_ok=True)
    
    with open(config_path, 'w') as config_file:
        config_file.write("[theme]\ntheme = default\nsymbol=λ\n")
    
    print(f"Config file has been created on {config_path}")

#parsing theme from config to color
color_map = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "black": Fore.BLACK,
    "default": Fore.RESET
}

selected_theme = color_map.get(theme)
selected_user_color = color_map.get(user_color)
selected_hostname_color = color_map.get(hostname_color)
selected_symbol_color = color_map.get(symbol_color)
def file_completer(text, state):
    path = os.getcwd()
    suggestions = [
        name + ("/" if os.path.isdir(os.path.join(path, name)) else "")
        for name in os.listdir(path)
        if name.startswith(text)
    ]
    return suggestions[state] if state < len(suggestions) else None


def executable_completer(text, state):
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


def combined_completer(text, state):
    local_suggestion = file_completer(text, state)
    if local_suggestion is not None:
        return local_suggestion

    return executable_completer(text, state)

readline.set_completer(combined_completer)
readline.parse_and_bind("tab: complete")

user = os.popen("echo $USER").read().strip()
hostname = os.popen("cat /etc/hostname").read().strip()

while True:
    selected_theme = color_map.get(theme)
    path = os.getcwd()
    command = input(
        
        f"{selected_user_color}{user}{Style.RESET_ALL} {selected_theme}on " +
        f"{selected_hostname_color}{hostname}{Style.RESET_ALL} " +
        f"{selected_symbol_color}{symbol}{Style.RESET_ALL} {selected_theme}{path} ")

    if command == "exit":
        break
    elif command.startswith("cd"):
        new_path = command[3:].strip()
        if new_path == "":
            os.chdir(f"/home/{user}/")
        else:
            try:
                os.chdir(os.path.abspath(new_path))
            except FileNotFoundError:
                print(f"No such directory: {new_path}")
            except NotADirectoryError:
                print(f"Not a directory: {new_path}")
    elif command == "help":
       print("some cutom pyshne commands")
    elif command == "listdir":
        print(os.listdir())
    elif command.startswith("color"):
        if command == "color --help" or command == "color":
            print(f"{selected_theme}color command is used to change text color on this session")
            print(f"{selected_theme}colors: red, green, blue, yellow, magenta, cyan, white, default")
        else:
            theme = command[6:]


    else:
        os.system(command)

