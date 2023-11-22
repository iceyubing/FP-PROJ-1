"""
Group Number: FP24
Students: [Yubing Chen (52915)], [Sona Moravcikova (62932)]
Project 2
"""
import random
#######################################################
####################  FUNCTIONS  ######################
#######################################################        

def askForExpertise():
    """
    Ask user to select their expertise level.
    
    Returns
    -------
    integer
       An integer, in the interval [MAX_EXPERT, LESS_EXPERT].
    """
    
    while True:
        try:
            expertise = int(input("Expert level - from 1 (radical) to 5 (beginner)? "))
            if MAX_EXPERT <= expertise <= LESS_EXPERT:
                return expertise
            else:
                print("Please enter an expertise level between 1 and 5.")
        except ValueError:
            print("Please enter a valid integer.")
    
# *****************************************************
def buildGameBottles(expertise):
    """
    Build and return a dictionary containing the information of each bottle in the game.

    Parameters
    ----------
    expertise : integer
        The user's expertise level.

    Returns
    -------
    dictionary
        A dictionary where each bottle is represented by a letter (key) and contains a list of symbols.
    """
    N = NR_BOTTLES - expertise
    symbols_to_distribute = [symbol for symbol in SYMBOLS[:N] for _ in range(8)]

    assert len(symbols_to_distribute) == N * CAPACITY

    random.shuffle(symbols_to_distribute)
    bottles = {letter: [] for letter in LETTERS}

    
    while symbols_to_distribute:
        for bottle in random.sample(LETTERS, len(LETTERS)):
            if len(bottles[bottle]) < CAPACITY and symbols_to_distribute:
                symbol = symbols_to_distribute.pop()
                bottles[bottle].append(symbol)

    
    for bottle in bottles.keys():
        while len(bottles[bottle]) < CAPACITY:
            bottles[bottle].insert(0, ' ')  

    return bottles
# *****************************************************
def showBottles(bottles,nrErrors):
    """
    Display a representation of the bottles and the number of errors in the game.

    Parameters
    ----------
    bottles : dict
        A dictionary containing information about the game bottles.
    nrErrors : integer
        Number of errors the user has committed.

    Returns
    -------
    None
    """
    
    column_names = list(LETTERS)
    print("  " + "     ".join(column_names))
    
    for row_index in range(CAPACITY):
        row = "| |".join([f" {bottles[column][row_index]} " for column in column_names])
        print("|" +row + "|")
        
    print(f"NUMBER OF ERRORS: {nrErrors}")
   
# *****************************************************
def askForPlay():
    """
    Asks user for letters that identify the source and destination bottles.
   
    Returns
    -------
    2 Strings 
       Two strings containing the source and destination letters.
       
    """
    source = input("Source bottle? ").upper()
    
    while not (len(source) == 1 and 'A' <= source <= 'J'):
        print("Please enter a valid single uppercase letter (A to J).")
        source = input("Source bottle? ").upper()

    while True:
            destin = input("Destination bottle? ").upper()

            if len(destin) == 1 and 'A' <= destin <= 'J':
                return source, destin
            else:
                print("Please enter a valid single uppercase letter (A to J).")
                
# *****************************************************
def moveIsPossible(source, destin, bottles):
    """
    Check if a move from the source bottle to the destination bottle is possible.

    Parameters
    ----------
    source : str
        The letter identifying the source bottle.
    destin : str
        The letter identifying the destination bottle.
    bottles : dict
        A dictionary containing the game's bottles and their contents.

    Returns
    -------
    bool
        True if the move is possible, False otherwise.
    """
    # Check if source and destination bottles are the same
    if source == destin:
       return False
        
    # Check if both bottles exist
    if source not in bottles or destin not in bottles:
        return False

    # Check if source bottle is empty
    if bottles[source] == [' ' for _ in range(8)]:
        return False

    # Check if destination bottle is full
    if full(bottles[destin]):  # Assuming a maximum capacity
        return False

    # Check if the top symbol of both bottles is the same
    sourceTop = topOfBottle(source)  #position of top
    destinTop = topOfBottle(destin)  #position of top
    if destinTop:
        if bottles[destin] and bottles[source][sourceTop] != bottles[destin][destinTop]:
            return False

    return True

# *****************************************************
def topOfBottle(letter):
    """
    Find the position of the top non-empty symbol in the specified bottle.

    Parameters
    ----------
    letter : str
        The letter identifying the bottle.

    Returns
    -------
    int or None
        The position of the top non-empty symbol (0-indexed) or None if the bottle is empty.
    """
    return next((i for i, symbol in enumerate(bottles[letter]) if symbol != ' '), None)

