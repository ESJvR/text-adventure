from asyncio import create_subprocess_exec
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

def drawHelp():
    print("Here a list of the available commands:\n")
    print("  !move <direction> -> you move to the room in the given direction")
    print("    available directions are: up, down, left, right")
    print("  !pick -> collect all items in the room")
    print("  !fight -> use your current power to attack the local enemy")
    print("  !use <itemName> -> use an item with given name")

def PickOne(a):
    index=math.floor(random.random()*len(a))
    return a[index]

def ItemNameGenerator(type,power):
    name=""
    weaponNames=["Sword","Staff"]
    weaponEpicAttributes=["mystic","shiny"]
    weaponLegendaryAttributes=["deadly","legendary"]
    potionNames=["Health Potion"]
    potionAttributes=["red","pink"]

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
        typ=PickOne(["potion","weapon"])
        power=math.ceil(random.random()*100)
        name=ItemNameGenerator(typ,power)
        placedItem=Item(name,power,typ)
        print("As you get closer you can clearly identify it as a "+typ)
        print("On closer inspection its actually a "+name)
        print("\nYou can now pick it up or leave the room")
        print("yet an ancient inscribe on the podest says, that it will vanish as you leave the room")
        newRoom.content=-1
    if(content>=0.65):
        print("You enter the room and a dark mist fills the air..\n")
        Enemy=Creature(PickOne(["goblin","GIGACHAD"]))
        print("You look around and as the fog starts to sh you can clearly see the outline of a "+Enemy.name+"..")
        print("You'll need to fight it to get along.")
        newRoom.content=-1
    return newRoom,placedItem,Enemy

def UseItem(name,Inv,Player):
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
            print("You used the potion")
        if Item.type=="weapon":
            Player.Damage+=Item.power
            print("You took your weapon into your own hands")
       
class Creature:
    Health=100
    Damage=0
    name="wtf"
    def __init__(self,type):
        match(type):
            case "player":
                self.Health=100
                self.Damage=5
                self.name="Dio"
            case "goblin":
                self.Health=30
                self.Damage=3
                self.name="goblin"
            case "GIGACHAD":
                self.Health=690
                self.Damage=420
                self.name="GIGACHAD"
                
class Item:
    def __init__(self,name,p,t):
        self.name=name
        self.power=p
        self.type=t
Player=Creature("player")
Enemy=None
PlacedItem=None
Inventory=[]
Map=createMap(8,8)
print("\nYour adventure begins in a deep cavern. Stay alarmed at all times and be ready to fight for your life, only the true heroes will return rich and with glory.")
print("Type !help for a list of commands\n")
while(Player.Health>0):
    command=input("What are you doing now?\n")
    commandKey=command.split(" ")[0]
    print("-------------------------------------------------------")
    match(commandKey):
        case "!help":
            drawHelp()
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
            if Enemy is None:
                print("Are you already hallucinating? There is noone there !")
            else: print("You menacingly approach the enemy ! Dio's Theme starts playing...")
            while((Enemy is not None)&(Player.Health>0)):
                print("")
                Enemy.Health-=Player.Damage
                print("You strike your opponent for "+str(Player.Damage)+" damage, the "+Enemy.name+" is now on "+str(Enemy.Health)+" HP.")
                Player.Health-=Enemy.Damage
                print("You got struck for "+str(Enemy.Damage)+" damage and are now on "+str(Player.Health)+" HP.")
                if(Enemy.Health<=0):
                    Enemy=None
                    print("You destroyed the opponent, congrats! Dio's Theme stops playing... \n")
        case "!use":
            UseItem(command[5:],Inventory,Player)
print("Unfortunately your HP dropped to 0, this means game over")
