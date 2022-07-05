import os, pickle, datetime, hashlib, re, random
from umbrella import modules, analytics

userPattern = "{\"username\":\"(.*)\";\"password\":\"(.*)\";\"email\":\"(.*)\";\"id\":\"(.*)\";\"nickName\":\"(.*)\";\"role\":\"(.*)\"}"
cookiePattern = re.compile("{\"username\":\"(.*)\";\"password\":\"(.*)\"}")
instancePath = os.getcwd()+"/protected"
fileNamePattern = re.compile("<FileStorage:\s'(.*)'\s\('.*'\)")
userdatabasePath = os.getcwd()+"/data/userDatabase/Users/"
itemPicturesPath = os.getcwd()+"/static/items/"
itemPattern = re.compile("{\"itemId\":\"(.*)\";\"userId\":\"(.*)\"}")
walletPattern = re.compile("{\"id\":\"(.*)\";\"walletId\":\"(.*)\"}")
timePattern = "(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)"

userList = []
userObjectList = []
itemList = []
itemObjectList = []

popularItemsList = []
sponsoredItemsList = []

def InitDB():
    LoadUserList()
    print("[+]DATABASE: users in userList >> " + str(len(userList)))
    LoadFullUserDatabase()
    print("[+]DATABASE: users in userObjectList >> " + str(len(userObjectList)))
    LoadAllItems()
    print("[+]DATABASE: items in itemList >> " + str(len(itemList)))
    LoadItemObjectFromDiskByItemList()
    print("[+]DATABASE: items object in itemList >> " + str(len(itemObjectList)))
    CreateRandomPopularItemsList()
    CreateRandomSponsoredItemsList()
    #CreateSupportUser()
    
####################################  U S E R S ####################################

def CreateUser(_username, _password, _email, _nickName):
    user = modules.User()
    user.id = CreateRandomId()
    user.username = _username
    user.password = _password
    user.email = _email
    user.nickName = _nickName
    line = "{\"username\":\"" + _username + "\";\"password\":\"" + _password + "\";\"email\":\"" + _email + "\";\"id\":\"" + user.id + "\";\"nickName\":\"" + _nickName + "\";\"role\":\"" + "tester" + "\"}"
    os.mkdir(os.getcwd()+"/data/userDatabase/Users/"+user.username)
    os.mkdir(os.getcwd()+"/data/userDatabase/Users/"+user.username+"/items")
    os.mkdir(os.getcwd()+"/data/userDatabase/Users/"+user.username+"/messages")
    WriteUserDataToUserDatabase(line)
    SaveUserObject(user)
    global userObjectList
    global userList
    userObjectList.append(user)
    userList.append(user)
    return True 

def CreateSupportUser():
    if GetSimpleUserObjectById("support") != "invalid":return
    user = modules.User()
    user.id = "support"
    user.username = CreateMD5Hash("support@umbrella")
    user.password = CreateMD5Hash("support@umbrella")
    user.nickName = "Support"
    line = "{\"username\":\"" + user.username + "\";\"password\":\"" + user.password + "\";\"email\":\"" + "email" + "\";\"id\":\"" + user.id + "\";\"nickName\":\"" + user.nickName + "\";\"role\":\"" + "support" + "\"}"
    global userObjectList
    global userList
    userObjectList.append(user)
    userList.append(user)
    WriteUserDataToUserDatabase(line)
    os.mkdir(os.getcwd()+"/data/userDatabase/Users/"+user.username)
    os.mkdir(os.getcwd()+"/data/userDatabase/Users/"+user.username+"/messages")
    os.mkdir(os.getcwd()+"/data/userDatabase/Users/"+user.username+"/items")    
    SaveUserObject(user)
    print("[+]DATABASE: Support user created")
    
def SaveUserObject(_userObject):
    _userObject.itemObjectList.clear()
    userObjectFile = open(os.getcwd()+"/data/userDatabase/Users/"+_userObject.username+"/userObject", "wb")
    pickle.dump(_userObject, userObjectFile)
    userObjectFile.close()

def WriteUserDataToUserDatabase(_line):
    file = open(os.getcwd()+"/data/userDatabase/userdatabase.db", "a")
    file.write(_line + "\n")
    file.close()

def GetUserByCredentials(_username, _password):
    global userObjectList
    for userObject in userObjectList:
        if userObject.username == _username and userObject.password == _password:
            return userObject
    return "invalid"
    
