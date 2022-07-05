import os, re
from umbrella import database, api, modules

itemObjectList = []

def Run():
    command=input("Enter command [-pdb]")
    if command == "-pdb":
        PrintDatabase()

def PrintDatabase():
    global itemObjectList
    itemObjectList = database.GetGlobalItemList()
    if len(itemObjectList) < 1:
        command = input("Empty item list. You want to init the database? ")
        if command =="yes" or command=="-yes" or command=="-y":
            database.InitDB()
            itemObjectList = database.GetGlobalItemList()
            if len(itemObjectList) < 1:
                print("No items available")
    for item in itemObjectList:
        print("Item-Name: " + item.name + "\nItem-Price: " + str(item.price) + "\nItem-ID: " + item.id+"\n")
    input("Press Enter to exit")  

def PrintDangerousItemsList():
    if len(database.userObjectList) <1:
        database.InitDB()
        print("Initializing database")
    dangerousItemDatabaseFile = open(os.getcwd()+"/data/__/dangerousitemdatabase.db", "r")
    lines = dangerousItemDatabaseFile.readlines()
    dangerousItemDatabaseFile.close()
    dangerousItemsList = []
    dangerousItemObjectList = []
    for line in lines:
            print("loop")
            result = re.search(database.itemPattern, line)
            item = modules.Item()
            item.id = result.group(1)
            item.userId = result.group(2)
            dangerousItemsList.append(item)
    for item in dangerousItemsList:
        dangerousItemObjectList.append(database.LoadItemObjectFromDisk(item))
    for item in dangerousItemObjectList:
        print("Item-Name: " + item.name + "\nItem-Id: " + item.id + "\nItem-Discription: " + item.discription + "\nSeller-Id: " + item.userId + "\n")

def Setup():
    print("[+]Setting up server settings...")
    newApiKey = input("[?]Enter your new API-Key or -create a random key: ")
    if newApiKey == "-create":
        newApiKey = database.CreateRandomId()
    if newApiKey == "":
        newApiKey = input("[?]You have to enter a key: ")
        if newApiKey == "": 
            print("[-]Setup cancled!")
    print("[!]Your API-Key: " + newApiKey)
    host = input("[?]Enter host url: ")
    if host == "":
        host = "0.0.0.0"
    port = input("[?]Enter port: ")
    if port == "":
        port = 5456      
    command = input("[+]Configure API:\n[+]You can do this later ass well or use the default server\n[?]Options [-configure, -later] ")
    if command == "-configure":
        btcpayServerUrl = input("[!]Get your pairing tokens code for your btc-pay server\n[?]Enter server url: ")
        pairingCode = input("[?]Enter paring token code: ")
        print(api.CreateClient(btcpayServerUrl, pairingCode))
    lines = "\"host\":\""+host+"\",\n\"port\":\""+port+"\",\n\"key\":\""+newApiKey+"\""
    serverConfigFile = open(os.getcwd()+"/data/__/server.conf", "w")
    serverConfigFile.writelines(lines)
    serverConfigFile.close()

def CheckIfSetupIsDone():
    if CheckFolderStructure():
        LoadServerSettings()
        return True
        
def LoadServerSettings():
    serverConfigFile = open(os.getcwd()+"/data/__/server.conf", "r")
    lines = serverConfigFile.readlines()
    serverConfigFile.close()
    for line in lines:
        if "port" in line:
            port = re.search("\"port\":\"(\d*)\"", line).group(1)
        if "host" in line:
            host = re.search("\"host\":\"(.*)\"", line).group(1)
        if "key" in line:
            key = re.search("\"key\":\"(.*)\"", line).group(1)
    api.key = key
    api.host = host
    api.port = port
    print("[+]CONTROLLER: Server settings loaded")        
    return
    
def CreateFiles():
    print("[+]CONTROLLER: Creating folders...")
    os.mkdir(os.getcwd()+"/data")
    os.mkdir(os.getcwd()+"/data/__")
    os.mkdir(os.getcwd()+"/data/userDatabase")
    os.mkdir(os.getcwd()+"/data/userDatabase/Users")
    os.mkdir(os.getcwd()+"/api")
    os.mkdir(os.getcwd()+"/api/_data")
    os.mkdir(os.getcwd()+"/api/_data/__")
    os.mkdir(os.getcwd()+"/api/_data/__logs")
    print("[+]CONTROLLER: Folders created\n[+]CONTROLLER: Creating files...")
    open(os.getcwd()+"/data/userDatabase/userdatabase.db", "a")
    open(os.getcwd()+"/data/itemdatabase.db", "a")
    open(os.getcwd()+"/data/__/PurchaseRequests", "a")
    open(os.getcwd()+"/api/_data/__logs/log", "a")
    open(os.getcwd()+"/api/_data/paidAndDeliveredList", "a")
    print("[+]CONTROLLER: Files created")
    database.CreateSupportUser()
    Setup()  
        
def CheckFolderStructure():
    fileExists = os.path.exists(os.getcwd()+"/data/__")
    fileExists = os.path.exists(os.getcwd()+"/data/itemdatabse.db")
    fileExists = os.path.exists(os.getcwd()+"/data/userDatabase/userdatabase.bd")
    fileExists = os.path.exists(os.getcwd()+"/data/userDatabase/Users")
    fileExists = os.path.exists(os.getcwd()+"/api/_data/paidAndDeliveredList")
    fileExists = os.path.exists(os.getcwd()+"/api/_data/__logs/log")
    if fileExists == False:
        print("[-]SERVER: Error with folder structure")
        CreateFiles()
        return True
    return True
    
if __name__ == "__main__":
    Run()