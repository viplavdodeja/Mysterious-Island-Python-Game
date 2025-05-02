import random
import time
import os

playing = False
treasure_code = []
inventory = {0: "0 Gold Coins", 1: "Map", 2: "Flashlight"}
current_user = None
high_score = "Stage 0"
hidden_treasures = ["Jeweled Crown", "Diamond Necklace", "Golden Chalice", "Ancient Coin",
    "Emerald Ring", "Sapphire Amulet", "Ruby Bracelet", "Silver Goblet",
    "Pearl Tiara", "Obsidian Idol"]

def get_user():
    global playing
    global current_user
    global high_score

    print("1. View High Scores")
    print("2. Play Again")
    print("3. Create Account")
    print()

    try:
        answer = int(input("Enter your choice: "))

        if answer == 1:
            print("High Scores:")
            try:
                with open("highscores.txt", "r") as file:
                    for line in file:
                        data = line.strip().split("|")
                        if len(data) >= 3:
                            print(f"Player ID: {data[0]}, High Score: {data[1]}, Gold Coins Collected: {data[2]}")
            except FileNotFoundError:
                print("No High scores available yet.")
            get_user()
        elif answer == 2:
            player_name = input("Player Name: ")
            if check_player(player_name):
                current_user = player_name
                print(f"Welcome back {player_name}. Let's play again.")
                playing = True
            else:
                print("Invalid credentials. Please try again.")
                return get_user()
        elif answer == 3:
            create_account()
            return get_user()
        else:
            print("Invalid choice. Please try again.")
            return get_user()
    except ValueError:
        print("Please enter a valid choice.")
        return get_user()

def create_account():
    player_name = input("Create a player ID: ")

    if os.path.exists("highscores.txt"):
        with open("highscores.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")
                if data[0] == player_name:
                    print("That Player ID already exists. Please try another.")
                    return create_account()

    with open("highscores.txt", "a") as file:
        file.write(f"{player_name}|Stage 0|0\n")
        for key in inventory:
            if key != 0:
                file.write(f"    {inventory[key]}\n")

    print(f"Account successfully created. Welcome {player_name}. Please log in!")

def check_player(player_name):
    if not os.path.exists("highscores.txt"):
        return False

    with open("highscores.txt", "r") as file:
        for line in file:
            data = line.strip().split("|")
            if data[0] == player_name:
                return True

def update_highscore(player_name, score):
    global inventory
    global hidden_treasures
    if not player_name:
        return

    updated = []
    found_player = False

    try:
        with open("highscores.txt", "r") as file:
            lines = file.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith(player_name + "|"):
                found_player = True
                parts = line.split("|")
                old_score = parts[1].strip()
                stage_order = {
                    "Stage 0": 0, "Stage 1": 1, "Stage 2": 2, "Stage 3": 3,
                    "Stage 4": 4, "Stage 5": 5, "Stage 6": 6
                }
                current_score = score if stage_order.get(score,0) > stage_order.get(old_score, 0) else old_score

                old_inventory = []
                i += 1
                while i < len(lines) and lines[i].startswith("    "):
                    item = lines[i].strip()
                    if item not in old_inventory:
                        old_inventory.append(item)
                    i += 1
                new_inventory = []
                for key, value in inventory.items():
                    if key != 0 and value not in old_inventory and value not in new_inventory:
                        new_inventory.append(value)


                gold = inventory[0].split()[0]
                updated.append(f"{player_name}|{current_score}|{gold}\n")

                for item in old_inventory + new_inventory:
                    updated.append(f"    {item}\n")

            else:
                updated.append(lines[i])
                i += 1
        if not found_player:
            gold = inventory[0].split()[0]
            updated.append(f"{player_name}|{score}|{gold}\n")
            for key in inventory:
                if key != 0:
                    updated.append(f"    {inventory[key]}\n")

        with open("highscores.txt", "w") as file:
            file.writelines(updated)
    except FileNotFoundError:
        print("Could not update the high score. Source file not found.")

def generate_treasure_code():
    global treasure_code
    treasure_code = (random.randint(1, 9), random.randint(1, 9), random.randint(1, 9))
    return

