import json

def test_variables(current_area,player_dict,area_directions):
    #test_variables(current_area,player_dict,area_directions)
    print("VARIABLES TEST")
    print()
    print(type(area_directions))
    print(area_directions)
    print()
    print(type(current_area))
    print(f"current_area - {current_area}")
    print()
    print(f"Player json - {player_dict}")

#Saving the game -
#Either use a "local" dictionary for each file across the whole code and only write to the file while quitting

def update_dropped_items(dropped_items_dict):
    with open("dropped_items.json", 'w') as write_file:
        json.dump(dropped_items_dict, write_file)
    write_file.close()

def update_inventory(inventory_dict):
    with open("inventory.json", 'w') as write_file:
        json.dump(inventory_dict, write_file)
    write_file.close()

def update_game_map(game_map_dict):
    with open("game_map.json", 'w') as write_file:
        json.dump(game_map_dict, write_file)
    write_file.close()

def update_game_map(dropped_items_dict):
    with open("dropped_items.json", 'w') as write_file:
        json.dump(dropped_items_dict, write_file)
    write_file.close()

def update_player(player_dict):
    with open("player.json", 'w') as write_file:
        json.dump(player_dict, write_file)
    write_file.close()

def read_dropped_items():
    with open("dropped_items.json", mode="r") as read_file:   
        dropped_items_dict = json.load(read_file)
    read_file.close
    return(dropped_items_dict)

def read_game_map():
    with open("game_map.json", mode="r") as read_file:   
        game_map_dict = json.load(read_file)
    read_file.close
    return(game_map_dict)

def read_inventory():
    with open("inventory.json", mode="r") as read_file:   
        inventory_dict = json.load(read_file)
    read_file.close
    return(inventory_dict)

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

def __init__():
    exit=False
    game_map_dict=read_game_map()
    player_dict=read_player()
    #List of Valid commands
    verb_commands=["go","view","drop","pickup","quit"]
    noun_commands=["north","east","south","west","game","inventory","item"]
    current_area=starting_area(game_map_dict,player_dict)
    area_directions={
        "north_area":game_map_dict["game_map"]["area_connections"][current_area]["north"],
        "east_area":game_map_dict["game_map"]["area_connections"][current_area]["east"],
        "south_area":game_map_dict["game_map"]["area_connections"][current_area]["south"],
        "west_area":game_map_dict["game_map"]["area_connections"][current_area]["west"]
    } 
    return(exit,verb_commands,noun_commands,current_area,area_directions,game_map_dict,player_dict)

def update_areas(current_area,area_directions,game_map_dict): #Updates where each cardinal direction leads to for the current area
    area_directions.update({"north_area":game_map_dict["game_map"]["area_connections"][current_area]["north"]})
    area_directions.update({"east_area":game_map_dict["game_map"]["area_connections"][current_area]["east"]})
    area_directions.update({"south_area":game_map_dict["game_map"]["area_connections"][current_area]["south"]})
    area_directions.update({"west_area":game_map_dict["game_map"]["area_connections"][current_area]["west"]})
    return(area_directions)

def starting_area(game_map_dict,player_dict): #Sets what area the player first starts off in when opening the game
    print("Start from the start or where you last left off?")
    print("1 - From the start")
    print("2 - From where you last left off")
    start_choice="0"
    while ord(start_choice)<49 or ord(start_choice)>50: #Keeps asking the user for an input until it is valid. The Ord value gets the ascii value. 49 in ascii is "1" and 50 in ascii is "2".
        start_choice=input()
    if start_choice=="1":
        current_area=game_map_dict["game_map"]["area_properties"]["start_area"] # Predefined start areaby the json file
    else:
        current_area=player_dict["player"]["properties"]["current_area"] #Last location the user was at after quitting the game (must use the quit feature)
    return(current_area)

