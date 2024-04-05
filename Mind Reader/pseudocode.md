scroll through different screens on the same page 
    use global screen variable
    if/else or switch to display content corresponding to value of screen variable
    
    screens consist of instructions, 'next' button, help text, and go/reset button

click event for 'next' button to move to next screen

'start' button on first screen becomes 'reset' button for future pages
    if screen == 1
        button = go
    else
        button = reset

display symbols for each number

generate list of symbols and numbers:
    for loop to create array filled with numbers from 0 - 99
    create array with symbols
    function to create list items by combining numbers and symbols using %