def start_game():
    global inventory
    print("🌏WELCOME TO THE MYSTICAL ISLAND🌏\n")
    print("PLease log in to play")
    print()
    get_user()
    print("Explore the island, solve the mysteries, survive the challenges, and maybe you'll even find the treasure!")
    print("Choose your paths carefully to unveil the secrets of the island.")
    print("💠💠💠💠💠💠💠💠💠💠💠💠💠💠💠💠💠💠💠💠")
    generate_treasure_code()
    print("In your bacpack:")
    for key, value in inventory.items():
        print(value)
    print()

def stage_1():
    # decide where to explore first. begin at basecamp.
    # random generator chooses which one will be correct. 1/3 results in danger.
    global treasure_code
    global playing
    global high_score
    high_score = "Stage 1"
    time.sleep(1)
    #make more possible options for danger to reduce the chance of choosing the wrong path
    locations = ("The Dense Jungle", "The Abandoned Lighthouse", "The Hidden Cave")
    danger = random.randint(1,len(locations) + 2 )

    print("You begin at the base camp. From here, you can explore three different areas of the island.\n")
    print(f"1. {locations[0]}")
    print(f"2. {locations[1]}")
    print(f"3. {locations[2]}")

    while True:
        try:
            user_choice = int(input("Enter the number corresponding to the area you want to explore: "))
            if user_choice not in [1, 2, 3]:
                print("Please enter a valid choice (1, 2, or 3).")
                continue
            break
        except ValueError:
            print("Please enter a valid number (1, 2, or 3).")
    print()
    time.sleep(1.5)

    if user_choice == danger:
        print("Oh no! You were attacked by a wild animal and couldn't proceed.")
        print("GAME OVER! You finished at Stage 1.")
        playing = False
    else:
        #print(f"You made the right choice! Your exploration continues. You walk down the path towards the {locations[user_choice - 1]}")
        print(f"You made the right choice! Your exploration continues. You walk down the path.")
        print()

def stage_2():
    global playing
    global high_score
    high_score = "Stage 2"
    #successfully made it to stage 2. You find a scrap of paper with a 3-digit code on it
    #The first number is visible but the other two are redacted
    #Now you must solve a riddle
    #three guesses to get it correct. If user fails, game over.
    #will take string input from user
    print("As you move forwards in your adventure, you check your map and notice a code scrawled on the top")
    print("The writing is old and faded so you can only make out the first number.")
    print(f"{treasure_code[0]} _ _")
    print("You pocket the map and keep moving forwards.\n")
    time.sleep(0.5)

    print("🛕")
    print("You reach an ancient temple. The large doors in front are locked and guarded by a statue")
    print("It speaks....\n")
    time.sleep(4)

    print("'You face a riddle at this gate. Solve it to proceed further!'\n")

    print("You can’t change me once I'm born, \n"
          "Though I might look like a list's form.\n"
          "I sit with parentheses, not brackets wide.\n"
          "What am I that keeps data inside?")

    answer = "tuple"
    attempts = 0
    max_attempts = 3
    counter = 3

    while attempts < max_attempts:
        user_answer = input("Your Answer: ").lower()
        counter -= 1
        if counter > 1:
            if user_answer == answer:
                print()
                time.sleep(1)
                print("Correct! The statue moves to the side and lets you pass")
                print()
                return
            else:
                attempts += 1
                print()
                time.sleep(1)
                print(f"Incorrect! You have {max_attempts - attempts} attempts remaining.")
                print("Hint: the answer is a python data type.")
                print()
        elif counter == 1:
            if user_answer == answer:
                print()
                time.sleep(1)
                print("Correct! The statue moves to the side and lets you pass")
                print()
                time.sleep(1)
                return
            else:
                attempts += 1
                print()
                time.sleep(1)
                print(f"Incorrect! You have {max_attempts - attempts} attempts remaining.")
                print("Hint: Here is an example of the answer in use:")
                print("data_type = (1, 64, 'apple', 10)")
                print("What is the data_type?")
                print()
        else:
            if user_answer == answer:
                print()
                time.sleep(1)
                print("Correct! The statue moves to the side and lets you pass")
                print()
                time.sleep(1)
                return
            else:
                attempts += 1
                print()
                time.sleep(1)
                print(f"Incorrect! You have {max_attempts - attempts} attempts remaining.")
                print()


    print("You failed to solve the riddle! The stone statue attacks you.")
    time.sleep(2)
    print("GAME OVER! You finished at Stage 2.")
    playing = False