def player_options(current_area,game_map_dict,area_directions): #Displays the player what their options are and asks for an input
    dropped_items_dict=read_dropped_items()
    #Player options
    print(f"Current area: {current_area.replace("_", " ")}")
    print(game_map_dict["game_map"]["area_descriptions"][current_area])
    print()
    print("What would you like to do?")
    print()
    print("Go...") #Command is "go 'cardinal direction'"
    print(f"North - {area_directions["north_area"].replace("_", " ")}")
    print(f"East - {area_directions["east_area"].replace("_", " ")}")
    print(f"South - {area_directions["south_area"].replace("_", " ")}")
    print(f"West - {area_directions["west_area"].replace("_", " ")}")
    print()
    print("Quit")
    print("View Inventory")
    print("Drop...") #Command is "drop item"
    view_inventory()
    print("Pickup...") #Command is "pickup item"
    view_dropped_items(current_area)

    choice=input().lower()
    print()
    return(choice)

def check_key(game_map_dict,current_area,seperated): #Checks if player has correct key
    inventory_dict=read_inventory()
    key=game_map_dict["game_map"]["area_connections"][current_area][seperated[1]]+"_"+"key"
    if key in inventory_dict["inventory"]:
        return(True)
    else:
        return(False)

def parse_validate_input(verb_commands,noun_commands,choice,current_area,game_map_dict): #Checks if the input is valid from 2 lists for each half for the input.
    #Too many ifs
    if choice=="": #If the inputs inputs nothing
        return(False,"")
    else:
        seperated=choice.split() #Splits the input into the 2 components of "verb command" and "noun command" such as "go" and "north"
        if seperated[0] in verb_commands and len(seperated)==1: #If the command is only one word and valid
            return(True,seperated)
        elif seperated[0] in verb_commands and seperated[1] in noun_commands: #Checks both are valid
            if seperated[0]=="go":
                if game_map_dict["game_map"]["area_connections"][game_map_dict["game_map"]["area_connections"][current_area][seperated[1]]]["accessible"]=="False": #Checks whether the area chosen to move to is accessible
                    if game_map_dict["game_map"]["area_connections"][game_map_dict["game_map"]["area_connections"][current_area][seperated[1]]]!="wall":
                        if check_key(game_map_dict,current_area,seperated)==True:
                            print("You use your key to open the door")
                            return(True,seperated)
                        else:
                            print("Locked")
                            return(False,seperated)
                    else:
                        print("Inaccessible")
                    return(False,seperated)
            return(True,seperated)
        else:
            return(False,seperated)

def quit(current_area,player_dict): #Saves the area the player was in when they quit for the next time they play. This will be expanded upon to add more stuff saved and the ability to save to a seperate file
    exit=False
    while exit!=True:
        exit=True
        save=input("Would you like to save your progress? (Y/N)")
        if save=="Y":
            print("Saving current properties...")
            player_dict["player"]["properties"]["current_area"]=current_area
            update_player(player_dict)
            print("Saved")
            print("Exiting...")
            print("Exited")
        elif save=="N":
            print("Exiting without saving...")
            print("Exited")
        else:
            print("Please input a valid answer")
            exit=False
    return(exit)

def view_inventory():
    print("Inventory:")
    inventory_dict=read_inventory()
    if inventory_dict["inventory"][0]=="placeholder":
        print("You inventory is empty")
        print()
    else:
        for item in inventory_dict["inventory"][:-1]:
            print(item.replace("_", " "))
        print()

def go_area(seperated,game_map_dict,current_area):
    print(f"You have moved {seperated[1]} into area: {game_map_dict["game_map"]["area_connections"][current_area][seperated[1]].replace("_", " ")}")
    current_area=game_map_dict["game_map"]["area_connections"][current_area][seperated[1]]
    if current_area==game_map_dict["game_map"]["area_properties"]["end_area"]:
        print("You have won the game and found the correct area!")
        exit=True
    else:
        exit=False
    return(current_area,exit)

