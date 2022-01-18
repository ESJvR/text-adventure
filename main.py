import random
import math
class Room:
    def __init__(self):
        self.content=random.random()
    def link(self,u,d,l,r):
        self.up=u
        self.down=d
        self.left=l
        self.right=r

def createMap(x,y):
    MapUnlinked=[]
    for i in range(y):
        MapUnlinked.append([Room() for o in range(x)])
    height,width=len(MapUnlinked),len(MapUnlinked[0])
    for y in range(height):
        for x in range(width):
            MapUnlinked[y][x].link(MapUnlinked[(y+1)%height][x],MapUnlinked[(y-1+height)%height][x],MapUnlinked[y][(x-1+width)%width],MapUnlinked[y][(x+1)%width])
    MapUnlinked[0][0].content=-1
    return MapUnlinked[0][0]

def BorderLine():
    print("-------------------------------------------------------")

def drawHelp():
    print("Here a list of the available commands:\n")
    print("  !inv -> shows your inventory")
    print("  !move <direction> -> you move to the room in the given direction")
    print("    available directions are: up, down, left, right")
    print("  !pick -> collect all items in the room")
    #print("  !stairs -> use the stairs to go to the next floor")
    print("  !fight -> use your current power to attack the local enemy")
    print("  !stats -> shows your stats")
    print("  !use <itemName> -> use an item with given name")
    print("    you can search for the name in the inventory")

def drawInv(inventory):
    if len(inventory)==0: print("Your inventory is empty, go explore some rooms, before you check your bag."); return
    print("Here you can see all your current belongings:")
    for i in inventory:
        print("  "+i.type+": "+i.name+", with a strength of "+str(i.power))

def drawStats(Player,Enemy):
    print("let's take a look at you\n")
    print("Your name is: "+Player.name)
    print("You currently have "+ str(Player.Health)+ " HP")
    print("You have "+ str(Player.Damage)+ " damage to deal")
    print("You carry "+ str(Player.Gold)+ " Gold ounces with you")
    if(not Enemy is None):
        print("")
        print("There is also an Enemy in your room!")
        print("It is a "+Enemy.name)
        print("It has "+str(Enemy.Health)+" HP")
        print("It deals "+str(Enemy.Damage)+ " damage")
    print("") 

def PickOne(a):
    index=math.floor(random.random()*len(a))
    return a[index]

def ItemNameGenerator(type,power):
    name=""
    weaponNames=["Dagger","Bow","Sword","Pike","Staff"]
    weaponEpicAttributes=["mystic","shiny","golden","sharp"]
    weaponLegendaryAttributes=["deadly","legendary","magnificent","enhanced","reinforced"]
    potionNames=["Health Potion","Potion of Regeneration","Life Potion","Bandages"]
    potionAttributes=["big", "regenerating","tasty","red","pink"]
    treasureNames=["Coins","Treasure Map","Monocle","Gem"]
    treasureAttributes=["ancient","valuable","golden","famous"]
    if type=="weapon":
        if power>=50&power<75:
            name+=PickOne(weaponEpicAttributes)
            name+=" "
        elif power>=75:
            name+=PickOne(weaponLegendaryAttributes)
            name+=" "
        name+=PickOne(weaponNames)
    elif type=="potion":
        if power>=60:
            name+=PickOne(potionAttributes)
            name+=" "
        name+=PickOne(potionNames)
    elif type=="treasure":
        if power>=60:
            name+=PickOne(treasureAttributes)
            name+=" "
        name+=PickOne(treasureNames)
    return name

def loadRoom(Map, dir):
    placedItem=None
    Enemy=None
    newRoom=None
    if dir=="up":
        newRoom=Map.up
    elif dir=="down":
        newRoom=Map.down
    elif dir=="left":
        newRoom=Map.left
    else:
        newRoom=Map.right
    #print("DEBUG: content val is",newRoom.content)
    content=newRoom.content
    if(content==-1):
        print("The room is empty.\n")
        print("Could it be that you were here before?")
    if((content>=0)&(content<0.2)):
        print("You walk into a dark room, you await some kind of danger,")
        print("but to your delight, the room is indeed empty.")
        print("You can use some items or just go into the next room.\n")
        newRoom.content=-1
    if((content>=0.2)&(content<0.65)):
        print("You enter the room and on a podest next to you is a mysterious item, with some sunrays burning on it through a crack in the ceiling")
        typ=PickOne(["potion","weapon","treasure"])
        power=math.ceil(random.random()*100)
        name=ItemNameGenerator(typ,power)
        #print("DEBUG:",name,typ,power)
        placedItem=Item(name,power,typ)
        print("As you get closer you can clearly identify it as a "+typ)
        print("\nYou can now pick it up or leave the room")
        print("yet an ancient inscribe on the podest says, that it will vanish as you leave the room")
        newRoom.content=-1
    if(content>=0.65):
        print("You enter the room and a dark mist fills the air..\n")
        Enemy=Creature(PickOne(["bat","rat","goblin"]))
        print("You look around and as the fog starts to vanish you can clearly see the outline of a "+Enemy.name+"..")
        print("You'll need to fight it to get along.")
        newRoom.content=-1
    #print("DEBUG: content val is",newRoom.content)
    return newRoom,placedItem,Enemy

        
    return newRoom,Item,Enemy