def stage_3():
    #made it to the temple. on the wall you see 3 numbers.
    #the first matches the scrap of paper, second is new, and third is eroded and not readable.
    #wall with unlock combination
    #correct sequence to open door is (2, 4, 8, 16, 32)

    global playing
    global treasure_code
    global high_score
    high_score = "Stage 3"
    #Update to the ongoing treasure code game logic:
    print("You've made it to the temple! On the wall you see 3 numbers.\n")
    print(f"The first number {treasure_code[0]} matches the scrap of paper you found earlier.")
    print(f"The code reads {treasure_code[0]} {treasure_code[1]} _")
    print(f"The third number is eroded and unreadable.\n")

    #Now the game logic for the next stage
    print("As you keep walking, you reach a wooden door.")
    print(f"On the wall are 5 numeric dials. The first two read 2 4 _ _ _")
    print("You need to complete the sequence by entering the next three numbers.")

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        user_answers = []

        #first num from user
        while True:
            try:
                print("The sequence reads 2 4 _ _ _")
                time.sleep(0.5)
                answer1 = int(input("Enter your choice for the third number: "))
                user_answers.append(answer1)
                break
            except ValueError:
                print("Please enter a valid number as your choice.")
        #second num from user
        while True:
            try:
                print(f"Your sequence reads 2 4 {answer1} _ _")
                time.sleep(1)
                answer2 = int(input("Enter your choice for the fourth number: "))
                user_answers.append(answer2)
                break
            except ValueError:
                print("Please enter a valid number as your choice.")

        #third num from user
        while True:
            try:
                print(f"Your sequence reads 2 4 {answer1} {answer2} _")
                time.sleep(1)
                answer3 = int(input("Enter your choice for the last number: "))
                print(f"Your sequence reads 2 4 {answer1} {answer2} {answer3}")
                user_answers.append(answer3)
                break
            except ValueError:
                print()
                print("Please enter a valid number as your choice.")

        if user_answers == [8, 16, 32]:
            print()
            time.sleep(1)
            print("You got it! the door unlocks and swings open. You enter cautiously.")
            print()
            return
        else:
            attempts += 1
            tries = max_attempts - attempts
            if tries > 0:
                time.sleep(1)
                print(f"Incorrect! The door doesnt budge. You have {tries} remaining attempts.")
                print("Think about common factors between the first two numbers.")
            else:
                print("No more tries remaining. The door remains shut, and you have no other way forwards.")
                time.sleep(2)
                print("GAME OVER! You made it to stage 3.")
                playing = False
                return

