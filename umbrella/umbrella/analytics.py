import os, re
from umbrella import database, modules

def CalculateUserReputation(_userObject):
    upCounter = 0
    downCounter = 0
    for itemId in _userObject.itemList:
        item = database.LoadItemObejctById(itemId)
        upCounter += int(item.upVotes)
        downCounter += int(item.downVotes)
    _userObject.reputation = int(round((upCounter / (upCounter + downCounter) * 100),0)) + _userObject.carma                     
    database.SaveUserObject(_userObject)
    return _userObject
    
def CalculateItemRating(item):
    if item.downVotes < 1:
        return 100
    sellerObject = database.GetItemSeller(item.id)
    CalculateUserReputation(sellerObject)
    return int(round((item.upVotes / (item.downVotes + item.upVotes) * 100),0))

def DetectDangerousItem(_itemName, _itemDiscription, _itemCategorie):
    _itemName = str.lower(_itemName)
    _itemDiscription = str.lower(_itemDiscription)
    _itemCategorie = str.lower(_itemCategorie)
    itemText = _itemName + " " + _itemDiscription + " " + _itemCategorie
    alertLevel = 0
    if "child" in itemText:
        alertLevel += 3
    if "kid" in itemText:
        alertLevel += 3
    if "young" in itemText:
        alertLevel += 2
    if "boy" in itemText:
        alertLevel += 1
    if "girl" in itemText:
        alertLevel += 1
    if "porn" in itemText:
        alertLevel += 3
    if "sex" in itemText:
        alertLevel += 2
    if "prostitution" in itemText:
        alertLevel += 3
    if "worker" in itemText:
        alertLevel += 2
    if "naked" in itemText:
        alertLevel += 1
    if "pictures" in itemText:
        alertLevel += 2
    if "videos" in itemText:
        alertLevel += 2
    if alertLevel > 5:
        return True
    return False
        
    
    