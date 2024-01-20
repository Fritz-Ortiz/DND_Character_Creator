import requests

url = "https://www.dnd5eapi.co"
headers = {'Accept': 'application/json'}


Character = {
    "name": "",
    "race": {},
    "class": {},
    "equipment": {},
    }
def Player():
    print("\n\n")
    for detail in Character:
        print(detail)
        print(Character[detail])
        print("\n\n\n")


def addInfo(index, data, forOutput=''):
    print("started adding . . .")
    i = index
    info = data
    
    if type(Character[i]) == dict:
        Character[i] = {forOutput: info}
        print("Character " + i + " set to " + forOutput)
    else:
        Character[i] = info
        print("Character " + i + " set to " + data)
    

def Name():
    name = input("What would you like your name to be? Name: ")
    addInfo("name", name)


def Race():
    option = 1
    races = {1: "dragonborn",2: "dwarf",3: "elf",4: "gnome",5: "half-elf",6: "half-orc",6: "halfling",7: "human",8: "tiefling"}

    print("Choose your Race:")
    for i in races:
        print(str(option) + ". " + str(races[i]))
        option += 1
    try:
        pick = input("Number: ")

        lookup = "/api/races"
        item = races[int(pick)]

        response = requests.get(url + lookup + "/" + item, headers=headers)

        if response.status_code == 200:
            data = response.json()
            addInfo("race", data, data['index'])
            print("Race is " + str(races[int(pick)]))
        else:
            print("Something went wrong")
    except:
        print("failure while picking race, please try again.")

def Class():
    option = 1
    classes = {1: "barbarian", 2: "bard", 3: "cleric", 4: "druid", 5: "fighter", 6: "monk", 7: "paladin", 8: "ranger", 9: "rogue", 10: "sorcerer", 11: "warlock", 12: "wizard"}

    print("Choose your class:")
    for i in classes:
        print(str(option) + ". " + str(classes[i]))
        option += 1
    
    pick = input("Number: ")
    try:
        lookup = "/api/classes"
        item = classes[int(pick)]

        response = requests.get(url + lookup + "/" + item, headers=headers)

        if response.status_code == 200:
            data = response.json()
            toAdd={"hit die" : data['hit_die']}
            addInfo("class", toAdd, data['name'])
            print("class is " + str(classes[int(pick)]))
        else:
            print("Something went wrong")
    except:
        print("failure while picking class, please try again.")


def Weapons():
    weapons = []
    option = 0
    
    response = requests.get(url + "/api/equipment-categories/weapon", headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            equipment = data['equipment']
            for i in equipment[:-4]:
                weapons.append(i['index'])

            print("Choose a weapon:")
            
            for i in weapons:
                print(str(option + 1) + ". " + weapons[option])
                option += 1
            pick = int(input("Enter your Choice: ")  )
            print(f"You have chosen {weapons[pick -1]}")
            getinfo = input("Would you like to know more about this weapon? (Y/N)")  
            if getinfo.lower().strip() == "y":
                itemInfo(weapons[pick -1])
            else:
                print("understood, returning to main menu...")
                pass
            
        except:
            print("failure while picking weapon, please try again.")
    
    else:
         print("Something went wrong")

def Armor():
    armor = []
    option = 0
    
    response = requests.get(url + "/api/equipment-categories/armor", headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            equipment = data['equipment']
            for i in equipment[:-4]:
                armor.append(i['index'])

            print("Choose a piece of armor:")
            
            for i in armor:
                print(str(option + 1) + ". " + armor[option])
                option += 1
            pick = int(input("Enter your Choice: ")  )
            print(f"You have chosen {armor[pick -1]}")
            getinfo = input("Would you like to know more about this weapon? (Y/N)")  
            if getinfo.lower().strip() == "y":
                itemInfo(armor[pick -1])
            else:
                print("Returning to main menu...")
                pass
            
        except:
            print("failure while picking armor, please try again.")
    
    else:
         print("Something went wrong")


def itemInfo(itemName):
    #index = characterIndex  characterIndex
    item = itemName
    response = requests.get(url + "/api/equipment/" + item, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        try:
            response = requests.get(url + "/api/magic-items/" + item, headers=headers)
            data = response.json()
        except:
            print("Could not find item, please try again.")
            return 'error: item not found'

    
    print(f"\nName: {data['name']}")
    #Check what attributes there are and print them

    if 'equipment_category' in data and 'name' in data['equipment_category'] and data['equipment_category']['name'] == 'Weapon':
        print(f"\nEquipment Category: {data['equipment_category']['name']}")
        if 'desc' in data and data['desc'] and len(data['desc']) > 1:
            print(f"\nDescription: {data['desc'][1:]}\n")

        

        if 'weapon_category' in data:
            print(f"\nWeapon Category: {data['weapon_category']}")

        if 'weapon_range' in data:
            print(f"\nWeapon Range: {data['weapon_range']}")

        if 'category_range' in data:
            print(f"\nCategory Range: {data['category_range']}")

        if 'cost' in data and 'quantity' in data['cost']:
            if 'unit' in data['cost']:
                print(f"\nCost: {data['cost']['quantity']} {data['cost']['unit']}")
            else:
                print(f"\nCost: {data['cost']['quantity']}")

        if 'throw_range' in data:
            if 'normal' in data['throw_range'] and 'long' in data['throw_range']:
                print(f"\nRange: Normal: {data['throw_range']['normal']} ft, Long: {data['throw_range']['long']} ft")

        if 'weight' in data:
            print(f"\nWeight: {data['weight']} lbs")
            print("\nProperties:")
        if 'properties' in data:
            for prop in data['properties']:
                print(f"- {prop['name']}")
        if 'special' in data:
            print("\nSpecial:")
            for line in data['special']:
                print(line)
        print()        
        toChar = input("Would you like to add this to your character? (Y/N)")
        if toChar.lower().strip() == "y":
                    addInfo("equipment", data, data['name'])
                    print()
        else:
            print("Returning to main menu... \n\n")
            pass
    else:
        for i in data:
            if type(data[i]) == dict:
                for detail in data[i]:
                    if detail != 'url'  and detail != 'index' :
                        print(str(detail) +": " + str(data[i][detail]))
            else:
                if i != 'url'  and i != 'index' :
                    print(str(i) +": " + str(data[i]))
        print()        
        toChar = input("Would you like to add this to your character? (Y/N)")
        if toChar.lower().strip() == "y":
                    addInfo("equipment", data, data['name'])
                    print()
        else:
            print("Returning to main menu... \n\n")
            pass



#Primary functions that the user can choose
option = {
            "1" : "Name",
            "2" : "Race",
            "3" : "Class",
            "4" : "Armor",
            "5" : "Weapons",
            "6": "Player"
            
        } 
#Runs the chosen function
def Run(id):
    if id in option:
        # Get the function name from the dictionary
        function_name = option[id]
        
        # Execute the function using eval()
        eval(function_name + "()")
    


def main():
    choice = ""
    print("Welcome to the D&D 5e Character Creator!")
    

    while True:
        print("Commands:")
        print("1 - Character Name")
        print("2 - Race")
        print("3 - Class")
        print("4 - Armor")
        print("5 - Weapons")
        print("6 - Show Palyer Info")
        print("7 - I'm Finished")

        choice = input("Enter your choice: ")

        if 1 <= int(choice) <= 6:
            print(choice)
            Run(choice)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()