def stage_4():
    #you open the door successfully and make into the temple!
    #along the walls you see three numbers repeated over and over again:
    #this is the random treasure code for the game
    #you walk down the halls exploring the temple, eventually finding a treasure room.
    #the room requires a mathematical riddle to be unlocked
    global playing
    global treasure_code
    global high_score
    high_score = "Stage 4"

    print("As the door swings open, you see another passageway.")
    print("You walk down the halls, and notice three numbers repeated on the walls over and over again.")
    print(f"{treasure_code[0]} {treasure_code[1]} {treasure_code[2]}")
    print(f"{treasure_code[0]} {treasure_code[1]} {treasure_code[2]}")
    print(f"{treasure_code[0]} {treasure_code[1]} {treasure_code[2]}")

    print("You make a mental note of these numbers and keep exploring.\n")
    time.sleep(1)

    print("You finally find the treasure room, but the door is locked. ")
    print("The door is locked by a puzzle. In order to unlock it, you must clear a set of mathematical puzzles.")

    num1 = random.randint(3, 15)
    num2 = random.randint(3, 15)
    num3 = random.randint(1, 8)
    num4 = random.randint(1, 8)

    #question 1:
    operation = random.choice(['+', '-', '*'])

    if operation == '+':
        correct_answer = num1 + num2
        equation = f"{num1} + {num2}"
    elif operation == '-':
        correct_answer = num1 - num2
        equation = f"{num1} - {num2}"
    else:
        correct_answer = num1 * num2
        equation = f"{num1} × {num2}"

    time.sleep(1)
    print(f"Solve: {equation} = ?")

    try:
        user_answer = int(input("Your answer: "))

        if user_answer == correct_answer:
            time.sleep(1)
            print("Correct! You move on to the next question.")
            print()
        else:
            print(f"Wrong! The correct answer was {correct_answer}.")
            print("The floor beneath you gives way, and you fall into a trap!")
            time.sleep(2)
            print("GAME OVER! You finished at Stage 4.")
            playing = False
            return
    except ValueError:
        print("Invalid input. The puzzle resets and triggers a trap mechanism. The floor beneath you gives way, and you fall into a trap!")
        time.sleep(2)
        print("GAME OVER! You finished at Stage 4.")
        playing = False
        return

    #question 2:
    correct_answer2 = (num1 + num3) * num4
    equation2 = f"({num1} + {num3}) * {num4}"

    print(f"Solve: {equation2} = ?")

    try:
        user_answer = int(input("Your answer: "))

        if user_answer == correct_answer2:
            print("Correct! Next question.")
            print()
        else:
            print(f"Wrong! The correct answer was {correct_answer2}.")
            print("The floor beneath you gives way, and you fall into a trap!")
            time.sleep(2)
            print("GAME OVER! You finished at Stage 4.")
            playing = False
            return
    except ValueError:
        print("Invalid input. The puzzle resets and triggers a trap mechanism. The floor beneath you gives way, and you fall into a trap!")
        time.sleep(2)
        print("GAME OVER! You finished at Stage 4.")
        playing = False
        return

    # question 3:
    correct_answer3 = (num3 + num4) * (num2 - num1)
    equation3 = f"({num3} + {num4}) * ({num2} - {num1})"

    print(f"Solve: {equation3} = ?")

    try:
        user_answer = int(input("Your answer: "))

        if user_answer == correct_answer3:
            print("Correct! The door creaks open revealing a hidden room with an alcove.")
            print()
        else:
            print(f"Wrong! The correct answer was {correct_answer3}.")
            print("The floor beneath you gives way, and you fall into a trap!")
            time.sleep(2)
            print("GAME OVER! You finished at Stage 4.")
            playing = False
            return
    except ValueError:
        print("Invalid input. The puzzle resets and triggers a trap mechanism. The floor beneath you gives way, and you fall into a trap!")
        time.sleep(2)
        print("GAME OVER! You finished at Stage 4.")
        playing = False
        return


def stage_5():
    #success! you unlock the door and see a large treasure chest in front of you.
    #In order to unlock this chest, you must enter a 3-digit code.
    #three tries. this is the secret treasure code you have discovered during the exploration
    global playing
    global treasure_code
    global inventory
    global high_score
    global hidden_treasures
    high_score = "Stage 5"

    print("You've made it to the treasure room.")
    print("In front of you stands a large treasure chest. The padlock has a 3-digit combo.")
    print("You need to enter the correct combination to unlock the chest.\n")
    print("Remember the numbers you've seen throughout your journey.")

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        user_attempt = input("Enter your guess for the 3-digit code: ")

        try:
            code = [int(digit) for digit in user_attempt.split()]
            if len(code) != 3:
                print("Please enter a valid 3-digit code. Use spaces to separate them.")
                continue

            if tuple(code) == treasure_code:
                print("You got it! The chest unlocks. 💰💰It is filled with gold coins!💰💰")
                print("*Inventory + 50 Gold coins*")
                inventory[0] = "50 Gold Coins"

                rewards = random.sample(hidden_treasures, 2)

                current_items = set(inventory.values())
                next_key = max(inventory.keys()) + 1 if inventory else 1

                for item in rewards:
                    if item in current_items:
                        print(f"You found {item}, but you already have it.")
                    else:
                        inventory[next_key] = item
                        print(f"*Inventory + {item}*")
                        next_key += 1

                print()
                return
            else:
                attempts += 1
                tries = max_attempts - attempts
                if tries > 0:
                    print(f"Incorrect combination! You have {tries} attempts remaining.")
                else:
                    print("No more tries remaining. The chest seals and the treasure is gone forever.")
                    time.sleep(2)
                    print("GAME OVER! You finished at stage 5.")
                    playing = False
                    return
        except ValueError:
            print("Please enter a valid 3-digit code. Use spaces to separate them.")

