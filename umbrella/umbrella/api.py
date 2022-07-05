import requests, pickle, os, time, sys, datetime
from btcpay import BTCPayClient
from umbrella import database, communication, modules

url = "http://YOUR_HOST_IP:YOUR_PORT/api"
host = "YOUR_HOST_IP"
port = "YOUR_PORT"
key = "YOUR_API-KEY"
btcHost = "YOURBITCOIN-PAYMENT-SERVER"
tokenCode = ""
pattern = "{\"invoiceid\":\"(.*)\";\"userid\":\"(.*)\";\"itemid\":\"(.*)\"}"

paidInvoiceListLenght = 0
paidAndDeliverdList =  []
paidAndDeliveredListLenght = 0

def Run(_command):
    if _command == "":
        _command = input("Enter command: [-payment, -btcpay -listenLoop] ")
    if _command == "-payment":
        Payment()
    if _command == "-btcpay":
        _command = input("Enter command: [-createClient, -deleteClient] ")
        if _command == "-createClient":
            CreateClient(btcHost, tokenCode)
        if _command == "-deleteClient":
            DeleteClient()
    if _command == "-localListenLoop":
        InitAPI()
    if _command == "-listenLoop":
        #LoadPaidAndDeliveredList()
        print("[+]API: Starting Payment Server") 
        data = {"command":"startBPS", "data":"_", "key": key}
        API_Post(data)
    if _command == "-stopListenLoop":
        print("[+]API: Shuting Down Payment Server") 
        data = {"command":"stopBPS", "data":"_", "key": key}
        API_Post(data)
    if _command == "-reloadPopularItemsList":
        data = {"command":"reloadPopularItemsList", "data":"_", "key": key}
        API_Post(data)
        
def InitAPI():
    LoadPaidAndDeliveredList()
    if len(database.userObjectList) < 1:
        print("Loading Database from API")
        database.InitDB()
    LoopCheck()
    
def Payment():
    userId = input("Enter user-Id: ")
    itemId = input("Enter item-Id: ")
    data = userId + "??" + itemId
    data = {"command":"paymentDone", "data":data, "key": key}    
    Post(data)
    
def Post(_data):
    print(requests.post(url, data=_data).text)

def CreateClient(_btcHost, _tokenCode):
    if os.path.exists(os.getcwd()+"/api/pair.pair"):
        print("client exists")
        return "client exists"
    if _btcHost == "": _btcHost = btcHost
    if _tokenCode == "": _tokenCode == tokenCode
    client = BTCPayClient.create_client(host=_btcHost, code=_tokenCode)
    SaveClient(client)
    print("Client created and saved @" + os.getcwd()+"/api/pair.pair\nPress enter to exit")
    return "client created and saved"

def DeleteClient():
    command = input("Do you realy want to delete the cliente?\nWithout the client have to handle the payment manually\nDelete Client? [-YES / no]: ")
    if command == "-YES":
        global key
        _key = input("Enter api key: ")
        if _key == key: 
            os.remove(os.getcwd()+"/api/pair.pair")
    print("Press enter to exit")

def LoadClient():
    try:
        file = open(os.getcwd()+"/api/pair.pair", "rb")
        return pickle.load(file)
    except:
        return "[-]API: Can't load client"

def SaveClient(_client):
    if os.path.exists(os.getcwd()+"/api/pair.pair"):
        print("file exists")
        return 
    file = open(os.getcwd()+"/api/pair.pair", "wb")
    pickle.dump(_client, file)

def BuyItem(_username, _itemId, _country, _city, _postal, _region, _streetNameAndNumber, _buyerName):
    simpleUserObject = database.GetSimpleUserObjectByUserName(_username)
    item = database.LoadItemObejctById(_itemId)
    client = LoadClient()
    print("[+]API: Client loaded")
    newInvoice = client.create_invoice({"price": item.price, "currency": "USD", "posData": simpleUserObject.id, "itemDesc": _itemId, "buyer":{"name":_buyerName,"address1":_streetNameAndNumber,"address2":_city,"phone":_postal,"locality":_city,"region":_region,"country":_country}})
    return newInvoice

def CustomInvoice(_userId, _sellerId, _offerId):
    client = LoadClient()
    buyerUserObject = database.GetSimpleUserObjectById(_userId)
    sellerUserObject = database.GetSimpleUserObjectById(_sellerId)
    buyerUserName = buyerUserObject.username
    conversation = communication.LoadConversationIfExisiting(buyerUserName, sellerUserObject.username)
    for message in conversation.messageList:
        if message.offer != "":
            if message.offer.id == _offerId:
                newInvoice = client.create_invoice({"price": message.offer.offerPrice, "currency": "USD", "posData": _userId, "itemDesc": _offerId, "buyer":{"name":_sellerId}})
                return newInvoice
    return

def SavePaidAndDeliverdList():
    global paidAndDeliverdList
    global paidAndDeliveredListLenght
    paidAndDeliveredListLenght = len(paidAndDeliverdList)
    file = open(os.getcwd()+"/api/_data/paidAndDeliveredList", "wb")
    pickle.dump(paidAndDeliverdList, file)
    file.close()
    print("[+]API: Saved paidInvoiceList")

def LoadPaidAndDeliveredList():
    global paidAndDeliverdList
    global paidAndDeliveredListLenght
    if os.path.exists(os.getcwd()+"/api/_data/paidAndDeliveredList") == False:
        command = input("[?]API: No database file found: Create one? ")
        if command == "yes":
            open(os.getcwd()+"/api/_data/paidAndDeliveredList", "wb")
    file = open(os.getcwd()+"/api/_data/paidAndDeliveredList", "rb")
    try:
        paidAndDeliverdList = pickle.load(file)
        paidAndDeliveredListLenght = len(paidAndDeliverdList)
        file.close()
    except:
        print("[-]API: no data in paidAndDeliveredList")
        file.close()