#************************************************************
def howManyEqualInTop(source, destin):
    """
    Count the number of equal symbols at the top of two bottles.

    Parameters
    ----------
    source : str
        The identifier of the source bottle.
    destin : str
        The identifier of the destination bottle.

    Returns
    -------
    int
        The number of equal symbols at the top of the two bottles.
    """
    num_transferable = 0
    index_a = index_b = 0

    # Skip initial spaces in both pillars
    while index_a < len(source) and source[index_a] == ' ':
        index_a += 1
    while index_b < len(destin) and destin[index_b] == ' ':
        index_b += 1

    # Compare the numbers starting from the first non-space character
    while index_a < len(source) and index_b < len(destin):
        if source[index_a] == destin[index_b]:
            num_transferable += 1  
            index_a += 1
        else:
            break
    if num_transferable == 0:
        num_transferable += 1
        while index_a < len(source) - 1:
            if source[index_a] == source[index_a + 1]:
                index_a += 1
                num_transferable += 1
            else:
                break

    return num_transferable

#************************************************************
def doMove(source, destin, bottles):
    """
    Transfers as many symbols as possible from the source bottle to the destination bottle.

    Parameters
    ----------
    source : str
        The identifier of the source bottle.
    destin : str
        The identifier of the destination bottle.
    bottles : dict
        A dictionary containing the information of each bottle in the game.

    Returns
    -------
    None
    """
    # Find the top symbol index in both source and destination bottles
    destin_index = next((i for i, symbol in enumerate(bottles[destin]) if symbol != ' '), None)
    source_index = next((i for i, symbol in enumerate(bottles[source]) if symbol != ' '), None)
    # If the destination bottle is empty, set the index to its capacity
    if destin_index is None:
        destin_index = CAPACITY

    # Transfer symbols
    num_transferable = howManyEqualInTop(bottles[source], bottles[destin])
    
    for i in range(num_transferable):
        bottles[destin][destin_index - 1] = bottles[source][source_index]
        bottles[source][source_index] = ' '
        destin_index -= 1
        source_index += 1
        
# ******************************************
def full(aBottle):
    """
    Given a structure representing a bottle, returns True if the bottle is full with equal symbols; returns False otherwise.

    Parameters
    ----------
    aBottle : list
        A list containing the information about a bottle, including symbols.

    Returns
    -------
    bool
        True if the bottle is full with equal symbols; False otherwise.

    """
    for elem in aBottle:
        if elem == ' ':
            return False

    first_symbol = aBottle[0]
    for symbol in aBottle:
        if symbol != first_symbol:
            return False
    return True

# *****************************************************
def allBottlesFull(fullBottles, expertise):
    """
    Checks if a structure representing a bottle is full with equal symbols; returns True if it is,
    and False otherwise.

    Parameters
    ----------
    fullBottles : int
        The number of full bottles.

    expertise : int
        The level of expertise.

    Returns
    -------
    bool
        True if the bottles are full and their quantity equals the expertise; otherwise, False.
    """
    
    if fullBottles == NR_BOTTLES - expertise:
       
        return fullBottles, expertise
    else:
        False

#######################################################
##################  MAIN PROGRAM ######################
#######################################################        
CAPACITY = 8
LETTERS = "ABCDEFGHIJ"
SYMBOLS = "@#%$!+o?§"
NR_BOTTLES = 10
LESS_EXPERT = 5
MAX_EXPERT = 1
expertise = askForExpertise()
bottles = buildGameBottles(expertise)
nrErrors = 0
fullBottles = 0 
endGame = False
showBottles(bottles, nrErrors)
# Let's play the game
while not endGame:
    source, destin = askForPlay()
    if moveIsPossible(source, destin, bottles):
        doMove(source, destin,bottles)
        showBottles(bottles, nrErrors)
        if full(bottles[destin]):
            fullBottles += 1
            keepGo = input("Bottle filled!!! Congrats!! Keep playing? (Y/N)")
            if keepGo == "N":
                endGame = True
    else:
        print("Error!")
        nrErrors += 1
    endGame = allBottlesFull(fullBottles, expertise) or nrErrors == 3

print("Full bottles =", fullBottles, "  Errors =", nrErrors)
if nrErrors >= 3:
    print("Better luck next time!")
else:
    print("CONGRATULATIONS!!")
    