def stage_6():
    #you have raided the temple, and made it to the docks. You must make a speedy getaway. Which boat will you use?
        #small wooden boat
        #luxury yacht
        #sturdy fishing vessel
    #success if choose option 1 or 3. Luxury yach will suddenly take on water and sink in the middle of the ocean
    global playing
    global inventory
    global high_score

    print("You have finished raiding the temple and have made it to the docks with your treasure.")
    print("In your backpack:")
    for key, value in inventory.items():
        print(value)
    print("It is time for your escape back to civilization. Which boat will you choose?")
    print()
    print("1. Small wooden raft ⛵\n"
          "The boat looks leaky and has a cracked paddle on board. No one is near it and it would be easy to sneak off with the treasure in.\n"
          "That is...if it stays afloat.\n"
          "(Cost: Free)\n")
    print("2. Luxury yacht 🚤\n"
          "The captain eyes your treasure greedily. While a potential quick getaway, this option will certainly not be cheap\n"
          "Will you trust the captain?\n"
          "(Cost: 25 Gold Coins)\n")
    print("3. Sturdy fishing vessel 🛶\n"
          "Manned by a few sailors, this boat is getting ready to depart for voyage.\n"
          "The captain agrees to take you as far as the next city.\n"
          "(Cost: 3 Gold Coins)\n")

    user_choice = input("Enter the number of your choice: ")

    if user_choice == "3":
        print("Good choice! Your vessel proves reliable and you safely navigate away from the island.")
        print("You've escaped with the treasure!")
        high_score = "Stage 6"
        return
    elif user_choice == "2":
        print("The seedy crew of the yacht steal all your belongings while you sleep at night. Your treasure is nowhere to be found.")
        time.sleep(2)
        print("GAME OVER! You finished at Stage 6.")
        playing = False
    elif user_choice == "1":

        print("Oh no! The wooden raft suddenly starts taking on water and sinks in the middle of the ocean.")
        time.sleep(2)
        print("GAME OVER! You finished at Stage 6.")
        playing = False

    else:
        print("Invalid choice! While you hesitate, island guards capture you.")
        time.sleep(2)
        print("GAME OVER! You finished at Stage 6.")
        playing = False

def main():
    global high_score
    global current_user
    global hidden_treasures
    start_game()

    stages = [stage_1, stage_2, stage_3, stage_4, stage_5, stage_6]

    for stage in stages:
        if not playing:
            break
        stage()

    print()

    if playing:
        print("You Won! You successfully completed all the challenges and escaped the island alive!\n"
              "💰Not to mention that shiny new loot of yours!")
    else:
        print("Aww. You lost. Better luck next time on the Mystical Island. ")

    if current_user:
        update_highscore(current_user, high_score)

    player_treasures = set()
    if os.path.exists("highscores.txt"):
        with open("highscores.txt", "r") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith(current_user + "|"):
                    i += 1
                    while i < len(lines) and lines[i].startswith("    "):
                        item = lines[i].strip()
                        if item in hidden_treasures:
                            player_treasures.add(item)
                        i += 1
                    break
                i += 1

    found_count = len(player_treasures)
    total_count = len(hidden_treasures)

    print(f"\nHidden Treasure Tracker: You’ve found {found_count} out of {total_count} hidden treasures!")

if __name__ == "__main__":
    main()