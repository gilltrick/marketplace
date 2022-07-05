from flask import Flask, render_template, make_response, request, redirect
from umbrella import analytics, database, communication, api, controller

#cli = api.sys.modules['flask.cli']
#cli.show_server_banner = lambda *x: None
app = Flask(__name__)

@app.route("/")
def index():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        return render_template("home.html", resultList = [], popularItemsList=database.popularItemsList, sponsoredItemsList = database.sponsoredItemsList)
    return render_template("index.html")

@app.route("/search", methods=["post"])
def search():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        searchTerm = request.form["searchTerm"]
        return render_template("home.html", resultList=database.SearchItem(searchTerm))
    return "you need to be loged in"

@app.route("/advancedSearch", methods=["post"])
def advancedSearch():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        searchTerm = request.form["searchTerm"]
        categorie = request.form["categorie"]
        priceFrom = request.form["from"]
        priceTo = request.form["to"]
        try:
            command = request.form["command"]
        except:
            command=""
        return render_template("home.html", resultList=database.AdvancedItemSearch(searchTerm, categorie, priceFrom, priceTo, command))
    return "you need to be loged in"            
    
@app.route("/itemPage", methods=["post"])
def itemPage():
    itemId = request.form["id"]
    itemObject = database.LoadItemObejctById(itemId)
    sellerObject = database.GetItemSeller(itemObject.id)
    return render_template("itemPage.html", itemObject=itemObject, sellerObject=sellerObject)

@app.route("/impressum")
def impressum():
    return render_template("impressum.html")

@app.route("/addToCard", methods=["post"])
def addToCard():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        itemId = request.form["id"]
        print(itemId)
        checkOutItem = database.LoadItemObejctById(itemId)
        print(checkOutItem.price)
        userObject = database.GetUserObjectByUserName(username)
        database.AddItemToUsersCard(itemId, username)
        sellerObject = database.GetItemSeller(itemId) 
        return render_template("checkOut.html", userObject=userObject, checkOutItem = checkOutItem, sellerObject=sellerObject)
    return "you need to be loged in"
    
@app.route("/card")
def card():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):
        userObject = database.GetUserObjectByUserName(username)
        if len(userObject.cardList) < 1:
            return "no items in card"
        sellerObject = database.GetItemSeller(userObject.cardList[0])
        return render_template("checkOut.html", userObject = userObject, checkOutItem = userObject.cardList[0], sellerObject=sellerObject)


@app.route("/checkOut", methods=["post"])
def checkOut():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        itemId = request.form["id"]
        checkOutItem = database.LoadItemObejctById(itemId)
        userObject = database.GetUserObjectByUserName(username)
        sellerObject = database.GetItemSeller(itemId)    
        return render_template("checkOut.html", userObject=userObject, checkOutItem = checkOutItem, sellerObject=sellerObject)
    return "you need to be loged in"  

@app.route("/buyItem", methods=["post"])
def buyItem():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        itemId = request.form["id"]
        country = request.form["cn"]
        city = request.form["cy"]
        postal = request.form["pc"]
        region = request.form["rn"]
        houseNumber = request.form["hn"]
        streetName = request.form["sn"]
        lastName = request.form["ln"]
        firstName = request.form["fn"]
        buyerName = firstName + " " + lastName
        streetNameAndNumber = streetName + " " + houseNumber
        #info = {"firstName":firstName,"lastName":lastName,"streetName":streetName,"houseNumber":houseNumber,"region":region,"postal":postal,"city":city,"country":country}
        return redirect(api.BuyItem(username, itemId, country, city, postal, region, streetNameAndNumber, buyerName)["url"])
    return "you need to be loged in"  