def GetUserObjectById(_id):
    global userObjectList
    for userObject in userObjectList:
        if userObject.id == _id:
            return userObject
    global userList
    for user in userList:
        if user.id == _id:
            return LoadUserObjectFromFileByName(user.username)
    return "invalid"

def GetSimpleUserObjectById(_id):
    global userList
    for user in userList:
        if user.id == _id:
            return user
    return "invalid"

def GetSimpleUserObjectByUserName(_username):
    global userList
    for user in userList:
        if user.username == _username:
            return user
    return "invalid"

def GetUserObjectByUserName(_username):
    global userObjectList
    for userObject in userObjectList:
        if userObject.username == _username:
            return userObject
    return LoadUserObjectFromFileByName(_username)

def LoadUserList():
    file = open(os.getcwd()+"/data/userDatabase/userdatabase.db", "r")
    lines = file.readlines()
    file.close()
    global userList
    for line in lines:
        userList.append(LineToUser(line))
        
def LineToUser(_line):
    user = modules.User()
    result = re.search(userPattern, _line)
    user.username = result.group(1)
    user.password = result.group(2)
    user.email = result.group(3)
    user.id = result.group(4)
    user.nickName = result.group(5)
    user.role = result.group(6)
    return user

def UserToLine(_user):
    line = "{\"username\":\"" + _user.username + "\";\"password\":\"" + _user.password + "\";\"email\":\"" + _user.email + "\";\"id\":\"" + _user.id + "\";\"nickName\":\"" + _user.nickName + "\";\"role\":\"" + _user.role + "\"}"
    return line     
        
def LoadUserObjectFromFileByName(_username):
    global userObjectList
    for userObject in userObjectList:
        if userObject.username == _username:
            userObject.itemObjectList = LoadUserItems(userObject.itemList)
            userObject.purchasedItemsObjectList = LoadUserPurchasedItems(userObject.purchasedItemsList)
            userObject.favoriteObjectList = LoadUserFavoriteList(userObject.favoriteList)
            return userObject
    userObjectFile = open(os.getcwd()+"/data/userDatabase/Users/"+_username+"/userObject", "rb")
    userObject = pickle.load(userObjectFile)
    userObjectFile.close()
    userObject.itemObjectList = LoadUserItems(userObject.itemList)
    userObject.purchasedItemsObjectList = LoadUserPurchasedItems(userObject.purchasedItems)
    userObject.favoriteObjectList = LoadUserFavoriteList(userObject.favoriteList)
    if userObject not in userObjectList:
        userObjectList.append(userObject)
    return userObject

def LoadFullUserDatabase():
    global userList
    for user in userList:
        userObjectFile = open(os.getcwd()+"/data/userDatabase/Users/"+user.username+"/userObject", "rb")
        userObject = pickle.load(userObjectFile)
        userObjectFile.close()
        userObject.itemObjectList = LoadUserItems(userObject.itemList)
        userObjectList.append(userObject)
    return

def UpdateUserObjectList(_userObject):
    global userObjectList
    for userObject in userObjectList:
        if userObject.id == _userObject.id:
            userObject = _userObject
    return   

def GetItemSeller(_itemId):
    global itemList
    for item in itemList:
        if item.id == _itemId:
            return GetUserObjectById(item.userId)

def LikeSeller(_sellerId, _userId):
    userObject = GetUserObjectById(_userId)
    sellerObject = GetUserObjectById(_sellerId)
    if userObject.nickName != "Support":
        for userId in userObject.followingList:
            if userId == _sellerId:
                return
    sellerObject.carma += 1
    sellerObject.followerList.append(_userId)
    userObject.followingList.append(_sellerId)
    SaveUserObject(sellerObject)
    SaveUserObject(userObject)
    analytics.CalculateUserReputation(sellerObject)
    return

def ChangeWallet(_username, _password, _walletId):
    user = GetUserObjectByUserName(_username)
    if user.password == _password:
        line = "{\"id\":\"" + user.id+ "\";\"walletId\":\""+_walletId+"\"}"
        walletFile = open(os.getcwd()+"/data/userDatabase/Users/"+_username+"/wallet", "w")
        walletFile.write(line)
        walletFile.close()

def LoadUserWalletId(_userId):
    user = GetSimpleUserObjectById(_userId)
    try:
        walletFile = open(os.getcwd()+"/data/userDatabase/"+user.username+"/wallet" ,"r")
    except:
        print("[-]DATABASE: Can't load wallet file for user with id: " + user.id)
    try:
        line = walletFile.readlines()
        walletId = re.search(walletPattern, line).group(1)
    except:
        print("[-]DATABASE: Can't load walled id for user with id: " + user.id)

