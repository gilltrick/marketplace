import requests, os, pickle
from umbrella import api, controller
from btcpay import BTCPayClient

def Run():
    command = input("Enter command [-start, -stop, -newClient, -deleteClient, -database]: ")
    if command == "-start":
        StartListenLoop()
    if command == "-stop":
        StopListenLoop()
    if command == "-newClient":
        CreateClient()
    if command == "-deleteClient":
        DeleteClient()
    if command == "-database":
        Database()
    if command =="-reload":
        data = {"command":"reloadPopularItemsList", "data":"_", "key": api.key}
        api.API_Post(data)

def Database():
    command = input("You have the following databsae options [-print, -dangerousItems]")
    if command == "-print":
        controller.PrintDatabase()
    if command == "-dangerousItems":
        controller.PrintDangerousItemsList()

def CreateClient():
    if os.path.exists(os.getcwd()+"/api/pair.pair"):
        print("[-]API: Client file already exists @"+os.getcwd()+"/api/pair.pair")
        return "client exists"
    host = input("[?]Enter host url: ")
    code = input("[?]Enter access token code: ")
    client = BTCPayClient.create_client(host=host, code=code)
    SaveClient(client)
    return "[+]API: Client created and saved"        

def LoadClient():
    try:
        file = open(os.getcwd()+"/api/pair.pair", "rb")
        return pickle.load(file)
    except:
        print("[-]API: Can't load client @"+os.getcwd()+"/api/pair.pair")
        return 
    
def DeleteClient():
    command = input("[+]Do you realy want to delete the cliente?\n[+]Without the client have to handle the payment manually\n[?]Delete Client? [-YES / no]: ")
    if command == "-YES":
        controller.LoadServerSettings()
        _key = input("[?]Enter api key: ")
        if _key == api.key: 
            os.remove(os.getcwd()+"/api/pair.pair")
            
def SaveClient(_client):
    if os.path.exists(os.getcwd()+"/api/pair.pair"):
        print("[-]API: Client file already exists @"+os.getcwd()+"/api/pair.pair")
        return 
    file = open(os.getcwd()+"/api/pair.pair", "wb")
    pickle.dump(_client, file)

def StartListenLoop():
    print("[+]Enter server address:")
    host = input("[?]Enter host url: ")
    port = input("[?]Enter port: ")
    key = input("[?]Enter api key: ")
    url = "http://" + host + ":" + port + "/api"
    print("[+]API: Pay server on " + url + " starting...")
    try:
        requests.post(url, data={"command":"startBPS", "data":"_", "key": key})
    except:
        print("[-]API: Pay server stopped")
    input("Press Enter to exit")    
        
def StopListenLoop():
    print("[+]Enter server address:")
    host = input("[?]Enter host url: ")
    port = input("[?]Enter port: ")
    key = input("[?]Enter api key: ")
    url = "http://" + host + ":" + port + "/api"
    print("[+]API: Pay server on " + url + " shuting down...")
    try:
        requests.post(url, data={"command":"stopBPS", "data":"_", "key": key})
    except:
        print("[-]API: Pay server stopped")  

if __name__ == "__main__":
    Run()