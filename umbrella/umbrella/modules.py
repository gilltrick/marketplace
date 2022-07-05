class User():
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""
        self.favoriteList = []
        self.favoriteObjectList = []
        self.historyList = []
        self.loginStampList = []
        self.ipLoginList = []
        self.itemList = []
        self.itemObjectList = []
        self.id = ""
        self.nickName = ""
        self.role = ""
        self.cardList = []
        self.purchasedItemsList = []
        self.purchasedItemsObjectList = []
        self.followerList = []
        self.followingList = []
        self.unreadConversationsList = []
        self.writtenCommentsList = []
        self.likedItemList = []
        self.dissLikedItemList = []
        self.commentList = []
        self.upVotes = 0
        self.downVotes = 0
        self.reputation = 0
        self.carma = 0
        self.saleObjectList = []
        
class Item():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.price = 0
        self.acutionPrice = 0
        self.discription = ""
        self.picturePath = ""
        self.galerieList = []
        self.userId = ""
        self.soldOut = False
        self.available = False
        self.bidderList = []
        self.categorie = ""
        self.categorieList = []
        self.commentList = []
        self.upVotes = 0
        self.downVotes = 0
        self.rating = 0
        self.sellCounter = 0
        self.listed = True
        self.status = ""

class Conversation:
    def __init__(self):
        self.starterId = ""
        self.participentId = ""
        self.senderUserName = ""
        self.participentUsername = ""
        self.participentNickName = ""
        self.messageList = []
        self.id = ""
        self.read = False
        
class Message:
    def __init__(self):
        self.senderId = ""
        self.receiverId = ""
        self.senderUserName = ""
        self.receiverUserName = ""
        self.titleText = ""
        self.messageText = ""
        self.timeStamp = ""
        self.senderNickName = ""
        self.id = ""
        self.conversationId = ""
        self.offer = ""
        self.read = False
        self.link = ""
        
    def CreateMessage(_senderId, _receiverId, _senderUserName, _receiverUserName, _titleText, _messageText, _timeStamp, _senderNickName):
        message = Message()
        message.senderId = _senderId
        message.receiverId = _receiverId
        message.senderUserName = _senderUserName
        message.receiverUserName = _receiverUserName
        message.titleText = _titleText
        message.messageText = _messageText
        message.timeStamp = _timeStamp
        message.senderNickName = _senderNickName
        return message     
    
class CustomSale:
    def __init__(self):
        self.id = ""
        self.sellerId = ""
        self.buyerId = ""
        self.timeStamp = ""
        self.offerTitle = ""
        self.offerText = ""
        self.status = ""
        self.offerPrice = ""
        
class CommentObject:
    def __init__(self):
        self.title = ""
        self.text = ""
        self.writerId = ""
        self.writerNickName = ""
        self.createdOn = ""
        self.upVotes = ""
        self.downVotes = ""
        self.id = ""
        self.itemId = ""
        self.verifiedPurchase = False

class SaleObject:
    def __init__(self):
        self.id = ""
        self.createdOn = ""
        self.itemId = ""
        self.sellerId = ""
        self.buyerId = ""
        self.buyerData = {}
        self.status = ""
        