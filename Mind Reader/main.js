let activeScreen = 0;
updateButtons();
document.querySelector(".symbolsList").style.visibility="hidden";

let topTextArray = ['I can read your mind!', 'Pick a number from 0-99, inclusive', 'Add both digits together to get a new number', 'Subtract the second number from the first', 'Placeholder for bottom text position', "Your number's symbol is"];
let bottomTextArray = ["Press GO to begin", "Once you've thought of a number, click NEXT", "For example: 14 --> 1 + 4 = 5 7 --> 0 + 7", "ex: 14 - 5 = 9", "Find the symbol corresponding to your new number", ""];
let pageNumbersArray = ["1 of 6", "2 of 6", "3 of 6", "4 of 6", "5 of 6", "6 of 6"];

function updateButtons(){
if (activeScreen == 0 || activeScreen == 5) {
    document.querySelector("#nextButton").style.visibility="hidden";
} else {
    document.querySelector("#nextButton").style.visibility="visible";
}
if (activeScreen == 0) {
    document.getElementById("goResetButton").textContent="GO";
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
function updateText() {
    document.getElementById("topText").textContent=topTextArray[activeScreen];
    document.getElementById("bottomText").textContent=bottomTextArray[activeScreen];
    document.getElementById("pageNumber").textContent=pageNumbersArray[activeScreen];
    if (activeScreen == 4) {
        document.querySelector("#topText").style.visibility="hidden";
    } else {
        document.querySelector("#topText").style.visibility="visible";
    }
}

function showHideSymbols() {
    if (activeScreen == 4) {
        document.querySelector(".symbolsList").style.visibility="visible";
    } else {
        document.querySelector(".symbolsList").style.visibility="hidden";
    }
}

function goReset() {
    if (activeScreen == 0) {
        activeScreen = 1;
    } else {
        activeScreen = 0;
    }
    updateText();
    updateButtons();
    showHideSymbols();
}

function nextScreen() {
    activeScreen++;
    updateText();
    updateButtons();
    showHideSymbols();
}

function pageNavigationForwards() {
    if (activeScreen == 5) {
        activeScreen = 0;
        updateText();
        updateButtons();
    } else {
        nextScreen();
    }
}

function pageNavigationBackwards() {
    if (activeScreen == 0) {
        activeScreen = 5;
    } else {
        activeScreen--;
    }
    updateText();
    updateButtons();
    showHideSymbols();
}

function navigateHome() {
    activeScreen = 0;
    updateText();
    updateButtons();
    showHideSymbols();
}

document.querySelector("#goResetButton").addEventListener("click", goReset)
document.querySelector("#nextButton").addEventListener("click", nextScreen)
document.querySelector("#forwardButton").addEventListener("click", pageNavigationForwards)
document.querySelector("#backwardButton").addEventListener("click", pageNavigationBackwards)
document.querySelector("#homeButton").addEventListener("click", navigateHome)