@app.route("/removeItemFromCard", methods=["post"])
def removeItemFromCard():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):
        userObject = database.GetUserObjectByUserName(username)
        itemId = request.form["id"]
        database.RemoveItemFromCard(userObject.id, itemId)
        if len(userObject.cardList) < 1:
            return "no items in card"
        sellerObject = database.GetItemSeller(userObject.cardList[0])
        return render_template("checkOut.html", userObject = userObject, checkOutItem = userObject.cardList[0], sellerObject=sellerObject)
    return render_template("error.html", error=database.modules.ErrorMessage("Video not removed from card", "What did you do?"))

###################### U S E R ########################

@app.route("/register")
def register():
    return render_template("registerUser.html")

@app.route("/registerUser", methods=["post"])
def registerUser():
    username = database.CreateMD5Hash(request.form["username"])
    password = database.CreateMD5Hash(request.form["password"])
    email = request.form["email"]
    nickName = request.form["4"]
    if database.NickNameAvailabel(nickName) == False:
        return "<script>alert(\"Nickname already in use. Please choose other\");location.href = \"/register\";</script>"
    if database.UserNameAvailable(username) == False:
        return "<script>alert(\"Username already in use. Please choose other\");location.href = \"/register\";</script>"
    if database.CreateUser(username, password, email, nickName):
        return render_template("login.html")
    return "something went wrong"

@app.route("/deleteUserAccount", methods=["post"])
def deleteUserAccount():
    userId = request.form["id"]
    userPassword=database.CreateMD5Hash(request.form["password"])
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        if userPassword == password:
            database.DeleteUser(userId)
            return "<script>alert(\"Your account and items got deleted\");location.href = \"/\";</script>"
        return "<script>alert(\"Wrong password\");location.href = \"/userAccount\";</script>"
    return "you need to be loged in"     

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginUser", methods=["post"])
def loginUser():
    username = database.CreateMD5Hash(request.form["username"])
    password = database.CreateMD5Hash(request.form["password"])
    if database.CheckCredentials(username, password):
        userObject = database.LoadUserObjectFromFileByName(username)
        response = make_response(render_template("home.html", resultList = [], popularItemsList=database.popularItemsList, sponsoredItemsList = database.sponsoredItemsList, unreadMessagesCount=str(len(userObject.unreadConversationsList))))
        cookieValue = "{\"username\":\""+username+"\";\"password\":\""+password+"\"}"
        response.set_cookie("data", cookieValue)
        return response
    return "not allowed"

@app.route("/home")
def home():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        return render_template("home.html", resultList = [], popularItemsList = database.popularItemsList, sponsoredItemsList = database.sponsoredItemsList)
    return "you need to login first"

@app.route("/userAccount")
def userAccount():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        userObject = database.LoadUserObjectFromFileByName(username)
        return render_template("userAccount.html", userObject = userObject, unreadMessagesCount=str(len(userObject.unreadConversationsList)), favoriteItemsList = database.GetUserFavoriteList(userObject.id))
    return "not allowed"

@app.route("/logout")
def logout():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password) == True:
        response = make_response(render_template("login.html"))
        response.set_cookie("data", '', expires=0)
        return response
    return "logoud didnt work"

@app.route("/likeSeller", methods=["post"])
def likeSeller():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        itemId = request.form["id"]
        userObject = database.GetSimpleUserObjectByUserName(username)
        sellerObject = database.GetItemSeller(itemId)
        item = database.LoadItemObejctById(itemId)
        database.LikeSeller(sellerObject.id, userObject.id)
        return render_template("itemPage.html", itemObject=item, sellerObject=sellerObject)
    return "you need to be loged in"

@app.route("/likeItem", methods=["post"])
def likeItem():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        itemId = request.form["id"]
        userObject = database.GetSimpleUserObjectByUserName(username)
        item = database.LikeItem(itemId, userObject.id)
        sellerObject = database.GetItemSeller(item.id)
        return render_template("itemPage.html", itemObject=item, sellerObject=sellerObject)
    return "you need to be loged in"
    

