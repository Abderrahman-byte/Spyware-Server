import sys

from .commands import commands_list

def print_help () :
    print("spyware_server_scripts [command] [cmd-arg]")
    print("[*] Commands : ")
    for command in commands_list :
        print(f"\t {command.name} - {command.description}")

def run_command (name, *args) :
    for command in commands_list :
        if command.name == name :
            command.run(*args)
            return
    
    print(f"[ERROR] command {name} not found !")
    print_help()

def main () :
    if len(sys.argv) <= 1:
        return print_help()

    command_name = sys.argv[1]
    args = sys.argv[2:]
    run_command(command_name, *args)

if __name__ == '__main__' :
    main()