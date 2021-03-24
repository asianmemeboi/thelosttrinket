import random
import time
armor = "none"
gold = 0
maxstamina = 20
stamina = 20
health = 30
weapon = "fist"
critmult = 2
armordef = {
  "none": 30,
  "leather suit": 40,
  "kevlar vest": 50
}
weapondmg = {
  "fist": 1,
  "crude sword": 3,
  "polished sword": 5
}
critchance = {
  "fist": 3,
  "crude sword": 5,
  "polished sword": 10
}
monstertypes = {
  #1 - low hp high attack, 2 - medium hp medium attack, 3 - high hp low attack
  1: ("Goblin", 5, 5),
  2: ("Dwarf", 10, 3),
  3: ("Ogre", 15, 2),
  4: ("Joe", 100, 10)
}

class cavetree:
    def __init__(self, data, parent, level):
        #initializes binary tree for cave system
        self.left = 0
        self.right = 0
        self.data = data
        self.alive = True
        self.monstertype = 0
        self.monsterhealth = 0
        self.parent = parent
        self.level = level
    
    def getData(self):
        #test function for debugging
        return self.data
    
    def insert(self, data, level):
        #adds nodes to the tree based on "instructions" in the beginning of the data - "LRL monster" will place a monster at the tree to the left then right then left of the binary tree
        for i in data:
            if (i == " "):
                break
            else:
                if (i == "L"):
                    if self.left:
                        #recursively call self.insert to go down the tree
                        self.left.insert(data[1:], level + 1)
                        #splice the string to remove used instruction
                        break
                    else:
                        #create new node
                        self.left = cavetree(data[2:], self, level + 1)
                elif (i == "R"):
                    if self.right:
                        self.right.insert(data[1:], level + 1)
                        break
                    else:
                        self.right = cavetree(data[2:], self, level + 1)
    def printTree(self):
        #debugging function - prints current node then goes as much to the left as possible before going to the right by one node
        print(self.data, self.level)
        if self.left:
            self.left.printTree()
        if self.right:
            self.right.printTree()

def createLR(levels, levelslist):
    if levels == 0:
        return levelslist
    temp = levelslist.copy()
    if levelslist:
        levelslist = []
        for x in temp:
            #next level of instructions to the left
            levelslist.append("L" + x)
        for x in temp:
            #next level of instructions to the right
            levelslist.append("R" + x)
    else:
        levelslist = ["L", "R"]
    temp1 = levelslist.copy()
    levelslist = createLR(levels - 1, temp1)
    for i in levelslist:
        temp.append(i)
    return temp

levelsdata = {
  1: "monster",
  2: "monster",
  3: "checkpoint",
  4: "monster",
  5: "checkpoint",
  6: "monster",
  7: "monster",
  8: "checkpoint",
  9: "chest"
}
def appendData(levelsdata, levellist):
    #appends the thing you encounter at a certain level to the instructions, things you encounter at a certain level are defined in a dictionary (1: "monster") means that at level 1 you will encounter a monster
    for i in range(0, len(levellist)):
        if len(levellist[i]) != 9:
            level = levelsdata[random.randrange(1, 10)]
            levellist[i] = levellist[i] + " " + level
        else:
            levellist[i] = levellist[i] + " " + "final boss"
    return levellist

def addDataToTree(leveldata):
  root = cavetree("checkpoint", 0, 0)
  for i in leveldata:
    root.insert(i, 0)
  return root

def createTree(levelcount):
  #initializes tree
  instructionlist = createLR(levelcount, [])
  treedata = appendData(levelsdata, instructionlist)
  root = addDataToTree(treedata)
  return root

def fight(enemyhealth, weapon, monster):
  #tells the user they dealt damage, returns remaining enemy health to the user
  global stamina
  hitcrit = False
  if random.randrange(1, 101) > critchance[weapon]:
    dmgdealt = weapondmg[weapon]
  else:
    hitcrit = True
    dmgdealt = weapondmg[weapon] * critmult
  if hitcrit == False:
    print(f"You dealt {dmgdealt} damage to the {monster}! The monster now has {enemyhealth - dmgdealt} health. You have {stamina - 1} stamina remaining.")
  else:
    print(f"You landed a critical hit! You dealt {dmgdealt} to the {monster}! The enemy now has {enemyhealth - dmgdealt} health. You have {stamina - 1} stamina remaining.")
  stamina -= 1
  if stamina <= 0:
    print("You fell down in the middle of the fight due to exhaustion! Unluckily for you, this monster doesn't seem to care...")
    print("Game over!")
    print("Maybe watch your stamina better next time...")
    exit()
  return enemyhealth - dmgdealt

