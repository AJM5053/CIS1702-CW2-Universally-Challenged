import json

# Programming 1 - CW2 Group Project:
# Text-Based Adventure Game Engine

def update_save_file(save_file_dict,save_file_num):
    file_name="save_file_"+save_file_num+".json"
    with open(file_name, "w") as write_file:
        json.dump(save_file_dict, write_file,indent=4)
    write_file.close()

# The player current health in the chosen save file is reset to the max health
def reset_player_health(save_file_num):
    file_name="save_file_"+save_file_num+".json"
    with open("player.json", "r") as f:
        player_data = json.load(f)
    max_health = player_data["player"]["max_health"]
    with open(file_name, "r") as f:
        save_data = json.load(f)
    save_data["save_file"]["player"]["current_health"] = max_health
    with open(file_name, "w") as f:
        json.dump(save_data, f, indent=4)

def read_save_file(save_file_num):
    file_name="save_file_"+save_file_num+".json"
    with open(file_name, mode="r") as read_file:   
        save_file_dict = json.load(read_file)
    read_file.close
    return(save_file_dict)

def read_default_save_file():
    with open("default_save_file.json", mode="r") as read_file:   
       default_save_file_dict = json.load(read_file)
    read_file.close
    return(default_save_file_dict)

def read_game_map():
    with open("game_map.json", mode="r") as read_file:   
        game_map_dict = json.load(read_file)
    read_file.close
    return(game_map_dict)

def read_items():
    with open("items.json", mode="r") as read_file:   
        items_dict = json.load(read_file)
    read_file.close
    return(items_dict)

def read_player():
    with open("player.json", mode="r") as read_file:   
        player_dict = json.load(read_file)
    read_file.close
    return(player_dict)

def read_npcs():
    with open("npcs.json", mode="r") as read_file:   
        npcs_dict = json.load(read_file)
    read_file.close
    return(npcs_dict)

def __init__():
    # This is a list of valid commands
    verb_commands=["go","drop","pickup","quit","help","view"]
    noun_commands=["north","east","south","west"]
    exit,save_file_num=start_menu()
    save_file_dict=read_save_file(save_file_num)
    game_map_dict=read_game_map()
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    reset_player_health(save_file_num)
    return(verb_commands,noun_commands,exit,save_file_num)

def overwrite_saved(save_file_num):
    default_save_file_dict=read_default_save_file()
    default_save_file_dict["save_file"]=default_save_file_dict.pop("default_save_file")
    update_save_file(default_save_file_dict,save_file_num)

def saved_choice(option):
    print(f"Select saved game to {option}")
    save_file_1_dict=read_save_file("1")
    print(f"1 - {save_file_1_dict["save_file"]["player"]["current_room"]}")
    save_file_2_dict=read_save_file("2")
    print(f"2 - {save_file_2_dict["save_file"]["player"]["current_room"]}")
    save_file_3_dict=read_save_file("3")
    print(f"3 - {save_file_3_dict["save_file"]["player"]["current_room"]}")
    save_file_num="0"
    while ord(save_file_num)<49 or ord(save_file_num)>51: 
        # This keeps asking the user for an input until it is valid. The ord value gets the ascii value. 49 in ascii is "1" and 51 in ascii is "3"
        save_file_num=input()
        if save_file_num=="":
            print("Please enter valid option")
            save_file_num="0"
    if option=="overwrite":
        overwrite_saved(save_file_num)
    return(save_file_num)
    
def action(separated,exit,save_file_num):
    function_name=separated[0] # String of function name
    function=globals()[function_name] # Globals returns dictionary of global variables including functions
    exit=function(separated,exit,save_file_num)
    return(exit)

def room_decision(exit,choice,verb_commands,noun_commands,save_file_num):
    valid,separated=parse_validate_input(verb_commands,noun_commands,choice,save_file_num)
    if valid:
        exit=action(separated,exit,save_file_num)
    else:
        print("Invalid command try again")
        print()
    return(exit)

def start_menu(): # Sets what room the player first starts off in when opening the game
    game_map_dict=read_game_map()
    print("1 - Start Game")
    print("2 - Load Game")
    print("3 - Quit")
    start_choice="0"
    while ord(start_choice)<49 or ord(start_choice)>51: 
        # This keeps asking the user for an input until it is valid. The ord value gets the ascii value. 49 in ascii is "1" and 50 in ascii is "2"
        start_choice=input()
        if start_choice=="1":
            save_file_num=saved_choice("overwrite")
            save_file_dict=read_save_file(save_file_num)
            print()
            print(game_map_dict["game_map"]["story"]["intro_text"])
        elif start_choice=="2":
            save_file_num=saved_choice("load")
        elif start_choice=="3":
            print("Exiting...")
            print("Exited")
            return(True,"")
        else:
            start_choice="0"
            print("Please enter valid option")
    return(False,save_file_num)

def main():
    verb_commands,noun_commands,exit,save_file_num=__init__()
    while exit!=True:
        player_options(save_file_num)
        choice=input().lower()
        print()
        exit=room_decision(exit,choice,verb_commands,noun_commands,save_file_num)

main()

