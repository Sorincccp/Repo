import math
import os
import random
import re
import sys
import textwrap
import time
import colors
#Add "value" parameter to items
def getskill(player):
  fi=''
  fto=str(player.occupation)+'Skills'+'.txt'
  skills=open(fto,'r')
  x=skills.readlines()
  for i in range(0,len(x)-1):
    fi=fi+x[i]
  choices=[]
  it=re.finditer(r'\{[^\}]*\}',fi,re.S|re.I)
  for i  in it:
    a=eval(i.group(0))
    choices.append(a)
  for skill in choices:
    if int(s.level)==int(skill["unlocklvl"]):
      print("You have gained a new skill: ",colors.magenta(skill["name"]))
      player.skill.append(skill)


def useskill(player,skill,target):
  if skill != []:
    print(len(player.skill))
    print("Type the number corresponding to the skill you want to use \n")
    for skills in player.skill:
      print(player.skill.index(skills)+1,skills["name"],"\n")
    sk=int(input())
    skill=player.skill[sk-1]
    if (int(player.mp)-int(skill["mpcost"]))>0:
      crit=random.randint(0,10)
      if crit > 7:
        print("You use",skill["name"])
        target.hp=int(target.hp)-(int(skill["addeddmg"])+int(player.dmg))*2
        print(target.name," takes ",colors.cyan((int(skill["addeddmg"])+int(player.dmg))*2)," damage")
        if target.hp>0:
          print(target.name," HP left: ",colors.magenta(target.hp))
        else:
          print(target.name,"died")
        player.mp=int(player.mp)-int(skill["mpcost"])
        print(colors.cyan("MP"),colors.cyan(player.mp),colors.cyan("/"),colors.cyan(player.maxmp))
      else:
        print("You use",skill["name"])
        target.hp=int(target.hp)-(int(skill["addeddmg"])+int(player.dmg))
        print(target.name," takes ",colors.cyan((int(skill["addeddmg"])+int(player.dmg)))," damage")
        if target.hp>0:
          print(target.name," HP left: ",colors.magenta(target.hp))
        else:
          print(target.name,"died")
        player.mp=int(player.mp)-int(skill["mpcost"])
        print(colors.cyan("MP"),colors.cyan(player.mp),colors.cyan("/"),colors.cyan(player.maxmp))
    else:
      print("Not enough mana")
  else:
    print("You do not have any skills to use")

def useitem(item,inventory):
  names=[]
  x={}
  for i in range(0,len(inventory)):
   names.append(inventory[i]["name"])
  if str(item) in names:
    y=names.index(item)
    x=inventory[y]
    for key,value in x.items():
      if key=="type":
        itemtype="true"
        break
      else:
        itemtype="false"
    if itemtype=="true":
      print(itemtype)
      if x["type"]=="potion":
        for attr,value in s.__dict__.items():
          if str(attr)==str(x["effect"]):
            s.__dict__[attr]=int(s.__dict__[attr])+int(x["amount"])
            inventory[y]["quantity"]=int(inventory[y]["quantity"])-1
            if int(inventory[y]["quantity"]) <= 0 :
              inventory.pop(y)
        if s.hp > s.maxhp:
          s.hp=s.maxhp
        if s.mp > s.maxmp:
          s.mp=s.maxmp
        s.showstats()
        s.showinventory()
      else:
        print("This item cannot be used ")
    else:
      print("This item cannot be used")
  else:
    print("Something went wrong. You either don't have the item or you have incorrectly typed ot")
    s.showinventory()
def itemalterstats(item,player):
  if player.hp==player.maxhp:
    player.maxhp=int(player.maxhp)+int(item.hpi)
    player.hp=player.maxhp
  else:
    player.maxhp=int(player.maxhp)+int(item.hpi)
  if player.mp==player.maxmp:
    player.maxmp=int(player.maxmp)+int(item.mpi)
    player.mp=player.maxmp
  else:
    player.maxmp=int(player.maxmp)+int(item.mpi)
  player.dmg=int(player.dmg)+int(item.dmgi)
  return(player)

