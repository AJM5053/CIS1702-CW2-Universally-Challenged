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

def view_npcs(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    if save_file_dict["save_file"]["game_map"][current_room]["location_npcs"]==[]:
        print("There are no NPCs in this room")
    else:
        for npc in save_file_dict["save_file"]["game_map"][current_room]["location_npcs"]:
            print(npc.capitalize().replace("_"," "))

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
    print(f"1 - {save_file_1_dict['save_file']['player']['current_room']}")
    save_file_2_dict=read_save_file("2")
    print(f"2 - {save_file_2_dict['save_file']['player']['current_room']}")
    save_file_3_dict=read_save_file("3")
    print(f"3 - {save_file_3_dict['save_file']['player']['current_room']}")
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

def remove_item(item,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    items_dict=read_items()
    save_file_dict["save_file"]["player"]["current_carry_weight"]-=items_dict["items"][item]["weight"]
    save_file_dict["save_file"]["player"]["inventory"].remove(item)
    update_save_file(save_file_dict,save_file_num)

def add_item(item,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    items_dict=read_items()
    if weight_check(item,save_file_num):
        save_file_dict["save_file"]["player"]["current_carry_weight"]+=items_dict["items"][item]["weight"]
        save_file_dict["save_file"]["player"]["inventory"].insert(0,item)
        update_save_file(save_file_dict,save_file_num)
        return(True)
    return(False)

# The command to let the player move in a direction to get to other rooms
def go(separated,exit,save_file_num):
    if len(separated)<2:
        print("Pick a direction. You can go north, east, south, or west")
        return(exit)
    direction=separated[1]
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    game_map_dict=read_game_map()
    connections=game_map_dict["game_map"]["room_connections"]
    if direction not in connections[current_room]:
        print("Invalid direction")
        return(exit)
    new_room=connections[current_room][direction]
    if new_room=="wall":
        print("You just walked into a wall")
        return(exit)
    save_file_dict["save_file"]["player"]["current_room"]=new_room
    update_save_file(save_file_dict,save_file_num)
    print("You moved"+direction)
    return(exit)

def validate_input(verb_commands,choice,save_file_num):
    if is_empty(choice):#If the inputs inputs nothing
        return(False,"")
    parsed=choice.split()
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    npc_result,parsed=npc_name(parsed,save_file_dict,current_room)
    if npc_result:
        return(True,parsed)
    else:
        return(False,parsed)

def parse_validate_input(verb_commands,noun_commands,choice,exit,save_file_num):
    parsed_data = choice.split(' ')

    verb = parsed_data[0].lower() ### defines the first half of the user input as the verb
    noun = parsed_data[1].lower() if len(parsed_data) > 1 else None ### defines the second half of the user input as the noun

    for each_verb in verb_commands:
        if verb == each_verb:
            action(parsed_data,exit,save_file_num) ### sent to action function to execute command
    print("Please enter valid option")
    return(exit)

def action(separated,exit,save_file_num):
    function_name=separated[0] # String of function name
    if function_name not in globals(): # Small guard to deal with invalid commands e.g. fly
        print("That command doesn't exist")
        return(exit)
    function=globals()[function_name] # Globals returns dictionary of global variables including functions
    exit=function(separated,exit,save_file_num)
    return(exit)

def pickup(seperated,exit,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    if save_file_dict["save_file"]["game_map"][current_room]["room_inventory"]!=None: # Checks that the current room has items dropped in it
        item_to_pickup=seperated[1]
        if item_to_pickup in save_file_dict["save_file"]["game_map"][current_room]["room_inventory"] and item_to_pickup!="": #Checks if the given item to pickup is dropped in the current room
            if add_item(item_to_pickup,save_file_num):
                save_file_dict=read_save_file(save_file_num)
                save_file_dict["save_file"]["game_map"][current_room]["room_inventory"].remove(item_to_pickup) # Removes the item from the items dropped in the room
                update_save_file(save_file_dict,save_file_num)
                print(f"{item_to_pickup.replace('_', ' ')} picked up and added to inventory...")
        else:
            print("Item is not dropped in this room")
            print()
    return(exit)

# Reads the current save file and returns what weapon the player has equipped
def equipped_weapon(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    return save_file_dict["save_file"]["player"]["equipped_weapon"]

def room_decision(exit,choice,verb_commands,noun_commands,save_file_num):
    valid,separated=parse_validate_input(verb_commands,noun_commands,choice,exit,save_file_num)
    if valid:
        exit=action(separated,exit,save_file_num)
    else:
        print("Invalid command try again")
        print()
    return(exit)

def drop(seperated,exit,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    if save_file_dict["save_file"]["player"]["inventory"]!=None: # Checks the player has items in their inventory
        item_to_drop=seperated[1]
        if item_to_drop in save_file_dict["save_file"]["player"]["inventory"] and item_to_drop!="": # Checks if the given item to drop is in the players inventory
            remove_item(item_to_drop,save_file_num) # Removes the earliest of that item in the list from the players inventory
            save_file_dict=read_save_file(save_file_num)
            current_room=save_file_dict["save_file"]["player"]["current_room"]
            save_file_dict["save_file"]["game_map"][current_room]["room_inventory"].insert(0,item_to_drop) # Add the dropped item to the dropped items file for the current room
            update_save_file(save_file_dict,save_file_num)
            print(f"{item_to_drop.replace('_', ' ').capitalize()} dropped in room: {current_room.replace('_', ' ')}...")
        else:
            print("You do not have this item in your inventory")
            print()
    else:
        print("Your inventory is empty")
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




def player_options(save_file_num): #This displays to the player what their options are and asks for an input
    #Player options
    game_map_dict=read_game_map()
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    print()
    print("#---OPTIONS---#")
    print(f"Current room: {current_room.replace("_", " ")}")
    print(game_map_dict["game_map"]["room_descriptions"][current_room])
    print()
    print("What would you like to do?")
    print()
    print("Go...") #This command is for the user to choose a direction via the logic term go
    print(f"North - {game_map_dict["game_map"]["room_connections"][current_room]["north"].replace("_", " ")}")
    print(f"East - {game_map_dict["game_map"]["room_connections"][current_room]["east"].replace("_", " ")}")
    print(f"South - {game_map_dict["game_map"]["room_connections"][current_room]["south"].replace("_", " ")}")
    print(f"West - {game_map_dict["game_map"]["room_connections"][current_room]["west"].replace("_", " ")}")
    print()
    print("Drop...") #This command is designed for the user to drop the item
    temp=view_inventory(save_file_num)
    print("Pickup...") #This command is designed for the user to pickup th'e iteme
    view_dropped_items(save_file_num)
    print()
    print("Interact With:")
    view_npcs(save_file_num)
    print()
    print("View Stats")
    print("Help")
    print("Quit")


def weight_check(item,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    items_dict=read_items()
    player_dict=read_player()
    if save_file_dict["save_file"]["player"]["current_carry_weight"]>=player_dict["player"]["carry_weight"]:
        print("Inventory Full")
        return(False)
    elif (save_file_dict["save_file"]["player"]["current_carry_weight"]+items_dict["items"][item]["weight"])>player_dict["player"]["carry_weight"]:
        print("You do not have the inventory space for this item")
        return(False)
    else:
        return(True)



def view_inventory(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    if save_file_dict["save_file"]["player"]["inventory"]==[]:
        print("You inventory is empty")
        print()
        return(False)
    else:
        for item in save_file_dict["save_file"]["player"]["inventory"]:
            print(item.replace("_"," ").capitalize())
        print()
        return(True)