def AddItemToPurchasedList(_userId, _itemId):
    userObject = GetUserObjectById(_userId)
    userObject.purchasedItemsList.append(_itemId)
    SaveUserObject(userObject)

def UserNameAvailable(_username):
    global userList
    for user in userList:
        if user.username == _username:
            return False
    return True

def NickNameAvailabel(_nickName):
    global userList
    for user in userList:
        if user.nickName == _nickName:
            return False
    return True

def ComparePasswords(_pw1, _pw2):
    if _pw1 == _pw2:
        return True
    return False

####################################  I T E M S ####################################

def CreateItem(_userId, _itemName, _itemDiscription, _itemPrice, _itemGaleryList, _categories):
    item = modules.Item()
    item.id = CreateRandomId()
    categorieList = re.split(", ", _categories)
    item.categorie = categorieList[0]
    item.categorieList = categorieList
    item.userId = _userId
    item.name = _itemName
    item.price = _itemPrice
    item.discription = _itemDiscription
    userObject = GetUserObjectById(_userId)
    os.mkdir(os.getcwd()+"/static/items/" + item.id)
    if len(_itemGaleryList) > 0:
        item.picturePath = "/static/items/" + item.id + "/" + _itemGaleryList[0]
        for image in _itemGaleryList:
            item.galerieList.append("/static/items/" + item.id + "/" + image)
    os.mkdir(os.getcwd()+"/data/userDatabase/Users/"+userObject.username+"/items/"+item.id)
    userObject.itemList.append(item.id)
    userObject.itemObjectList.append(item)
    global itemList
    global itemObjectList
    if analytics.DetectDangerousItem(item.name, item.discription, _categories):
        item.status="dangerous"
        print("[!]WARNING: Dangerous item detected!\n[INFO]ITEM: Name >> " + item.name + "\n            Discription >> " + item.discription + "\n            Categories >> " + _categories + "\n            Seller-ID >> " + item.userId)
        WriteDangerousItemToDangerousItemDatabase(item)
    itemList.append(item)
    itemObjectList.append(item)
    UpdateUserObjectList(userObject)
    SaveUserObject(userObject)
    WriteItemToItemDatabase(item)
    SaveItemObjectToDisk(item)
    return item

def DeleteItem(_itemId):
    item = LoadItemObejctById(_itemId)
    userObject = GetUserObjectById(item.userId)
    userObject = RemoveItemFromUserItemLists(userObject, _itemId)
    imageFileNameList = os.listdir(itemPicturesPath + _itemId)
    for imageFileName in imageFileNameList:
        os.remove(itemPicturesPath + _itemId + "/" + imageFileName)
    os.rmdir(itemPicturesPath+_itemId)
    RemoveItemFromGlobalList(_itemId)
    RemoveItemFromItemDatabaseFile(_itemId)
    UpdateUserObjectList(userObject)
    SaveUserObject(userObject)
    
def RemoveItemFromUserItemLists(_userObject, _itemId):
    os.remove(os.getcwd()+"/data/userDatabase/Users/"+_userObject.username+"/items/"+_itemId+"/itemObject")
    os.rmdir(os.getcwd()+"/data/userDatabase/Users/"+_userObject.username+"/items/"+_itemId)
    for id in _userObject.itemList:
        print(id)
        if id == _itemId:
            _userObject.itemList.remove(id)
            break
    for itemObject in _userObject.itemObjectList:
        try:
            print(itemObject.id)
        except:
            print("no id for ", itemObject)
        if itemObject.id == _itemId:
            _userObject.itemObjectList.remove(itemObject)
            return _userObject
    return _userObject
    
def RemoveItemFromGlobalList(_itemId):
    global itemObjectList
    for itemObject in itemObjectList:
        if itemObject.id == _itemId:
            itemObjectList.remove(itemObject)
            

def RemoveItemFromItemDatabaseFile(_itemId):
    itemDatabaseFile = open(os.getcwd()+"/data/itemdatabase.db", "r")
    lines = itemDatabaseFile.readlines()
    itemDatabaseFile.close()
    newLines = ""
    for line in lines:
        if _itemId not in line:
            newLines += line# + "\n"
    itemDatabaseFile = open(os.getcwd()+"/data/itemdatabase.db", "w")
    itemDatabaseFile.writelines(newLines)
    itemDatabaseFile.close()
            

def ItemObjectToLine(_item):
    line = "{\"itemId\":\""+_item.id+"\";\"userId\":\""+_item.userId+"\"}"
    return line