@app.route("/dissLikeItem", methods=["post"])
def dissLikeItem():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        itemId = request.form["id"]
        userObject = database.GetSimpleUserObjectByUserName(username)
        item = database.DissLikeItem(itemId, userObject.id)
        sellerObject = database.GetItemSeller(item.id)
        return render_template("itemPage.html", itemObject=item, sellerObject=sellerObject)
    return "you need to be loged in"
        
@app.route("/changeWallet", methods=["post"])
def changeWallet():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        _password = request.form["password"]
        walletId = request.form["id"]
        database.ChangeWallet(username, _password, walletId)
        return "your wallet got changed"        
        
@app.route("/forgottPassword")
def forgottPasswrod():
    return "not available on this kind of site :D"
############################ I T E M S #############################

@app.route("/createItem", methods=["post"])
def createItem():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        userId = request.form["id"]
        itemPrice = request.form["itemPrice"]
        itemName = request.form["itemName"]
        itemDiscription = request.form["itemDiscription"]
        images = request.files.getlist("images")
        categories = request.form["categories"]
        itemGaleryList = []
        for image in images:
            fileName = database.GetFileName(str(image))
            itemGaleryList.append(fileName)
        item = database.CreateItem(userId, itemName, itemDiscription, itemPrice, itemGaleryList, categories)  
        for image in images:
            fileName = database.GetFileName(str(image))
            if fileName != "":
                image.save(database.itemPicturesPath + item.id +"/" + fileName)
        userObject = database.LoadUserObjectFromFileByName(username)
        return render_template("userAccount.html", userObject = userObject)
            
@app.route("/deleteItem" ,methods=["post"])
def deleteItem():
    itemId = request.form["id"]
    database.DeleteItem(itemId)
    return "<script>alert(\"Item deleted\");location.href = \"/userAccount\";</script>" 

@app.route("/editItem", methods=["post"])
def editItem():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        itemId = request.form["id"]
        itemObject = database.LoadItemObejctById(itemId)
        return render_template("editItem.html", itemObject=itemObject)

@app.route("/deletePictureFromItem", methods=["post"])
def deletePictureFromItem():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)        
    if database.CheckCredentials(username, password):
        picturePath = request.form["picturePath"]
        itemId = request.form["id"]
        item = database.RemovePictureFromItem(itemId, picturePath)
        return render_template("editItem.html", itemObject=item)

@app.route("/addItemToFavoriteList", methods=["post"])
def addItemToFavoriteList():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):    
        itemId = request.form["id"]
        userId = database.GetSimpleUserObjectByUserName(username).id
        database.AddItemToFavoriteList(itemId, userId)
        return "<script>alert(\"Item added to your favorites list.\");location.href = \"/home\";</script>"  
    return "you need to be loged in"

@app.route("/removeItemFromFavoriteList", methods=["post"])
def removeItemFromFavoriteList():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):
        userObject = database.GetSimpleUserObjectByUserName(username)     
        itemId = request.form["id"]
        database.RemoveFavoriteFromList(userObject.id, itemId)
        return "<script>alert(\"Item removed from your favorites list.\");location.href = \"/home\";</script>"  
    return "you need to be loged in"

##################### M E S S A G I N G #####################
@app.route("/messaging", methods=["post"])
def messaging():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    receiverId = request.form["id"]
    if database.CheckCredentials(username, password):
        userObject = database.GetUserByCredentials(username, password)
        conversationList = communication.LoadUsersConversations(username)
        openConversation = communication.LoadConversationIfExisiting(username, database.GetUserObjectById(receiverId).username)
        if openConversation != None and openConversation.id in userObject.unreadConversationsList:
            communication.MarkConversationAsRead(openConversation.id, userObject.id)
    return render_template("messaging.html", openConversation=openConversation, senderId=userObject.id, receiverId=receiverId, conversationList=conversationList)

