import sqlite3, sys, colorama, os, time
from cryptography.fernet import Fernet
from getpass import getpass
from colorama import Fore, Style

colorama.init(autoreset=True)

encode = "utf-8"
#function for turning strings into bytes, i think u can understand this well 
def byte(string, encode=encode):
     return bytes(string, encode)
#function for decrpything strings
def decrypt(string, key):
     return Fernet(key).decrypt(string).decode(encode)
#function for encrypting strings
def encrypt(string, key):
     return Fernet(key).encrypt(byte(string))




# database create
### \/ RUN THIS ONCE \/###

"""conn = sqlite3.connect("Passwordkeeper.db")
bot = conn.cursor()
bot.execute("CREATE TABLE IF NOT EXISTS passwordkeeper (site TEXT, user TEXT, password TEXT, key TEXT)")
#insert your admin items here the important one is the password,
# the other ones won't realy be used so just do like admin admin yourpass
key = Fernet.generate_key()
#insert here your password between the two ""

yourpassword = "123123"

insertform = (
     encrypt("admin", key),
     encrypt("admin", key),
     encrypt(yourpassword, key),
     key
)
bot.execute("INSERT INTO passwordkeeper VALUES(?,?,?,?)", insertform)
conn.commit()
conn.close()"""
### /\ RUN THIS ONCE ONLY  /\ ###




#function to get user inputs
def getinputs(numi=3):
          site = input(" site > ")
          user = input(" user > ")
          password = input(" pass > ")
          if numi == 5:
               param = input(" parameter to change > ")
               newparam = input(" new value for param > ")
               return [site, user, password, param, newparam]
          else: return [site, user, password]

#i created this class to it extract the item from database for me and to be able to not be always doing all this code :D
class getdb():
     def __init__(self):
          pass
     #opens database and gets all the users and everything except the admin ones
     #this returns a list with lists each list inside the main list has the site, user, pass in this order
     def list(self):
          llist = []
          conn = sqlite3.connect("Passwordkeeper.db")
          bot = conn.cursor()
          #get those things from db
          bot.execute("""SELECT * FROM passwordkeeper""")
          db = bot.fetchall()
          for row in db:
               ensite, enuser, enpassword, enkey = (row[0], row[1], row[2], row[3])
               site, user, password = (decrypt(ensite, enkey), decrypt(enuser, enkey), decrypt(enpassword,enkey))
               llist.append([site,user,password])
          #remove the admin credentials from the list so it doesnt show up in the console
          #print("antes", llist)
          llist.remove([llist[0][0], llist[0][1], llist[0][2]])
          conn.close()
          #print("depois", llist)
          return llist
     #this function gets all the data
     def all(self):
          conn = sqlite3.connect("Passwordkeeper.db")
          bot = conn.cursor()
          bot.execute("SELECT * FROM passwordkeeper")
          db = bot.fetchall()
          conn.close()
          return db

#shows all accounts to console 
def show():
     llist = getdb().list()
     llist.append(["NONE", "NONE", "NONE"])
     llist.insert(0, ["site/platform", "user", "password"])
     lastsite = ""
     #spaces algorythm so everything is lined up
     biggestsite, biggestuser = " ", " "
     sitegroup, usergroup = [], []
     #define wich is the biggest word for each catagory
     for y in llist:
          if len(y[0]) > len(biggestsite): biggestsite = y[0]
          if len(y[1]) > len(biggestuser): biggestuser = y[1]
     #define wich words need to get extra spaces to be the size of the others
     for x in llist:
          if len(biggestsite) > len(x[0]): sitegroup.append(x[0])
          if len(biggestuser) > len(x[1]): usergroup.append(x[1])
     #check if group is empty and if not add spaces to them 
     tuple = [sitegroup, usergroup]
     #novas listas com users nomes e passes sem espacos para verificao da sua presenca na lista para saber se e preciso trocar ou n
     newsitegroup, newusergroup = [], []
     for site, user in zip(sitegroup, usergroup):
          newsitegroup.append(site.strip())
          newusergroup.append(user.strip())
     #print all the accounts
     removed_count = 0

     for x, list in enumerate(tuple[0]):
          y = x + removed_count
          nextsite, nextuser, nextpass = llist[x][0], llist[x][1], llist[x][2]
          while len(nextsite) < len(biggestsite):
               nextsite += " "
          while len(nextuser) < len(biggestuser):
               nextuser += " "
          if nextsite.strip() == "site/platform": print(f"\n{Fore.GREEN}    {Fore.CYAN} {nextsite}  --  {Style.RESET_ALL}{nextuser}  --  {Fore.RED}{nextpass}")
          else:print(f"{Fore.GREEN}--> {Fore.CYAN} {nextsite}  --  {Style.RESET_ALL}{nextuser}  --  {Fore.RED}{nextpass}")
          if not lastsite == nextsite:
               print("\r")
          lastsite = nextsite

#adds new account
def add():
     data = getinputs()
     site, user, password = data[0], data[1], data[2]
     key = Fernet.generate_key()
     conn = sqlite3.connect("Passwordkeeper.db")
     bot = conn.cursor()
     insertform = (encrypt(site, key),encrypt(user, key),encrypt(password, key),key)
     bot.execute("INSERT INTO passwordkeeper VALUES(?,?,?,?)", insertform)
     conn.commit()
     conn.close()