def rest():
  print(f"You go to sleep by the campfire. You wake up and feel refreshed. You now have {armordef[armor]} health and {maxstamina} stamina.")
  global health
  global stamina
  health = armordef[armor]
  stamina = maxstamina
  return

def life_lost(life, damage):
  if (life - damage) > 0:
    print(f"You took {damage} points of damage! You now have {life - damage} health.")
    return life - damage
  else:
    print(f"You took {damage} points of damage! You now have {life - damage} health.")
    print("Uh-oh, you died. Game over!")
    exit()

def move(direction, position):
  global stamina
  global health
  if direction == "back":
    stamina -= 2
    if stamina <= 0:
      print("You collapse from exhaustion before moving. Good thing there's no monsters nearby!")
      print("You wake up feeling woozy. You must have hit your head when you fell...")
      stamina = int(maxstamina/2)
      health = int(health/2)
      print(f"You now have {stamina} stamina and {health} health.")
      return position
    print(f"You move back. You now have {stamina} stamina.")
    return position.parent
  elif direction == "left":
    stamina -= 2
    if stamina <= 0:
      print("You collapse from exhaustion before moving. Good thing there's no monsters nearby!")
      print("You wake up feeling woozy. You must have hit your head when you fell...")
      stamina = int(maxstamina/2)
      health = int(health/2)
      print(f"You now have {stamina} stamina and {health} health.")
      return position
    print(f"You move left. You now have {stamina} stamina.")
    return position.left
  elif direction == "right":
    stamina -= 2
    if stamina <= 0:
      print("You collapse from exhaustion before moving. Good thing there's no monsters nearby!")
      print("You wake up feeling woozy. You must have hit your head when you fell...")
      stamina = int(maxstamina/2)
      health = int(health/2)
      print(f"You now have {stamina} stamina and {health} health.")
      return position
    print(f"You move right. You now have {stamina} stamina.")
    return position.right
  else:
    print("error: improper direction inputted")

def peek(direction, position):
  if direction == "left":
    if position.left.data == "monster" and position.left.alive == True and position.left.monstertype == 0:
      position.left.monstertype = monstertypes[random.randrange(1, 4)]
      position.left.monsterhealth = position.left.monstertype[1]
    elif position.left.data == "final boss" and position.left.alive == True:
      return "final boss"
    return position.left.data
  elif direction == "right":
    if position.right.data == "monster" and position.right.alive == True and position.right.monstertype == 0:
      position.right.monstertype = monstertypes[random.randrange(1, 4)]
      position.right.monsterhealth = position.right.monstertype[1]
    elif position.right.data == "final boss" and position.right.alive == True:
      return "final boss"
    return position.right.data

def takeinput(question, *allowed):
  #asks question to the user and keeps asking until they give an answer that is in allowed
  allowedstr = ""
  for i in allowed:
    allowedstr = allowedstr + i + ", "
  allowedstr = allowedstr[:len(allowedstr) - 2]
  userinput = input(question + f" Allowed answers are: {allowedstr}. ")
  while userinput.lower() not in allowed:
    print("Please follow the input format.")
    userinput = input(question + f" Allowed answers are: {allowedstr}. ")
  return userinput

def shopequip(equipment, price):
  global gold
  if gold >= price:
    gold -= price
    print(f"You bought the {equipment} for {price} gold.")
    print(f"You now have {gold} gold.")
    return 1
  else:
    print(f"Sorry, you do not have enough to buy this item. You have {gold} gold and {price} gold is required.")
    return 0

def shop():
  print("""Shop\t\tWeapons\t\t\tArmor
       
1.\t\tCrude Sword\t(15)\tLeather Suit\t(15)
2.\t\tPolished Sword\t(30)\tKevlar Vest\t(30)""")
  global weapon
  global armor
  global gold
  global maxstamina
  print(f"You have {gold} gold.")
  equipment = takeinput("What would you like to buy?", "crude sword", "polished sword", "leather suit", "kevlar vest", "exit").lower()
  if equipment == "exit":
    print("Hope you buy something next time!")
    return
  if equipment == "crude sword" or equipment == "leather suit":
    canequip = shopequip(equipment, 15)
    if canequip == 1:
      if equipment == "crude sword":
        weapon = "crude sword"
      else:
        armor = "leather suit"
        maxstamina = 30
  else:
    canequip = shopequip(equipment, 30)
    if canequip == 1:
      if equipment == "polished sword":
        weapon = "polished sword"
      else:
        armor = "kevlar vest"
        maxstamina = 40