def equipitem(item,inventory):
  names=[]
  placeholder={}

  if s.itemslots!={}:
    for i in range(0,len(inventory)):
      names.append(inventory[i]["name"])
    if item in names:
      x=names.index(item)
      placeholder=inventory[x]
      inventory[x]=s.itemslots
      s.itemslots=placeholder
      s.itemslots["equiped"]="1"
      inventory[x]["equiped"]="0"
      s.maxhp=int(s.maxhp)-int(inventory[x]["hpi"])+int(s.itemslots["hpi"])
      if int(s.hp)>int(s.maxhp):
        s.hp=s.maxhp
      else:
        pass
      s.maxmp=int(s.maxmp)-int(inventory[x]["mpi"])+int(s.itemslots["mpi"])
      if int(s.mp)>int(s.maxmp):
        s.mp=s.maxmp
      else:
        pass
      s.dmg=int(s.dmg)-int(inventory[x]["dmgi"])+int(s.itemslots["dmgi"])
      print("You have equiped " , item)
      s.showstats()
    else:
      print("Something is off, please type the name of the item again")
    
  else:
    for i in range(0,len(inventory)):
      names.append(inventory[i]["name"])
    if item in names:
      x=names.index(item)
      s.itemslots=inventory[x]
     # print(s.itemslots)
      s.itemslots["equiped"]="1"
      s.maxhp=int(s.maxhp)+int(s.itemslots["hpi"])
      if int(s.hp)>int(s.maxhp):
        s.hp=s.maxhp
      else:
        pass
      s.maxmp=int(s.maxmp)+int(s.itemslots["mpi"])
      if int(s.mp)>int(s.maxmp):
        s.mp=s.maxmp
      else:
        pass
      s.dmg=int(s.dmg)+int(s.itemslots["dmgi"])
      print("You have equiped " , item)
      s.showstats()
      inventory.pop(x) 
      s.showinventory()  
    else:
      print("Something is off, please type the name of the item again")
  return(inventory)
def add_to_inventory(items,inventory):
  names=[]
  for i in range(0,len(inventory)):
    names.append(inventory[i]["name"])
  for j in range(0,len(items)):
    if items[j]["name"] in names:
      x=names.index(items[j]["name"])
      inventory[x]["quantity"]=int(inventory[x]["quantity"])+int(items[j]["quantity"])
    else:
      inventory.append(items[j])
  return(inventory)

def create(file):
    fi=''
    fit=open(file,'r')
    x=fit.readlines()
    for i in range(0,len(x)-1):
      fi=fi+x[i]
    choices=[]
    it=re.finditer(r'\{[^\}]*\}',fi,re.S|re.I)
    for i  in it:
        a=eval(i.group(0))
        choices.append(a)
    x=random.choice(choices)
    return(x)
class player:
  def __init__(self,name,maxhp,maxmp,ocupation):
    self.name=name
    self.maxhp=hp
    self.hp=self.maxhp
    self.maxmp=mp
    self.mp=self.maxmp    
    self.occupation=occupation
    self.xp=0
    self.dmg=10
    self.level=1
    self.inventory=[{'name':'Gold','quantity':'10'}]
    self.itemslots={}
    self.skill=[]
  def showinventory(self):
    print("Your inventory is :")
    for v in range(len(self.inventory)):
      print(self.inventory[v]["quantity"],self.inventory[v]["name"])
  def showstats(self):
    for attr,value in self.__dict__.items():
      if attr=="inventory":
        self.showinventory()
      elif attr == "skill":
        print(colors.cyan("Your skills are \n"))
        for i in range(0,len(self.skill)):
          for key,val in self.skill[i].items():
            print(colors.magenta(key),":",val)
      elif attr=="itemslots":
        print(colors.yellow("You currently have equiped "))
        for key,val in self.itemslots.items():
          print(key,":",val)
      else:
        print(attr,":",value)

  
  def sell(self,inventory):


    gold=0
    for m in range (0 , len(inventory)):
      print(m+1," ",inventory[m]["quantity"]," " ,inventory[m]["name"])
    print("Select the item you want to sell ")
    x=int(input())
    #Add restriction when x > len(inventory)
    print(" You want to sell " , inventory[x-1]["name"])
    print(" Please enter the amount")
    y=int(input())
    print("You want to sell", y," ",inventory[x-1]["name"])
    for key,value in inventory[x-1].items():
      if key=="value":
        selleable="true"
        break
      else:
        selleable="false"
    if selleable=="true" :
      if y>int(inventory[x-1]["quantity"]):
        print("You do not have that amount ")
      elif int(inventory[x-1]["quantity"])-y==0:
        gold=int(inventory[x-1]["value"])*int(inventory[x-1]["quantity"])
        inventory.pop(x-1)
        for t in range (0,len(inventory)):
          if inventory[t]["name"]=="Gold":
            inventory[t]["quantity"]=int(inventory[t]["quantity"])+int(gold)
      else:
        gold=int(inventory[x-1]["value"])*y
        inventory[x-1]["quantity"]=int(inventory[x-1]["quantity"])-y
        for t in range (0,len(inventory)):
          if inventory[t]["name"]=="Gold":
            inventory[t]["quantity"]=int(inventory[t]["quantity"])+int(gold)
    else:
      print("Item cannot be sold")

    self.showinventory()