def drop_item(current_area):
    print("Which item would you like to drop?")
    view_inventory()
    inventory_dict=read_inventory()
    if inventory_dict["inventory"][0]!="placeholder": #Checking that the player has items in their inventory
        item_to_drop=input().lower().replace(" ", "_")
        if item_to_drop in inventory_dict["inventory"] and item_to_drop!="placeholder": #Checks if the given item to drop is in the players inventory
            inventory_dict["inventory"].remove(item_to_drop) #Removes the earliest of that item in the list from the players inventory
            update_inventory(inventory_dict)
            dropped_items_dict=read_dropped_items()
            dropped_items_dict["dropped_items"][current_area].insert(0,item_to_drop) #Add the dropped item to the dropped items file for the current area the player is in
            update_dropped_items(dropped_items_dict)
            print(f"{item_to_drop.replace("_", " ")} dropped in area: {current_area.replace("_", " ")}...")
        else:
            print("You do not have this item in your inventory")
            print()

def view_dropped_items(current_area):
    dropped_items_dict=read_dropped_items()
    if dropped_items_dict["dropped_items"][current_area][0]=="placeholder":
        print("This area has not dropped items...")
        print()
    else:
        for item in dropped_items_dict["dropped_items"][current_area][:-1]:
            print(item.replace("_", " "))
        print()

def pickup_item(seperated,current_area):
    print("Which item would you like to pick up?")
    view_dropped_items(current_area)
    dropped_items_dict=read_dropped_items()
    if dropped_items_dict["dropped_items"][current_area][0]!="placeholder": #Checking that the current room has any items dropped in it
        item_to_pickup=input().lower().replace(" ", "_")
        if item_to_pickup in dropped_items_dict["dropped_items"][current_area] and item_to_pickup!="placeholder": #Checking if the given item to pickup is dropped in the current area
            dropped_items_dict["dropped_items"][current_area].remove(item_to_pickup) #Removing the item from the items dropped in the area
            update_dropped_items(dropped_items_dict)
            inventory_dict=read_inventory()
            inventory_dict["inventory"].insert(0,item_to_pickup) #Adding the picked up item to the players inventory
            update_inventory(inventory_dict)
            print(f"{item_to_pickup.replace("_", " ")} picked up and added to inventory...")
        else:
            print("Item is not dropped in this area")
            print()

def action(seperated,game_map_dict,current_area,player_dict,exit):
    #Change this as this practically removes most of the purpose of validating the input
    if seperated[0]=="quit":
        exit=quit(current_area,player_dict)
    elif seperated[0]=="view" and seperated[1]=="inventory":
        view_inventory()
    elif seperated[0]=="go":
        current_area,exit=go_area(seperated,game_map_dict,current_area)
    elif seperated[0]=="drop" and seperated[1]=="item":
        drop_item(current_area)
    elif seperated[0]=="pickup" and seperated[1]=="item":
        pickup_item(seperated,current_area)
    else:
        print("Invalid command")
        print()
    return(exit,current_area)

def area_decision(exit,choice,player_dict,current_area,verb_commands,noun_commands,game_map_dict):
    valid,seperated=parse_validate_input(verb_commands,noun_commands,choice,current_area,game_map_dict)
    if valid==True:
        exit,current_area=action(seperated,game_map_dict,current_area,player_dict,exit)
        if seperated[0]=="quit":
            return(exit,current_area)
    else:
        print("Invalid command try again")
        print()
    return(exit,current_area)

def main():
    exit,verb_commands,noun_commands,current_area,area_directions,game_map_dict,player_dict=__init__()
    while exit!=True:
        area_directions=update_areas(current_area,area_directions,game_map_dict)
        choice=player_options(current_area,game_map_dict,area_directions)
        exit,current_area=area_decision(exit,choice,player_dict,current_area,verb_commands,noun_commands,game_map_dict)

main()