root = createTree(9)
position = root
#make a copy so that when you move forward the entire tree is not overwritten - only the position changes

def campfire():
  decision = takeinput("What would you like to do at the campfire?", "rest", "shop", "move", "peek")
  if decision.lower() == "shop":
    shop()
  elif decision.lower() == "rest":
    rest()
  elif decision == "move":
    return "move"
  else:
    return "peek"
  return "stay"

def fightmonster():
  global position
  global health
  monster = 0
  if position.monstertype != 0:
    monster = position.monstertype
  else:
    monster = monstertypes[random.randrange(1, 4)]
    position.monsterhealth = monster[1]
    position.monstertype = monster
  if position.monstertype[0] != "Joe":
    print(f"You are fighting a/an {monster[0]}! This monster has {monster[1]} health and {monster[2]} attack.")
  else:
    print(f"You are fighting Joe! This monster has {monster[1]} health and {monster[2]} attack. His aura is almost enough to knock you out...")
  while True:
    global gold
    decision = takeinput("Would you like to fight the monster or heal?", "fight", "heal")
    if decision == "fight":
      position.monsterhealth = fight(position.monsterhealth, weapon, monster[0])
      if position.monsterhealth <= 0:
        golddropped = random.randrange(3, 6)
        print(f"You defeated the monster! The monster dropped {golddropped} gold. You now have {golddropped + gold} gold.")
        gold += golddropped
        position.alive = False
        return "move"
      else:
        variation = random.randrange(0, 3) - 1
        monsterdmgdealt = monster[2] + variation 
        print("The monster attacks you.")
        health = life_lost(health, monsterdmgdealt)
    else:
      lifehealed = int(3/10 * armordef[armor])
      if (health + lifehealed) >= armordef[armor]:
        print(f"You healed to full health. You now have {armordef[armor]} health.")
        health = armordef[armor]
      else:
        print(f"You healed for {lifehealed} health. You now have {health + lifehealed} health.")
        health += lifehealed
      variation = random.randrange(0, 3) - 1
      monsterdmgdealt = monster[2] + variation 
      print("The monster attacks you.")
      health = life_lost(health, monsterdmgdealt)
def peekprint(position):
  global health
  global stamina
  direction = takeinput("Which direction would you like to peek?", "left", "right").lower()
  peekdata = peek(direction, position)
  stamina -= 1
  print(f"You now have {stamina} stamina.")
  if stamina <= 0:
    print("You collapse from exhaustion before moving. Good thing there's no monsters nearby!")
    print("You wake up feeling woozy. You must have hit your head when you fell...")
    stamina = int(maxstamina/2)
    health = int(health/2)
    print(f"You now have {stamina} stamina and {health} health.")
    return position
  if peekdata == "checkpoint":
    print("You peek and see a campfire.")
  elif peekdata == "chest":
    print("You peek and see a chest.")
  elif peekdata == "monster":
    monster = 0
    if direction == "left":
      if position.left.alive == False:
        print("There is a dead monster ahead.")
      else:
        monster = position.left.monstertype
        print(monster)
        print(f"There is a {monster[0]} up ahead.")
    else:
      if position.right.alive == False:
        print("There is a dead monster ahead.")
      else:
        monster = position.right.monstertype
        print(monster)
        print(f"There is a {monster[0]} up ahead.")
  elif peekdata == "final boss":
    print("There is a strange evil up ahead. Surely what you seek is behind it?")
def moveandpeek():
  curaction = takeinput("What would you like to do?", "peek", "move")
  while curaction == "peek":
    peekprint(position)
    curaction = takeinput("What would you like to do?", "peek", "move")
  direction = takeinput("Which direction would you like to go?", "back", "left", "right")
  return direction