class item:
    def __init__(self):
      x=create("Items.txt")
      self.name=x["name"]
      self.hpi=x["hpi"]
      self.mpi=x["mpi"]
      self.dmgi=x["dmgi"]
      self.equiped=x["equiped"]
      self.rarity=x["rarity"]
    def showstats(self):
      if self.rarity=="Rare":
        print(colors.cyan(self.name),"\n","HP + ",self.hpi,"\n","MP + ",self.mpi,"\n","Damage + ",self.dmgi,"\n","Rarity: ",self.rarity)
      elif self.rarity=="Common":
        print(colors.yellow(self.name),"\n","HP + ",self.hpi,"\n","MP + ",self.mpi,"\n","Damage + ",self.dmgi,"\n","Rarity: ",self.rarity) 
      elif self.rarity=="Uncommon":
        print(colors.green(self.name),"\n","HP + ",self.hpi,"\n","MP + ",self.mpi,"\n","Damage + ",self.dmgi,"\n","Rarity: ",self.rarity) 
      elif self.rarity=="Epic":
        print(colors.magenta(self.name),"\n","HP + ",self.hpi,"\n","MP + ",self.mpi,"\n","Damage + ",self.dmgi,"\n","Rarity: ",self.rarity) 
      else:
        print(colors.orange(self.name),"\n","HP + ",self.hpi,"\n","MP + ",self.mpi,"\n","Damage + ",self.dmgi,"\n","Rarity: ",self.rarity) 
class mob:
    def __init__(self):
      x=create('Creeps.txt')
      self.name=x["name"]
      self.hp=x["hp"]
      self.dmg=x["damage"]
      self.xpdrop=x["xpdrop"]
      self.drop=x["drop"]
    def showstats(self):
      for attr,value in self.__dict__.items():
        print(attr,":",value)
def drop():
    gold=create('Gold.txt')
    gold["quantity"]=random.randint(2,25)
    l=[]
    l.append(gold)
    itemchance=random.randint(0,100)
    miscchance=random.randint(25,100)
    miscq=random.randint(1,2)
    
    if itemchance>=90:
      dp=create('Items.txt')
      dp["quantity"]=1
      l.append(dp)
    else:
      pass
    if miscchance>=75:
      msc=create('Misc.txt')
      msc["quantity"]=miscq
      l.append(msc)
    else:
      pass
      
    return(l)

def attack(attacker,victim):
    crit=random.randint(0,10)
    if crit > 7:
      victim.hp=int(victim.hp)-int(attacker.dmg)*2
      print(victim.name," takes ",colors.cyan(int(attacker.dmg)*2)," damage")
    else:
      victim.hp=int(victim.hp)-int(attacker.dmg)
      print(victim.name," takes ",colors.cyan(int(attacker.dmg))," damage")

def xpgain(player,creep):
  player.xp=int(player.xp)+int(creep.xpdrop)  
  if int(player.xp)>=int(levelcap[int(player.level)-1]):  
    levelcap.append(int(levelcap[int(player.level)-1])+int(player.level)*15)     
    player.level=int(player.level)+1
    print("You have gained a level","You are now a level ",player.level," ",player.occupation)
    player.maxhp=int(player.maxhp)+15*int(player.level)
    player.hp=player.maxhp
    player.maxmp=int(player.maxmp)+15*int(player.level)
    player.mp=player.maxmp
    player.dmg=int(player.dmg)+3*int(player.level)
    print("XP: ",colors.cyan(player.xp),colors.cyan("/"),colors.cyan(levelcap[int(player.level)-1]) )  
    getskill(player)
    player.showstats()
  else:
    print("XP: ",colors.cyan(player.xp),colors.cyan("/"),colors.cyan(levelcap[int(player.level)-1]) ) 

def fight(creep,player):
  creep=mob()
  print("You see a ",creep.name," in the distance",)
  creep.showstats()
  print("Do you attack? y/n")
  ft=input()
  if ft=="y":
    while (int(player.hp) | int(creep.hp) )> 0 :
      action=input(colors.yellow("Choose your next action \n Press 'e' to equip an item \n Press 'u' to use an item \n Press 'a' to attack \n Press 's' to use skill \n"))
      if action=="a":
        time.sleep(0.2)
        attack(player,creep)
        if int(creep.hp)>0:
          time.sleep(0.2)
          print(creep.name," HP left: ",colors.magenta(creep.hp))
        else:
          break
      elif action=="u":
        player.showinventory()
        item=input("Choose the item you want to use")
        useitem(item,player.inventory)
      elif action=="s":
        useskill(player,player.skill,creep)
      attack(creep,player)
      time.sleep(0.2)
      print(player.name ," HP left: ",colors.green(player.hp),colors.green("/"),colors.green(player.maxhp))
    if int(player.hp) >= 1:
      time.sleep(0.2)
      print("Victory!!","\n","You have gained ",creep.xpdrop," XP") 
      xpgain(player,creep)
      specchance=random.randint(25,100)
      specdrop={"name":"","quantity":"","value":""}
      specdrop["name"]=creep.drop
      specdrop["quantity"]=random.randint(1,5)
      specdrop["value"]="5"
      drp=[]
      drp=drop()
      if int(specchance) >= 50:
       
        drp.append(specdrop)
      
      add_to_inventory(drp,player.inventory)
      for t in range(0,len(drp)):

        if int(drp[t]["quantity"]) == 1:

          print(colors.yellow("Your loot : "),drp[t]["name"])
        else:
          print(colors.yellow("Your loot : "),drp[t]["quantity"],drp[t]["name"])
      print("Your inventory is :")
      for v in range(len(player.inventory)):
            print(player.inventory[v]["quantity"],player.inventory[v]["name"])

        
      
    
    else:
      print("You have died")
  else:
    print("You change your path to avoid ",creep.name)