def WriteItemToItemDatabase(_item):
    itemDatabaseFile = open(os.getcwd()+"/data/itemdatabase.db", "a")
    itemDatabaseFile.write(ItemObjectToLine(_item)+"\n")
    itemDatabaseFile.close()
    
def LineToItemObject(_line):
    result = re.search(itemPattern, _line)
    itemObjectFile = open(os.getcwd()+"/data/userDatabase/Users/"+result.group(2)+"/items/"+result.group(1)+"/itemObject", "rb")
    itemObject = pickle.load(itemObjectFile)
    itemObjectFile.close()
    return itemObject

def SaveItemObjectToDisk(_item):
    itemObjectFile = open(os.getcwd()+"/data/userDatabase/Users/"+GetUserObjectById(_item.userId).username+"/items/"+_item.id+"/itemObject", "wb")
    pickle.dump(_item, itemObjectFile)
    itemObjectFile.close()

def WriteDangerousItemToDangerousItemDatabase(_item):
    dangerousItemDatabaseFile = open(os.getcwd()+"/data/__/dangerousitemdatabase.db", "a")
    dangerousItemDatabaseFile.write(ItemObjectToLine(_item)+"\n")
    dangerousItemDatabaseFile.close()
    return

def RemoveDangerousItemFromDangerousItemDatabase(_itemId):
    dangerousItemDatabaseFile = open(os.getcwd()+"/data/__/dangerousitemdatabase.db", "r")
    lines = dangerousItemDatabaseFile.readlines()
    if lines == "":return
    dangerousItemDatabaseFile.close()
    newLines = ""
    for line in lines:
        if re.search(itemPattern, line).group(1) != _itemId:
            newLines += line+"\n"
    dangerousItemDatabaseFile = open(os.getcwd()+"/data/__/dangerousitemdatabase.db", "w")
    dangerousItemDatabaseFile.writelines(newLines)
    dangerousItemDatabaseFile.close()
   

def LoadAllItems():
    itemDatabaseFile = open(os.getcwd()+"/data/itemdatabase.db", "r")
    lines = itemDatabaseFile.readlines()
    itemDatabaseFile.close()
    global itemList
    itemList.clear()
    for line in lines:
        result = re.search(itemPattern, line)
        item = modules.Item()
        item.id = result.group(1)
        item.userId = result.group(2)
        itemList.append(item)
    return        
          
def LoadItemObejctById(_itemId):
    global itemObjectList
    for itemObject in itemObjectList:
        if itemObject.id == _itemId:
            return itemObject
    global itemList
    for item in itemList:
        if item.id == _itemId:
            return LoadItemObjectFromDisk(item)
    return "invalid"
            
def LoadItemObjectFromDisk(_item):
    itemObjectFile = open(os.getcwd()+"/data/userDatabase/Users/"+GetUserObjectById(_item.userId).username+"/items/"+_item.id+"/itemObject", "rb")
    itemObject = pickle.load(itemObjectFile)
    itemObjectFile.close()
    return itemObject

def LoadItemObjectFromDiskByItemList():
    global itemObjectList
    global itemList
    itemObjectList.clear()
    for item in itemList:
        itemObjectFile = open(os.getcwd()+"/data/userDatabase/Users/"+GetSimpleUserObjectById(item.userId).username+"/items/"+item.id+"/itemObject", "rb")
        itemObject = pickle.load(itemObjectFile)
        itemObjectFile.close()
        itemObjectList.append(itemObject)
    return

def LoadUserItems(_itemList):
    itemObjectList = []
    for itemId in _itemList:
        itemObjectList.append(LoadItemObejctById(itemId))
    return itemObjectList

def LoadUserPurchasedItems(_itemList):
    itemObjectList = []
    for itemId in _itemList:
        itemObjectList.append(LoadItemObejctById(itemId))
    return itemObjectList

def LoadUserFavoriteList(_itemList):
    itemObjectList = []
    for itemId in _itemList:
        itemObjectList.append(LoadItemObejctById(itemId))
    return itemObjectList  

def AddItemToUsersCard(_itemId, _username):
    itemObject = LoadItemObejctById(_itemId)
    userObject = GetUserObjectByUserName(_username)
    userObject.cardList.append(itemObject)
    return True  

def RemoveItemFromCard(_userId, _itemId):
    userObject = GetUserObjectById(_userId)
    for itemObject in userObject.cardList:
        if itemObject.id == _itemId:
            userObject.cardList.remove(itemObject)
            return True
    return False