@app.route("/messages")
def messages():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password) == True:
        userObject = database.GetUserObjectByUserName(username)
        conversationList = communication.LoadUsersConversations(username)
        if len(conversationList) > 0:
            openConversation = conversationList[len(conversationList)-1]
        if len(conversationList) < 1:
            #openConversation = communication.CreateDummyConversation()
            openConversation = communication.CreateSupportConversation(userObject.id)
            conversationList.append(openConversation)
        return render_template("messaging.html", openConversation=openConversation, receiverId=openConversation.participentId, senderId=userObject.id, conversationList=conversationList)
    return "you need to be loged in"

@app.route("/sendMessage", methods=["post"])
def sendMessage():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):
        userObject = database.GetUserByCredentials(username, password)
        receiverId = request.form["id"]
        messageText = request.form["messageText"]
        senderNickName = database.GetSimpleUserObjectById(userObject.id).nickName
        communication.SendMessage(userObject.id, receiverId, userObject.username, "titleText", messageText, senderNickName)
        conversationList = communication.LoadUsersConversations(username)
        receiverObject = database.GetSimpleUserObjectById(receiverId)
        openConversation = communication.LoadConversationIfExisiting(username, receiverObject.username)
    return render_template("messaging.html", openConversation=openConversation, senderId=userObject.id, receiverId=receiverId, receiverNickName= receiverObject.nickName, conversationList=conversationList)
 
@app.route("/writeComment", methods=["post"])
def sendComment():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password) == True:
        #check later if writer has bought the item in the first place    
        itemId = request.form["id"]
        commentTitle = request.form["commentTitle"]
        commentText = request.form["commentText"]
        database.AddCommentToItem(itemId, username, commentTitle, commentText)
        sellerObject = database.GetItemSeller(itemId)
        return render_template("itemPage.html", itemObject = database.LoadItemObejctById(itemId), sellerObject=sellerObject)

@app.route("/sendOfferMessage", methods=["post"])
def sendOffer():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password) == True:
        #sellerId = request.form["sellerId"]
        userObject = database.GetUserByCredentials(username,password)
        sellerId = userObject.id
        buyerId = request.form["buyerId"]
        #offerTitle = request.form["offerTitle"]
        offerTitle = "offerMessage"
        offerText = request.form["offerText"]
        offerPrice = request.form["offerPrice"]
        if offerTitle == "":
            offerTitle = "offerMessage"
        communication.CreateOffer(sellerId, buyerId, offerTitle, offerText, offerPrice)
        conversationList = communication.LoadUsersConversations(username)
        if len(conversationList) > 0:
            openConversation = conversationList[len(conversationList)-1]
        if len(conversationList) < 1:
            openConversation = communication.CreateDummyConversation()
            conversationList.append(openConversation)
    return render_template("messaging.html", openConversation=openConversation, receiverId=openConversation.participentId, senderId=userObject.id, conversationList=conversationList) 

@app.route("/payOffer", methods=["post"])
def payOffer():
    cookieValue = request.cookies.get("data")
    username, password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):
        offerId = request.form["offerId"]
        sellerId = request.form["sellerId"]
        userId = database.GetUserByCredentials(username, password).id
        return redirect(api.CustomInvoice(userId, sellerId, offerId)['url'])

################################## Application Programming Interface ################################
@app.route("/api", methods=["Post"])
def API():
    command = request.form["command"]
    data = request.form["data"]
    key = request.form["key"]
    print("[+]API Command: " + command + " data: " + data)
    if key != api.key:
        return "Not allowed"
    if command == "startBPS":
        api.LoopCheck(True)
    if command == "stopBPS":
        api.run = False
    if command == "reloadPopularItemsList":
        database.CreateRandomPopularItemsList()
    if command == "paymentDone":
        result = database.re.search("(.*)\?\?(.*)", data)
        userId = result.group(1)
        itemId = result.group(2)
        database.AddItemToPurchasedList(userId, itemId)
    return "done"         
     
if __name__ == "__main__":
    controller.CheckIfSetupIsDone()
    database.InitDB()
    app.run(debug=True, host=api.host, port=api.port, use_reloader=True)
    print("[-]SERVER: Server stoped")