temp={}
temp1=[]
levelcap=["10"]
occup=["Fighter","Mage"]
name=input("How should this brave warrior be called? ")
i=int(input("Select Occupation: 1 Fighter  2 Mage"))
occupation=occup[i-1]
mp=25*i
hp=(300/i)+50
s=player(name,hp,mp,occupation)

shit=item()

eq=""
s.showstats()
print("In your adventure you find ")
shit.showstats()
print("Would you like to equip? y/n")
eq=input()
if eq=="y":
  itemalterstats(shit,s)
  s.itemslots["name"]=shit.name
  s.itemslots["hpi"]=shit.hpi
  s.itemslots["mpi"]=shit.mpi
  s.itemslots["dmgi"]=shit.dmgi
  s.itemslots["equiped"]="1"
  s.itemslots["rarity"]=shit.rarity
  s.itemslots["quantity"]="1"
  #print(s.itemslots)
  print("You have equiped your ",shit.name)
  s.showstats()
else:
  print("The item has been stored in your inventory")
  
  temp["name"]=shit.name
  temp["hpi"]=shit.hpi
  temp["mpi"]=shit.mpi
  temp["dmgi"]=shit.dmgi
  temp["equiped"]="0"
  temp["rarity"]=shit.rarity
  temp["quantity"]="1"
  temp1.append(temp)
  add_to_inventory(temp1,s.inventory)
  s.showinventory()
creep=mob()

fight(creep,s)
cont=input(colors.cyan("Choose your next action \n Press 'e' to equip an item \n Press 'u' to use an item \n Press 'c' to continue your killing spree \n Type showstats to see stats \n Type 'exit' to end the game \n Type sell to sell items \n")).lower()
while cont !="exit" :
  if cont=="e":
    s.showinventory
    item=str(input("Type the name of the item you want to equip"))
    equipitem(item,s.inventory)

    cont=input(colors.cyan("Choose your next action \n Press 'e' to equip an item \n Press 'u' to use an item \n Press 'c' to continue your killing spree \n Type showstats to see stats \n Type 'exit' to end the game \n Type sell to sell items \n")).lower()

  elif cont=="c":
    fight(creep,s)
    cont=input(colors.cyan("Choose your next action \n Press 'e' to equip an item \n Press 'u' to use an item \n Press 'c' to continue your killing spree \n Type showstats to see stats \n Type 'exit' to end the game \n Type sell to sell items \n")).lower()
  
  elif cont=="u":
    item=str(input("Type the name of the item you want to use"))
    useitem(item,s.inventory)
    cont=input(colors.cyan("Choose your next action \n Press 'e' to equip an item \n Press 'u' to use an item \n Press 'c' to continue your killing spree \n Type showstats to see stats \n Type 'exit' to end the game \n Type sell to sell items \n")).lower()
  elif cont=="showstats":
    s.showstats()
    
    cont=input(colors.cyan("Choose your next action \n Press 'e' to equip an item \n Press 'u' to use an item \n Press 'c' to continue your killing spree \n Type showstats to see stats \n Type 'exit' to end the game \n Type sell to sell items \n")).lower()
  elif cont=="sell":
    s.sell(s.inventory)
    cont=input(colors.cyan("Choose your next action \n Press 'e' to equip an item \n Press 'u' to use an item \n Press 'c' to continue your killing spree \n Type showstats to see stats \n Type 'exit' to end the game \n Type sell to sell items \n")).lower()
  else :   
    cont=input(colors.cyan("Incorrect choice. Choose your next action \n Press 'e' to equip an item \n Press 'u' to use an item \n Press 'c' to continue your killing spree \n Type showstats to see stats \n Type 'exit' to end the game \n Type sell to sell items \n")).lower()