def LoopCheck(_status):
    LoadPaidAndDeliveredList()
    global run
    global paidAndDeliverdList
    global paidAndDeliveredListLenght
    tempPaidList = []
    fullList = []
    run = _status
    client = LoadClient()
    print("[+]API: Client loaded")
    print("[+]API: Entering payment listen loop")
    while run:
        tempPaidList.clear()
        fullList.clear()
        try:
            fullList = client.get_invoices()
        except:
            print("[-]API: Cant load invoicese.\nSaving data\nShutdown bps service api")
            return
        for invoice in fullList:
            if invoice['status'] == "complete":
                tempPaidList.append(invoice)
        for invoice in tempPaidList:
            match = False
            if len(paidAndDeliverdList) < 1:
                Deliver(invoice['id'], invoice['posData'], invoice['itemDesc'], invoice["buyer"])
                paidAndDeliverdList.append(invoice)
            for completedInvoice in paidAndDeliverdList:
                if invoice['id'] == completedInvoice['id']:
                    match = True
            if match == False:
                if invoice["buyer"]["name"] != None and invoice["buyer"]["address1"] == None:
                    CustomOfferGotPayed(invoice['id'], invoice['posData'], invoice['itemDesc'], invoice["buyer"]["name"])
                else:
                    Deliver(invoice['id'], invoice['posData'], invoice['itemDesc'], invoice["buyer"])
                paidAndDeliverdList.append(invoice)
        if len(paidAndDeliverdList) > paidAndDeliveredListLenght + 1:
            SavePaidAndDeliverdList()
        time.sleep(10)
    SavePaidAndDeliverdList()
    print("[+]API: Payment server stoped")

def CustomOfferGotPayed(_invoiceId, _userId, _itemId, _sellerId):
    print("_sellerId: " + _sellerId)
    print("_buyerId: " + _userId)
    sellerUserObject = database.GetSimpleUserObjectById(_sellerId)
    buyerUserObject = database.GetSimpleUserObjectById(_userId)
    sellerConversationFile = open(os.getcwd()+"/data/userDatabase/Users/"+sellerUserObject.username+"/messages/"+buyerUserObject.username, "rb")
    sellerConversation = pickle.load(sellerConversationFile)
    sellerConversationFile.close()
    for message in sellerConversation.messageList:
        if message.offer != "":
            if message.offer.id == _itemId:
                newMessage = modules.Message()
                newMessage.senderNickName = "nJoyPorn-Support"
                newMessage.senderId = _sellerId
                newMessage.receiverId = _userId
                newMessage.messageText = "Your offer got accepted and payed in full"
                newMessage.senderUserName = sellerUserObject.username
                newMessage.receiverUserName = buyerUserObject.username
                newMessage.timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                newMessage.id = database.CreateRandomId()
                newMessage.conversationId = sellerConversation.id
                sellerConversation.messageList.append(newMessage)
                sellerConversationFile = open(os.getcwd()+"/data/userDatabase/Users/"+sellerUserObject.username+"/messages/"+buyerUserObject.username, "wb")
                pickle.dump(sellerConversation, sellerConversationFile)
                sellerConversationFile.close()
    buyerConversationFile = open(os.getcwd()+"/data/userDatabase/Users/"+buyerUserObject.username+"/messages/"+sellerUserObject.username, "rb")
    buyerConversation = pickle.load(buyerConversationFile)
    buyerConversationFile.close()
    for message in buyerConversation.messageList:
        if message.offer != "":
            if message.offer.id == _itemId:
                newMessage.senderNickName = "nJoyPorn-Support"
                newMessage.senderId = _userId
                newMessage.receiverId = _sellerId
                newMessage.messageText = "Your payment got accepted"
                newMessage.senderUserName = buyerUserObject.username
                newMessage.receiverUserName = sellerUserObject.username
                newMessage.conversationId = buyerConversation.id
                buyerConversation.messageList.append(newMessage)
                buyerConversationFile = open(os.getcwd()+"/data/userDatabase/Users/"+buyerUserObject.username+"/messages/"+sellerUserObject.username, "wb")
                pickle.dump(buyerConversation, buyerConversationFile)
                buyerConversationFile.close()

def Deliver(_invoiceId, _userId, _itemId, _buyerData):
    print("DELIVER")
    if _invoiceId == None or _userId == None or _itemId == None:
        print("[!]API: invalid invoice data!")
        return
    file = open(os.getcwd()+"/api/_data/__logs/log", "a")
    line = "{\"invoiceid\":\""+_invoiceId+"\";\"userid\":\""+_userId+"\";\"itemid\":\""+_itemId+"\"}"
    file.write(line+"\n")
    API_AddItemToPurchasedList(_userId, _itemId)
    communication.SendDeliverMessage(_itemId, _userId, _buyerData)     

def API_AddItemToPurchasedList(_userId, _itemId):
    data = _userId + "??" + _itemId
    data = {"command":"paymentDone", "data":data, "key": key}    
    API_Post(data)
    
def API_Post(_data):
    if requests.post(url, data=_data).status_code == "200":
        print("API: Api is connected and running. Ready to process payments")
        return
    print(requests.post(url, data=_data).status_code)
    
def APIPost():
    data = {"command":"startBPS", "data":"_", "key": key}
    print("[+]API: response status Code: >> ", requests.post(url, data=data).status_code)

                
if __name__ == "__main__":
    try:
        command = sys.argv[1]
    except:
        command = ""
    Run(command)
    