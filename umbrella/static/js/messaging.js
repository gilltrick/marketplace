const normalMessage = document.querySelector(".normalMessage")
const showOfferMessageButton = document.querySelector(".showOfferMessageButton")
const offerMessage = document.querySelector(".offerMessage")
const showNormalMessageButton = document.querySelector(".showNormalMessageButton")

const _showNormalMessageButton = document.querySelector("._showNormalMessageButton")

document.querySelector(".container").scrollTop = 99999

function ShowOfferMessage(){
    normalMessage.style.display = "none"
	offerMessage.style.display = "block"

}

showOfferMessageButton.addEventListener("click", ShowOfferMessage)

function ShowNormalMessage(){
    offerMessage.style.display = "none"
	normalMessage.style.display = "block"

}

showNormalMessageButton.addEventListener("click", ShowNormalMessage)


function _ShowNormalMessage(){

    offerMessage.style.display = "none"
	normalMessage.style.display = "block"

}
_showNormalMessageButton.addEventListener("click", _ShowNormalMessage)