def UseItem(name,Inv,Player):
    #print("DEBUG: len of Inv",len(Inv),Inv)
    Item=None
    for i in range(len(Inv)):
        if Inv[i].name==name:
            Item=Inv[i]
            Inv.pop(i)
            break
    if Item==None:
        print("There is no item with the name:",name+"\n")
        return
    else:
        if Item.type=="potion":
            Player.Health+=Item.power
        if Item.type=="weapon":
            Player.Damage+=Item.power
        if Item.type=="treasure":
            print("You get out the "+Item.name)
            print("it looks really good, you shouldn't lose it")
            print("\nyou put it back into your bag")
            Inv.append(Item)
        

class Creature:
    Health=69
    Damage=0
    Gold=0
    name="wtf"
    #Health, Damage, Gold,name
    def __init__(self,type):
        #print("DEBUG: creating creature of type: "+ type)
        match(type):
            case "player":
                self.Health=100
                self.Damage=5
                self.Gold=0
                self.name="kekw"
            case "bat":
                self.Health=20
                self.Damage=8
                self.Gold=4
                self.name="bat"
            case "rat":
                self.Health=16
                self.Damage=8
                self.Gold=4
                self.name="rat"
            case "goblin":
                self.Health=30
                self.Damage=3
                self.Gold=20
                self.name="goblin"
    def ResetDamage(self):
        if(self.Damage!=5):
            print("Oh no, you weapon broke in combat, you'll have to equip a new one.")
        self.Damage=5
class Item:
    #Name, Powerlevel, Use
    def __init__(self,name,p,t):
        #print("DEBUG: creating Item",name,p,t)
        self.name=name
        self.power=p
        self.type=t
Player=Creature("player")
Enemy=None
PlacedItem=None
Inventory=[]
Map=createMap(8,8)
print("Welcome to a cheap copy of Zorg, the great great grandfather of dwarf fortress, the only game you shall play!")
Player.name=input("But before we begin, we need to settle on a name for our hero. What shall we call you?\n")
BorderLine()
print("Great",Player.name,"! Now you can start your journey.")
print("\nYour adventure begins in a deep cavern. Stay alarmed at all times and be ready to fight for your life, only the true heroes will return rich and with glory.")
print("Type !help for a list of commands\n")
while(Player.Health>0):
    command=input("What are you doing now?\n")
    commandKey=command.split(" ")[0]
    BorderLine()
    match(commandKey):
        case "!help":
            drawHelp()
        case "!inv":
            drawInv(Inventory)
        case "!move":
            if(Enemy is None):
                print("You move into the next room\n")
                dir=command.split(" ")[1]
                Map,PlacedItem,Enemy=loadRoom(Map,dir)
            else:
                print("There's still someone to fight in the room, you can't leave now.\n")
        case "!pick":
            if PlacedItem is None:
                print("Unfortunately there is no item you could pick up")
            else:
                print("You pick up the "+PlacedItem.type+" lying in the room.")
                Inventory.append(PlacedItem)
                PlacedItem=None
        case "!fight":
            print("You engage in combat!")
            while((Enemy is not None)&(Player.Health>0)):
                print("")
                Enemy.Health-=Player.Damage
                print("You strike your opponent for "+str(Player.Damage)+" damage, the "+Enemy.name+" is now on "+str(Enemy.Health)+" HP.")
                Player.Health-=Enemy.Damage
                print("You got struck for "+str(Enemy.Damage)+" damage and are now on "+str(Player.Health)+" HP.")
                if(Enemy.Health<=0):
                    Player.Gold+=Enemy.Gold
                    Enemy=None
                    Player.ResetDamage()
            if Player.Health>0:
                print("You beat the opponent, congrats!\n")
        case "!stats":
            drawStats(Player,Enemy)
        case "!use":
            UseItem(command[5:],Inventory,Player)
        case x:
            print("You shout \""+command+"\" into the cavern...\n")
            print("Nothing seems to happen..")
            print("Maybe the lonelyness starts to drive you insane,")
            print("Type !help for help")
print("Unfortunately your HP dropped to 0, this means game over")
print("But it had a purpose!")
print("You had "+Player.Gold+" Gold with you")
totalWealth=sum(map(lambda x: x.power,list(filter(lambda x: x.type=="treasure",Inventory))))
print("Plus, your treasures had a total wealth of "+totalWealth)
print("That makes a total of "+str(Player.Gold+totalWealth)+" in gold coins, that you earned")
print("It was a good game!")
