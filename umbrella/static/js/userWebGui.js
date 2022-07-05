const addItemContainer = document.querySelector(".addItemContainer")
const openAddItemContainer = document.querySelector(".openAddItemContainer")
const favoriteItemsContainer = document.querySelector(".favoriteItemsContainer")
const openFavoriteItemsContainer = document.querySelector(".openFavoriteItemsContainer")
const purchasedItemsContainer = document.querySelector(".purchasedItemsContainer")
const openPurchasedItemsContainer = document.querySelector(".openPurchasedItemsContainer")
const forSaleItemsContainer = document.querySelector(".forSaleItemsContainer")
const openForSaleItemsContainer = document.querySelector(".openForSaleItemsContainer")
const editUserContainer = document.querySelector(".editUserContainer")
const openEditUserContainer = document.querySelector(".openEditUserContainer")
const hiddenInput = document.querySelector(".hiddenInput")
const showPasswordForDeleteUserContainer = document.querySelector(".showPasswordForDeleteUserContainer")
const hiddenWalletInput = document.querySelector(".hiddenWalletInput")
const showChangeWalletContainer = document.querySelector(".showChangeWalletContainer")
const changeContainer = document.querySelector(".changeContainer")

function OpenAddItemContainer(){

    hiddenInput.style.display="none"
    showPasswordForDeleteUserContainer.style.display = "initial"
    favoriteItemsContainer.style.display = "none"
    purchasedItemsContainer.style.display = "none"
    forSaleItemsContainer.style.display = "none"
    editUserContainer.style.display = "none"
    addItemContainer.style.display = "initial"
    
}

openAddItemContainer.addEventListener("click", OpenAddItemContainer)

function OpenFavoriteItemsContainer(){

    hiddenInput.style.display="none"
    showPasswordForDeleteUserContainer.style.display = "initial"
    addItemContainer.style.display = "none"
    purchasedItemsContainer.style.display = "none"
    forSaleItemsContainer.style.display = "none"
    editUserContainer.style.display = "none"
    favoriteItemsContainer.style.display = "initial"
}

openFavoriteItemsContainer.addEventListener("click", OpenFavoriteItemsContainer)

function OpenPurchasedItemsContainer(){

    hiddenInput.style.display="none"
    showPasswordForDeleteUserContainer.style.display = "initial"
    addItemContainer.style.display = "none"
    favoriteItemsContainer.style.display = "none"
    forSaleItemsContainer.style.display = "none"
    editUserContainer.style.display = "none"
    purchasedItemsContainer.style.display = "initial"
}

openPurchasedItemsContainer.addEventListener("click", OpenPurchasedItemsContainer)

function OpenForSaleItemsContainer(){

    hiddenInput.style.display="none"
    showPasswordForDeleteUserContainer.style.display = "initial"
    addItemContainer.style.display = "none"
    favoriteItemsContainer.style.display = "none"
    purchasedItemsContainer.style.display = "none"
    editUserContainer.style.display = "none"
    forSaleItemsContainer.style.display = "initial"
}

openForSaleItemsContainer.addEventListener("click", OpenForSaleItemsContainer)

function OpenEditUserContainer(){

    hiddenInput.style.display="none"
    hiddenWalletInput.style.display="none"
    showPasswordForDeleteUserContainer.style.display = "initial"
    showChangeWalletContainer.style.display = "initial"
    addItemContainer.style.display = "none"
    favoriteItemsContainer.style.display = "none"
    purchasedItemsContainer.style.display = "none"
    forSaleItemsContainer.style.display = "none"
    editUserContainer.style.display = "initial"
    changeContainer.style.display="flex"
}

openEditUserContainer.addEventListener("click", OpenEditUserContainer)

function ShowHiddenInputContainer(){
    showPasswordForDeleteUserContainer.style.display="none"
    hiddenInput.style.display="initial"
    
}

showPasswordForDeleteUserContainer.addEventListener("click", ShowHiddenInputContainer)

function ShowChangeWalletContainer(){
    showChangeWalletContainer.style.display="none"
    showPasswordForDeleteUserContainer.style.display="none"
    changeContainer.style.display="none"
    hiddenWalletInput.style.display="initial"
    
}

showChangeWalletContainer.addEventListener("click", ShowChangeWalletContainer)