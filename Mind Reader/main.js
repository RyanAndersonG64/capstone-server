//initial conditions, starts app on home screen with appropriate text and buttons
let activeScreen = 0;
updateButtons();
createSymbolsList();
document.querySelector("#symbolsList").style.visibility="hidden";

function saveScreen(){ //stores active screen to be read if page is refreshed
        sessionStorage.setItem("refresh", "true");
        sessionStorage.setItem("storedScreen", activeScreen);
}

window.onload = function() { //if page is refreshed, it loads the active screen instead of the home screen
    let refreshing = sessionStorage.getItem("refresh");
    if (refreshing) {
        activeScreen = sessionStorage.getItem("storedScreen");
        updateButtons();
        updateText();
        showHideSymbols();
    }
}

//the active screen will display the corresponding strings from the following arrays; an empty string means that that page should have no text in that location
let topTextArray = ['I can read your mind!', 'Choose a number from 0-99', 'Add both digits together to get a new number', 'Subtract the second number from the first', 'Placeholder for bottom text position', "Your number's symbol is"];
let bottomTextArray = ["Press GO to begin", "Once you've thought of a number, click NEXT", "For example: 14 --> 1 + 4 = 5 7 --> 0 + 7", "For example: 14 - 5 = 9", "Find the symbol corresponding to your new number (scroll or use 'ctrl + F' to find large numbers", ""];
let pageNumbersArray = ["1 of 6", "2 of 6", "3 of 6", "4 of 6", "5 of 6", "6 of 6"];

function createSymbolsList(){ //generates list of numbers and symbols
    let numbersArray = []; //creates an array with numbers 0-99 for generating list of numbers and corresponding symbols
    for (let i = 0; i <= 99; i++) {
        numbersArray[i] = i;
    }
    let symbolsArray = ["~\n", "!\n", "@\n", "#\n", "$\n", "%\n", "^\n", "&\n", "*\n"]; //creates array with symbols to match numbers with
    for (i = numbersArray[0]; i <= numbersArray[numbersArray.length-1]; i++) {
        let symbolForNumber = symbolsArray[numbersArray[i] % 9];
        document.querySelector("#symbolsList").textContent += numbersArray[i] + " = " +  symbolForNumber;
    }
}

function updateButtons(){ //changes button text and/or visibility when active screen changes
if (activeScreen == 0 || activeScreen == 5) {
    document.querySelector("#nextButton").style.visibility="hidden";
} else {
    document.querySelector("#nextButton").style.visibility="visible";
}
if (activeScreen == 0) {
    document.getElementById("goResetButton").textContent="GO";
} else if (activeScreen == 5) {
    document.getElementById("goResetButton").textContent="PLAY AGAIN";
} else {
    document.getElementById("goResetButton").textContent="RESET";
}
if (activeScreen == 5) {
    document.getElementById("numberSymbol").textContent="~";
} else {
    document.getElementById("numberSymbol").textContent="";
}
if (activeScreen == 4) {
    document.getElementById("nextButton").textContent="REVEAL";
} else if (activeScreen == 1 || activeScreen == 2 || activeScreen == 3) {
    document.getElementById("nextButton").textContent="NEXT";
}
}

function updateText() { //changes page and button text to that of the new active screen
    document.getElementById("topText").textContent=topTextArray[activeScreen];
    document.getElementById("bottomText").textContent=bottomTextArray[activeScreen];
    document.getElementById("pageNumber").textContent=pageNumbersArray[activeScreen];
    if (activeScreen == 4) {
        document.querySelector("#topText").style.visibility="hidden";
    } else {
        document.querySelector("#topText").style.visibility="visible";
    }
}

function showHideSymbols() { //displays list of symbols on the appropriate page and hides it on other pages
    if (activeScreen == 4) {
        document.querySelector("#symbolsList").style.visibility="visible";
    } else {
        document.querySelector("#symbolsList").style.visibility="hidden";
    }
}

function goReset() { //if on home screen, starts game when "GO" button is clicked; otherwise, "GO" button becomes "RESET" button and resets to home screen
    if (activeScreen == 0) {
        activeScreen = 1;
    } else {
        activeScreen = 0;
    }
    updateText();
    updateButtons();
    showHideSymbols();
    saveScreen();
}

function nextScreen() { //move to next screen when "NEXT" button is clicked
    activeScreen++;
    updateText();
    updateButtons();
    showHideSymbols();
    saveScreen();
}

function pageNavigationForwards() { //move to next screen when forward arrow is clicked
    if (activeScreen == 5) {
        activeScreen = 0;
        updateText();
        updateButtons();
        saveScreen();
    } else {
        nextScreen();
    }
}

function pageNavigationBackwards() { //move to previous screen when backward arrow is clicked
    if (activeScreen == 0) {
        activeScreen = 5;
    } else {
        activeScreen--;
    }
    updateText();
    updateButtons();
    showHideSymbols();
    saveScreen();
}

function navigateHome() { //move to home screen when home icon is clicked
    activeScreen = 0;
    updateText();
    updateButtons();
    showHideSymbols();
    saveScreen();
}

document.querySelector("#goResetButton").addEventListener("click", goReset)
document.querySelector("#nextButton").addEventListener("click", nextScreen)
document.querySelector("#forwardButton").addEventListener("click", pageNavigationForwards)
document.querySelector("#backwardButton").addEventListener("click", pageNavigationBackwards)
document.querySelector("#homeButton").addEventListener("click", navigateHome)