def AddCommentToItem(_itemId, _username, _commentTitle, _commentText):
    userObject = GetSimpleUserObjectByUserName(_username)
    item = LoadItemObejctById(_itemId)
    comment = modules.CommentObject()
    comment.id = CreateRandomId()
    comment.itemId = item.id
    comment.writerId = userObject.id
    comment.writerNickName = userObject.nickName
    comment.title = _commentTitle
    comment.text = _commentText
    comment.createdOn = TimeStampToTimeString(CreateTimeStamp())
    for item in userObject.purchasedItemsList:
        if item.id == comment.itemId:
            comment.verifiedPurchase = True
    item.commentList.append(comment)
    SaveItemObjectToDisk(item)

def LikeItem(_itemId, _userId):
    userObject = GetUserObjectById(_userId)
    item = LoadItemObejctById(_itemId)
    if userObject.nickName == "Support":
        item.upVotes += 1
        item.rating = analytics.CalculateItemRating(item)
        SaveItemObjectToDisk(item)
        return item
    for itemId in userObject.likedItemList:
        if itemId == item.id:
            return item
    item.upVotes += 1
    item.rating = analytics.CalculateItemRating(item)
    SaveItemObjectToDisk(item)
    userObject.favoriteList.append(item.id)
    SaveUserObject(userObject)
    return item

def DissLikeItem(_itemId, _userId):
    userObject = GetUserObjectById(_userId)
    item = LoadItemObejctById(_itemId)
    if userObject.nickName == "Support":
        item.downVotes += 1
        item.rating = analytics.CalculateItemRating(item)
        SaveItemObjectToDisk(item)
        return item
    for itemId in userObject.dissLikedItemList:
        if itemId == item.id:
            return item
    item.downVotes += 1
    item.rating = analytics.CalculateItemRating(item)
    SaveItemObjectToDisk(item)
    RemoveFavoriteFromList(_userId, item.id)
    return item

def SearchItem(_searchTerm):
    if _searchTerm == "":
        return RandomResultList()
    global itemObjectList
    _searchTerm = str.lower(_searchTerm)
    tempItemObjectList = itemObjectList.copy()
    resultList = []
    for item in tempItemObjectList:
        gotcha = False   
        if _searchTerm in str.lower(item.name):
            resultList.append(item)
            tempItemObjectList.remove(item)
            gotcha = True
        if _searchTerm in item.discription and gotcha == False:
            resultList.append(item)
            tempItemObjectList.remove(item)
            gotcha = True
        searchTermList = re.split("\s", _searchTerm)
        if gotcha == False:
            for searchTerm in searchTermList:
                if searchTerm in str.lower(item.name) and gotcha == False:
                    resultList.append(item)
                    tempItemObjectList.remove(item)
                    gotcha = True
                if searchTerm == item.categorie and gotcha == False:
                    resultList.append(item)
                    tempItemObjectList.remove(item)
    return resultList

def AdvancedItemSearch(_searchTerm , _categorie, _priceFrom, _priceTo, _command):
    global itemObjectList
    _searchTerm = str.lower(_searchTerm)
    tempItemObjectList = itemObjectList.copy()
    resultList = []
    for item in tempItemObjectList:
        gotcha = False   
        if _searchTerm in str.lower(item.name):
            resultList.append(item)
            tempItemObjectList.remove(item)
            gotcha = True
        if _searchTerm in item.discription and gotcha == False:
            resultList.append(item)
            tempItemObjectList.remove(item)
            gotcha = True
        searchTermList = re.split("\s", _searchTerm)
        if gotcha == False:
            for searchTerm in searchTermList:
                if searchTerm in str.lower(item.name) and gotcha == False:
                    resultList.append(item)
                    tempItemObjectList.remove(item)
                    gotcha = True
                if searchTerm == item.categorie and gotcha == False:
                    resultList.append(item)
                    tempItemObjectList.remove(item)
    if _priceTo != "":
        sortedList = []
        _priceTo = int(_priceTo)
        for item in resultList:
            if int(item.price) < _priceTo:
                sortedList.append(item)
        return sortedList
    return resultList

def RandomResultList():
    global itemObjectList
    tempList = itemObjectList.copy()
    resultList = []
    for i in range(len(tempList)):
        randomNumber = random.randint(0, len(tempList)-1)
        resultList.append(tempList[randomNumber])
        tempList.remove(tempList[randomNumber])
    return resultList
        