#delete account
def delete():
     data = getinputs()
     site, user, password = data[0], data[1], data[2]
     print(" Are you sure you want to delete?")
     os.system("pause")
     conn = sqlite3.connect("Passwordkeeper.db")
     bot = conn.cursor()
     bot.execute("""SELECT * FROM passwordkeeper""")
     db = bot.fetchall()
     for row in db:
          if (decrypt(row[0], row[3]) == site) and (decrypt(row[1], row[3]) == user) and (decrypt(row[2], row[3]) == password):
               deleteform = (row[0],row[1],row[2])
               bot.execute("DELETE FROM passwordkeeper WHERE site=? AND user=? AND password=?", deleteform)
               conn.commit()
     conn.close()
     print(f"{Fore.GREEN}   Deleted Successfully{Style.RESET_ALL}")
     show()

#change any account with the format --    site, user, pass,  newsite, newsitename (this is example)
# 1, 2,3 param is to make possible for the program know what to change and then the 4 is the param that u want to modify and then the 5 is the new value for that parameter
def change():
     data = getinputs(5)
     site, user, password, param, newparam = data[0], data[1], data[2], data[3], data[4]
     conn = sqlite3.connect("Passwordkeeper.db")
     bot = conn.cursor()
     bot.execute("""SELECT * FROM passwordkeeper""")
     db = bot.fetchall()
     for row in db:
          if (decrypt(row[0], row[3]) == site) and (decrypt(row[1], row[3]) == user) and (decrypt(row[2], row[3]) == password):
               if param == "site":
                    newsite = newparam, newuser, newpassword = (encrypt(newparam, row[3]), row[1], row[2])
               elif param == "user":
                    newsite, newuser, newpassword = (row[0], encrypt(newparam, row[3]), row[2])
               elif param == "pass":
                    newsite, newuser, newpassword = (row[0], row[1], encrypt(newparam, row[3]))
               changeform = (newsite, newuser, newpassword, row[0], row[1], row[2])
               bot.execute("UPDATE passwordkeeper SET site=?, user=?, password=? WHERE site=? AND user=? AND password=?", changeform)
               conn.commit()
     conn.close()
     show()


### \/ NOT DONE \/ ###
#for big lists i decided to me making this function to be possible to search for anything
#still not done but is the next thing i will be working on 
def search(param, searchparam):
     conn = sqlite3.connect("Passwordkeeper.db")
     bot = conn.cursor()
     bot.execute("SELECT * FROM passwordkeeper")
     db = bot.fetchall()
     print("not done")
     pass
     passw = decrypt(bot.fetchone()[0], b"")
     for row in db:
          if (decrypt(row[0], row[3]) != passw):
               for column in range(3):
                    if row[3].decode(encode) == row[column]:
                         print()
     bot.execute(f"SELECT * FROM passwordkeeper WHERE {param}=?", (searchparam))
     db = bot.fetchall()
     print(db)
     conn.close()
### /\ NOT DONE /\ ###

#just a login to enter the program
def login():
     db = getdb().all()
     for row in db:
          if getpass(f" pass > ") != decrypt(row[2], row[3]):
               print(f"{Fore.RED}CRITICAL ERROR\nBETTER COME BACK LATER")
               time.sleep(1)
               os.system("TASKKILL /IM cmd.exe")
               return False
               break
          else:
               return True
               break

#clear console so the colors work properly wich is weird asfuck lol
os.system("cls")
first_time = True
#main loop
if login():     
     while True:
          if first_time:
               print(f"\n  Command:      {Fore.LIGHTBLACK_EX}(type help to see the available commands)") 
               first_time = False
          else: print(f"  Command:")
          inputs = input(f"\n {Fore.YELLOW}   -->{Style.RESET_ALL} ").lower()
          if inputs in ["help", "hel", "he", "h"]:
               print(f"""
          {Fore.LIGHTBLACK_EX}help       --> Shows this{Style.RESET_ALL}
          {Fore.CYAN}show{Style.RESET_ALL}       --> {Fore.CYAN}Shows{Style.RESET_ALL} all the stored information
          {Fore.GREEN}add{Style.RESET_ALL}        --> {Fore.GREEN}Adds{Style.RESET_ALL} a new item to the database
          {Fore.RED}delete{Style.RESET_ALL}     --> {Fore.RED}Delete's{Style.RESET_ALL} a item from the database
          change     --> Changes a value from the database
          search     --> Searches a value in database
          {Fore.LIGHTBLACK_EX}close/quit --> Closes the program{Style.RESET_ALL}
          {Fore.LIGHTBLACK_EX}clear --> Clears the console{Style.RESET_ALL}
                    """)
          elif inputs in ["show", "sho", "sh", "s", "-s", "-show", "--show"]:                  show()
          elif inputs in ["add", "ad", "a", "-a", "-add", "--add"]:                            add()
          elif inputs in ["delete", "delet", "dele", "del", "de", "d", "-delete", "--delete"]: delete()
          elif inputs in ["change", "chang", "c", "-c", "-change", "--change"]:                change()    
          elif inputs in ["search", "searc", "sear", "sea", "s", "-s", "-search", "--search"]: search()
          elif inputs in ["quit", "qui", "qu", "q", "exit", "ex", "gtfo", "getout", "gottagetout", "immaheadout", "bigbrain", "bigweiner"]:quit()
          elif inputs in ["clear", "clea", "cle", "cls"]:                                      os.system("cls")
          else: first_time = True

