def finalboss():
  global health
  inputs = ["left", "right", "forward", "back"]
  totype = ""
  enemyhealth = 3
  for i in range(5):
    for i in range(20):
      totype = inputs[random.randrange(0, 4)]
      oldtime = time.time()
      playerinput = input(f"*{totype.upper()}*")
      timepassed = time.time() - oldtime
      if playerinput.lower() != totype:
        dmgtaken = int(timepassed) + 1
        health -= dmgtaken
        print(f"{dmgtaken} health lost from incorrect input, {health} health remaining.")
        if health < 0:
          time.sleep(2)
          print(f"'You thought that was it, huh? Well, I'm not done playing with you yet...'")
          finalboss()
          return
      elif timepassed > 3:
        dmgtaken = int(timepassed - 2) + 1
        health -= dmgtaken
        print(f"{dmgtaken} health lost from late input, {health} health remaining.")
        if health < 0:
          time.sleep(2)
          print(f"'You thought that was it, huh? Well, I'm not done playing with you yet...'")
          finalboss()
          return
    oldtime = time.time()
    playerinput = input(f"*ATTACK*")
    timepassed = time.time() - oldtime
    if timepassed > 2:
      print("Too slow...")
    else:
      print(f"You hit Joe! Joe now has {enemyhealth - 1} health!")
      enemyhealth -= 1
      if enemyhealth == 0:
        print("'You win...'")
        input("")
        print("'this time...'")
        input("")
        print("'...'")
        input("")
        print("you won!")
        exit()
  print("'See! You would never be able to defeat me. I'm just too strong! MWAHAHAHAHAHHAHAHAHA'")
  input("")
  print("'But I'll give you a second chance, since I'm so nice.'")
  finalboss()
  return
      
# —————— PROGRAM STARTS HERE ————— #
print("Welcome to The Lost Trinket!")
time.sleep(1)
print("You are a human called Bob.")
time.sleep(1)
print("There is a lost trinket that holds powerful powers.") 
time.sleep(1)
print("It is hidden in a dark cave guarded by many sneaky monsters.")
time.sleep(1)
print("You must obtain this trinket for your own good.")
time.sleep(1)
print("Entering the game...")
time.sleep(3)
print("Starting on base camp...")
root = createTree(9)
position = root
while True:
  if position.data == "checkpoint":
    action = campfire()
    while action == "stay":
      action = campfire()
    if action == "move":
      if position.parent == 0:
        direction = takeinput("Which direction would you like to go?", "left", "right")
        position = move(direction, position)
      else:
        direction = takeinput("Which direction would you like to go?", "back", "left", "right")
        position = move(direction, position)
    elif action == "peek":
      peekprint(position)
  elif position.data == "monster":
    if position.alive == True:
      action = fightmonster()
      if action == "move":
        curaction = takeinput("What would you like to do?", "peek", "move")
        while curaction == "peek":
          peekprint(position)
          curaction = takeinput("What would you like to do?", "peek", "move")
        direction = takeinput("Which direction would you like to go?", "back", "left", "right")
        position = move(direction, position)
    else:
      print("You see the remains of a dead monster.")
      direction = moveandpeek()
      position = move(direction, position)
  elif position.data == "chest":
    if position.alive == True:
      print("Lucky! You find a chest!")
      yesorno = takeinput("Do you want to open the chest?", "yes", "no")
      if yesorno == "yes":
        golddropped = random.randrange(5, 11)
        print(f"You got {golddropped} gold from the chest! You now have {gold + golddropped} gold.")
        gold += golddropped
        position.alive = False
      direction = moveandpeek()
      position = move(direction, position)
    else:
      print("You find a chest that you've already opened.")
      direction = moveandpeek()
      position = move(direction, position)
  elif position.data == "final boss":
    if position.alive == True:
      yesorno = takeinput("Are you sure you want to enter? This is the final boss, there's no going back.", "yes", "no")
      if yesorno == "yes":
        position.monstertype = monstertypes[4]
        position.monsterhealth = 100
        print("A strange melody comes out from the room, lulling you to sleep...")
        input("")
        print("You wake up and feel strangely refreshed.")
        input("")
        health = armordef[armor]
        stamina = maxstamina
        print(f"You have {health} health and {stamina} stamina.")
        input("")
        print("You hear an ominous voice from the darkness in front of you.")
        input("")
        print("'I've been waiting, you know. Waiting for a challenger to finally make it all the way here.'")
        input("")
        fightmonster()
        time.sleep(3)
        print("'OHOHOHO! You thought that was it, huh? You thought you could use your little tricks, your healing, you thought that was it!'")
        input("")
        print("'You thought you could defeat ME? The great and almighty JOE???'")
        input("")
        print("'That's not now it works, you know.'")
        input("")
        print("'The real boss battle begins now.'")
        input("")
        print("Joe will use his almighty powers to shift the power of gravity against you. You will have to move to the left or right.")
        input("")
        finalboss()
      else:
        position = position.parent


        