def AddItemToFavoriteList(_itemId, _userId):
    userObject = GetUserObjectById(_userId)
    userObject.favoriteList.append(_itemId)
    SaveUserObject(userObject)

def RemoveFavoriteFromList(_userId, _itemId):
    userObject = GetUserObjectById(_userId)
    for itemId in userObject.favoriteList:
        if itemId == _itemId:
            userObject.favoriteList.remove(itemId)
    SaveUserObject(userObject)

def GetUserFavoriteList(_userId):
    global userObjectList
    global itemObjectList
    for userObject in userObjectList:
        if userObject.id == _userId:  
            favList = []
            for itemId in userObject.favoriteList:
                for item in itemObjectList:
                    if item.id == itemId:
                        favList.append(item)
            return favList

def RemovePictureFromItem(_itemId, _picturePath):
    item = LoadItemObejctById(_itemId)
    if len(item.galerieList) < 2:
        return item
    for picturePath in item.galerieList:
        if picturePath == _picturePath:
            item.galerieList.remove(picturePath)
            os.remove(os.getcwd()+_picturePath)
            
    if item.picturePath == _picturePath:
        item.picturePath = item.galerieList[0]
    SaveItemObjectToDisk(item)
    return item    

#################### UTILITY ####################
def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()

def CreateMD5Hash(_input):
    return hashlib.md5(_input.encode()).hexdigest()

def CheckCredentials(_username, _password):
    global userList
    for user in userList:
        if user.username == _username and user.password == _password: return True 
    return False

def GetCookieData(_cookieValue):
    if _cookieValue == None:
        return "",""
    result = re.search(cookiePattern, _cookieValue)
    username = result.group(1)
    password = result.group(2)
    return username, password

def GetFileName(_file):
    result = re.search(fileNamePattern, _file)
    fileName = result.group(1)
    return fileName

def CreateTimeStamp():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def GetGlobalUserObjectList():
    global userObjectList
    return userObjectList

def GetGlobalItemList():
    global itemObjectList
    return itemObjectList

#################### H E L P E R ####################
def DeleteUser(_userId):
    global userList 
    tempItemList = []
    for user in userList:
        if user.id == _userId:
            userObject = GetUserObjectById(user.id)
            tempItemList = userObject.itemList.copy()
            for itemId in tempItemList:
                DeleteItem(itemId)
            os.remove(os.getcwd()+"/data/userDatabase/Users/"+user.username+"/userObject")
            os.rmdir(os.getcwd()+"/data/userDatabase/Users/"+user.username+"/items")
            os.rmdir(os.getcwd()+"/data/userDatabase/Users/"+user.username)
            userList.remove(user)
    lines = ""
    for user in userList:
        lines += UserToLine(user)+"\n"
    userDatabaseFile = open(os.getcwd()+"/data/userDatabase/userdatabase.db","w")
    userDatabaseFile.writelines(lines)
    userDatabaseFile.close()
    
def DeleteCommentFromItemObject():       
    InitDB()
    itemId = input("Enter item-id: ")
    global itemObjectList
    for itemObject in itemObjectList:
        if itemObject.id == itemId:
            commentId = input("Enter comment-id: ")
            for comment in itemObject.commentList:
                if comment.id == commentId:
                    itemObject.commentList.remove(comment)
                    
def CreateRandomPopularItemsList():
    global itemObjectList
    global popularItemsList
    tempList = itemObjectList.copy()
    popularItemsList.clear()
    loopRange = 4
    if len(tempList) < loopRange:
        loopRange = len(tempList)
    for i in range(loopRange):
        randomNumber = random.randint(0, len(tempList)-1)
        popularItemsList.append(tempList[randomNumber])
        tempList.remove(tempList[randomNumber])
    return popularItemsList
            
def CreateRandomSponsoredItemsList():
    global itemObjectList
    global sponsoredItemsList
    tempList = itemObjectList.copy()
    sponsoredItemsList.clear()
    loopRange = 3
    if len(tempList) < loopRange:
        loopRange = len(tempList)
    for i in range(loopRange):
        randomNumber = random.randint(0, len(tempList)-1)
        sponsoredItemsList.append(tempList[randomNumber])
        tempList.remove(tempList[randomNumber])
    return sponsoredItemsList

def TimeStampToTimeString(_timeStamp):
    timeString = ""
    result = re.search(timePattern, _timeStamp)
    timeString = result.group(3) + "." + result.group(2) + "." + result.group(1) + " - " + result.group(4) + ":" + result.group(5)
    return timeString