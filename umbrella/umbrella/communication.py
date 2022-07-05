import os, pickle
from umbrella import modules, database

messageRoot = os.getcwd()+"/data/userDatabase/Users/"

conversationList = []

def SendMessage(_senderId, _receiverId, _senderUserName, _titleText, _messageText, _senderNickName):
    timeStamp = database.CreateTimeStamp()
    receiverUserName = database.GetUserObjectById(_receiverId).username 
    message = modules.Message.CreateMessage(_senderId, _receiverId, _senderUserName, receiverUserName, _titleText, _messageText, timeStamp, _senderNickName)
    message.id = database.CreateRandomId()
    if ConversationExists(message):
        UpdateConversation(message)
        return
    return StartConversation(message)

def SendDeliverMessage(_itemId, _buyerId, _buyerData):
    item = database.LoadItemObejctById(_itemId)
    if item == "invalid": 
        print("invalid item with id: " + _itemId)
        for item in database.itemObjectList:
            print("[!]: item.id from list: " + item.id)
        for item in database.itemList:
            print("[!]: item.id from list: " + item.id)
        return
    senderId = "support"
    receiverId = item.userId
    senderUsername = "SUPPORTUSERNAME"
    senderNickName = "Support"
    messageTitle = "Item Sold - Time To Deliver"
    messageText = item.name +" sold!\nBuyer:\nName: " + _buyerData["name"]+"\nStreet: " + _buyerData["address1"] + "\nPostal: " +_buyerData["phone"] + "\nCity: " + _buyerData["address2"]
    SendMessage(senderId, receiverId, senderUsername, messageTitle, messageText, senderNickName)
    messageTitle = "Item Payed In Full"
    messageText = "Your payment of " +item.price +" $ for " + item.name + " has been accepted"
    SendMessage(senderId, _buyerId, senderUsername, messageTitle, messageText, senderNickName)
    saleObject = modules.SaleObject()
    saleObject.id = database.CreateRandomId()
    saleObject.sellerId = item.userId
    saleObject.buyerId = _buyerId
    saleObject.buyerData = _buyerData
    saleObject.createdOn = database.CreateTimeStamp()
    saleObject.status = "payed"
    buyerUserObject = database.GetUserObjectById(_buyerId)
    sellerUserObject = database.GetUserObjectById(item.userId)
    buyerUserObject.saleObjectList.append(saleObject)
    sellerUserObject.saleObjectList.append(saleObject)
    database.SaveUserObject(buyerUserObject)
    database.SaveUserObject(sellerUserObject)
      
def ConversationExists(_message):
    if os.path.exists(messageRoot+"/"+_message.senderUserName+"/messages/"+_message.receiverUserName):
        return True
    
def UpdateConversation(_message):
    senderConversationFile = open(messageRoot+"/"+_message.senderUserName+"/messages/"+_message.receiverUserName, "rb")
    senderConversation = pickle.load(senderConversationFile)
    senderConversationFile.close()
    _message.conversationId = senderConversation.id
    senderConversation.participentId = _message.receiverId
    senderConversation.senderUserName = _message.senderUserName
    senderConversation.receiverUserName = _message.receiverUserName
    senderConversation.participentNickName = database.GetUserObjectById(_message.receiverId).nickName
    senderConversation.messageList.append(_message)
    senderFile = open(messageRoot+"/"+_message.senderUserName+"/messages/"+_message.receiverUserName,"wb")
    pickle.dump(senderConversation, senderFile)
    senderFile.close()
    receiverConversationFile = open(messageRoot+"/"+_message.receiverUserName+"/messages/"+_message.senderUserName,"rb")
    receiverConversation = pickle.load(receiverConversationFile)
    receiverConversationFile.close()
    receiverConversation.participentId = _message.senderId
    receiverConversation.senderUserName = _message.receiverUserName
    receiverConversation.receiverUserName = _message.senderUserName
    receiverUserObject = database.GetUserObjectById(_message.receiverId)
    receiverUserObject.unreadConversationsList.append(senderConversation.id)
    database.SaveUserObject(receiverUserObject)
    receiverConversationFile.participentNickName = receiverUserObject.nickName
    receiverConversation.messageList.append(_message)
    receiverConversationFile = open(messageRoot+"/"+_message.receiverUserName+"/messages/"+_message.senderUserName,"wb")
    pickle.dump(receiverConversation, receiverConversationFile)  
    receiverConversationFile.close()

def StartConversation(_message):
    conversation = modules.Conversation()
    conversation.id = database.CreateRandomId()
    conversation.starterId = _message.senderId
    conversation.participentId = _message.receiverId
    conversation.senderUserName = _message.senderUserName
    conversation.receiverUserName = _message.receiverUserName
    conversation.participentNickName = database.GetUserObjectById(_message.receiverId).nickName
    conversation.messageList.append(_message)
    senderFile = open(messageRoot+"/"+_message.senderUserName+"/messages/"+conversation.receiverUserName,"wb")
    pickle.dump(conversation, senderFile)
    senderFile.close()
    receiverFile = open(messageRoot+"/"+_message.receiverUserName+"/messages/"+conversation.senderUserName,"wb")
    conversation.participentId = _message.senderId
    conversation.senderUserName = _message.receiverUserName
    conversation.receiverUserName = _message.senderUserName
    participentUserObject = database.GetUserObjectById(_message.receiverId)
    participentUserObject.unreadConversationsList.append(conversation.id)
    database.SaveUserObject(participentUserObject)
    conversation.participentNickName = database.GetUserObjectById(_message.senderId).nickName
    pickle.dump(conversation, receiverFile)  
    receiverFile.close()
    conversationList.append(conversation)
    database.SaveUserObject(participentUserObject)
    return conversation

def MarkConversationAsRead(_conversationId, _userId):
    userObject = database.GetUserObjectById(_userId)
    userObject.unreadConversationsList.remove(_conversationId)
    database.SaveUserObject(userObject)
    return

def CreateOffer(_sellerId, _buyerId, _offerTitle, _offerText, _offerPrice):
    sellerUserObject = database.GetUserObjectById(_sellerId)
    receiverUserObject = database.GetUserObjectById(_buyerId)
    offer = modules.CustomSale()
    offer.id = database.CreateRandomId()
    offer.sellerId = _sellerId
    offer.buyerId = _buyerId
    offer.offerTitle = _offerTitle
    offer.offerText = _offerText
    offer.offerPrice = _offerPrice
    offer.timeStamp = database.CreateTimeStamp()
    message = modules.Message.CreateMessage(_sellerId, _buyerId, sellerUserObject.username, receiverUserObject.username, "offerMessage", "", database.CreateTimeStamp(), sellerUserObject.nickName)
    message.id = database.CreateRandomId()
    message.offer = offer
    SendOfferMessage(message)
   
def SendOfferMessage(_message):
    if ConversationExists(_message):
        UpdateConversation(_message)
        return
    StartConversation(_message)    
    
def SendFollowerNotificationMessage(_message):
    if ConversationExists(_message):
        UpdateConversation(_message)
        return
    StartConversation(_message)  
        
def LoadUsersConversations(_username):
    conversationFileNameList = os.listdir(messageRoot+"/"+_username+"/messages/")
    conversationList = []
    for conversationFileName in conversationFileNameList:
        conversationFile = open(messageRoot+"/"+_username+"/messages/"+conversationFileName, "rb")
        conversation = pickle.load(conversationFile)
        conversationList.append(conversation)
    return conversationList
           
def LoadConversationIfExisiting(_username, _receiverUserName):
    if os.path.exists(messageRoot+"/"+_username+"/messages/"+_receiverUserName):
        conversationFile = open(messageRoot+"/"+_username+"/messages/"+_receiverUserName, "rb")
        conversation = pickle.load(conversationFile)
        conversationFile.close()
        return conversation
    return None


    
def CreateDummyConversation():
    #make this the welcome message and entry point for writing with the support 
    # i have to create a conversation and save it for both
    conversation = modules.Conversation()
    conversation.participentNickName = "Dummy-Object"
    message = modules.Message()
    message.titleText = "Dummy-Message"
    message.messageText = "Dummy-Message-Text-Content"
    conversation.messageList.append(message)
    return conversation

def CreateSupportConversation(_userId):
    receiverUserObject = database.GetUserObjectById(_userId)
    senderId = "support"
    senderUsername = "SUPPORTUSERNAME"
    titleText = "Hello and welcome to umbrella"
    messageText = "You can answer on this messag in case you need some support :)"
    senderNickName = "Support"
    return SendMessage(senderId, receiverUserObject.id, senderUsername, titleText, messageText, senderNickName)
    
def NotifyFollower(_userObject, __metaInformationObject):
    for follower in _userObject.followerList:
        followerUserObject = database.GetUserObjectById(follower)
        message = modules.Message()
        message.titleText = "followerNotification"
        message.messageText = "My new video: " + __metaInformationObject.videoTitle + " is online"
        message.offer = __metaInformationObject.videoUrl
        message.id = database.CreateRandomId()
        message.senderId = _userObject.id
        message.senderUserName = _userObject.username
        message.senderNickName = _userObject.nickName
        message.receiverId = follower
        message.receiverUserName = followerUserObject.username
        message.timeStamp = database.CreateTimeStamp()
        #SendMessage(_userObject.id, follower, _userObject.username, "followerNotification", "My new viedeo: " + __metaInformationObject.videoTitle + " is online", _userObject.nickName)
        SendFollowerNotificationMessage(message)
    return