"""
Group Number: FP24
Students: [Yubing Chen (52915)], [Sona Moravcikova (62932)]
Project 3
"""
from random import randint
from random import shuffle

# *****************************************************
def topSymbolAndPosition(contents):
    """
    The symbol and position of the top of the bottle, that is,
    of the last position of the list contents

    Parameters
    ----------
    contents : a sequence of characters
        The contents of a bottle.

    Returns
    -------
    symbol : string
        The symbol at the last position. "_" if contents is empty.
    position : int
        The index of the last position. -1 if contents is empty.

    """
    position = len(contents) - 1
    symbol = "_" if contents == [] else contents[position]
    return symbol, position

# *****************************************************
def showBottles(bottles,botSize,nrErrors):
    """
    Prints in the standard output a representation of the
    game bottles.

    Parameters
    ----------
    bottles : dictionary
        Keys are strings and values are lists.
    botSize : int
        The capacity of bottles.
    nrErrors : int
        The number of errors the user already made.

    Returns
    -------
    None.

    """
    print(" " * 3, end = "")
    for letter in bottles.keys():
        print(letter, end = " " * 6) 
    print()
    
    line = botSize - 1
    while line >= 0:
       for content in bottles.values():
           print(" " * 2, end = "")
           if line < len(content):
               print("|" + content[line] + "|", end = "")
           else:
               print("| |", end = "")               
           print(" " * 2, end = "")
       line -= 1
       print()
    print("NUMBER OF ERRORS:", nrErrors)
# *****************************************************
def allBottlesFull(nrBotts, nrBottFull, expert):
    """
    Are all the bottles that are supposed to be full at the end  
    of the game already full?

    Parameters
    ----------
    nrBotts : int
        The number of bottles in the game.
    nrBottFull : int
        The number of bottles already full (with equal symbol).
    expert : int
        The user's expert level.

    Returns
    -------
    True if the number of bottles that are supposed to be full at
    the end of the game is already achieved.

    """
    expectFull = nrBotts - expert
    return nrBottFull == expectFull
# *****************************************************
def full(bottle, botSize):
    """
    Is a given bottle all full with a same symbol?

    Parameters
    ----------
    bottle : list of characters
        The contents of a bottle.
    botSize : int
        The capacity of the bottle.

    Returns
    -------
    bool
        True if the list bottle has botSize elements, all equal.

    """
    if len(bottle) < botSize:
        return False
    top = bottle[0]
    for char in bottle:
        if not char == top:
            return False
    return True

# *****************************************************
def doMove(botSize, source, destin, bottles):
    """
    Transfers as much "liquid" as possible from source to destin

    Parameters
    ----------
    botSize : int
        The capacity of bottles.
    source : string
        The letter that identifies the source bottle in the dict bottles.
    destin : string
        The letter that identifies the destination bottle in the dict bottles.
    bottles : dictionary
        Keys are strings and values are lists.

    Returns
    -------
    int
        The quantity of "liquid" that was transferred from source to destin.

    Requires: 
    --------
        moveIsPossible(botSize, source, destin, bottles)
    """
    sourceSymb, sourceTop = topSymbolAndPosition(bottles[source])
    destSymb, destTop = topSymbolAndPosition(bottles[destin])    
    # How many there are in source to transfer?
    howManyEqual = 0
    i = sourceTop
    sourceContent = bottles[source]
    while i >= 0 and sourceContent[i] == sourceSymb:
       i -= 1
       howManyEqual += 1
    # Transfer as many as possible
    transfer = min(howManyEqual, botSize - destTop - 1)
    for i in range(transfer):
        sourceContent.pop()
        bottles[destin].append(sourceSymb)
    
    return transfer
# *****************************************************
def moveIsPossible(botSize, source, destin, bottles):
    """
    Is it possible to transfer any "liquid" from source to destin?

    Parameters
    ----------
    botSize : int
        The capacity of bottles.
    source : string
        The letter that identifies the source bottle in the dict bottles.
    destin : string
        The letter that identifies the destination bottle in the dict bottles.
    bottles : dictionary
        Keys are strings and values are lists.

    Returns
    -------
    bool
        True if the source is not empty, and, either the destination is empty
        or it has some empty position(s) and the top symbols of both bottles
        are the same.

    Requires: 
    --------
        bottles contain keys source and destin

    """
    sourceSymb, sourceTop = topSymbolAndPosition(bottles[source])
    destSymb, destTop = topSymbolAndPosition(bottles[destin])    
 
    return sourceTop != -1 and \
           (destTop == -1 or
           (destTop < botSize - 1 and sourceSymb == destSymb)) 
# ***************************************************************
def buildGameBottles(nrBotts, botSize, expert, letters, symbols):
    """
    Builds a dictionary of bottles, filled in a random way.

    Parameters
    ----------
    nrBotts : int
        The number of bottles in the game.
    botSize : int
        The capacity of bottles.
    expert : int
        The level of the user's expertise.
    letters : string
        The letters that identify bottles.
    symbols : string
        The symbols that compose the liquid in bottles.

    Returns
    -------
    result : dictionary where keys are strings and values are lists. 
        The dictionary contains nrBotts items, whose keys are the first nrBotts
        characters of letters. The different symbols used to populate the lists
        corresponding to keys are the first (nrBotts - expert) characters of
        symbols. In total, ((nrBotts - expert) * botSize) symbols will be
        randomly distributed by the nrBotts bottles.

    Requires: 
    --------
        letters length is >= nrBotts; symbols length is >= (nrBotts - expert);
        expert < nrBotts

    """   
    result = {}
    howManyFullBott = nrBotts - expert
    allSymbols = randomSymbols(botSize,howManyFullBott,symbols)
    letter = 0
    indexFrom = 0
    # In this way we obtain a more balanced symbol distribution
    indexTo = randint(botSize - expert,botSize)
    for nr in range(nrBotts - 1):
        symbolsToPut = allSymbols[indexFrom : indexTo]
        result[letters[letter]] = symbolsToPut
        letter += 1
        indexFrom = indexTo
        newValueTo = indexTo + randint(botSize - expert,botSize)
        indexTo = min(len(allSymbols), newValueTo)
    symbolsToPut = allSymbols[indexFrom : indexTo]
    result[letters[letter]] = symbolsToPut
        
    return result
# *****************************************************
def randomSymbols(botSize, howMany, symbols):
    """
    Builds and returns a list with (botSize * howMany) characters of symbols

    Parameters
    ----------
    botSize : int
        Capacity of bottles.
    howMany : int
        The number of different symbols to be used.
    symbols : string
        The symbols that can be used.

    Returns
    -------
    list of characters

    Requires: 
    --------
        symbols length is >= howMany;

    """
    # botSize chars of each of the first howMany symbols
    symbolsToUse = symbols[0:howMany]
    result = [s for s in symbolsToUse for _ in range(botSize)]
    shuffle(result)
    return result

# *****************************************************
def askUserFor(ask, options, end = ""):
    """
    Asks the user for some information

    Parameters
    ----------
    ask : string
        The text to be shown the user.
    options : sequence
        The options the user has.
    end : string, optional
        Additional messages to add to the above options. 
        The default is "".

    Returns
    -------
    string
        The user's choice (that belongs to the available options),
        in uppercase.

    """
    listOptions = list(options) + [end]
    answer = input(ask).upper()
    while answer not in listOptions:
       answer = input("Wrong choice! Repeat input: ").upper()
     
    return answer

# *****************************************************
# ***************** NEW FUNCTIONS HERE ****************
# *****************************************************
def newGameInfo(fileName):
    """
     Reads information from the file for a new game and returns a tuple.
     Parameters
     ----------
     fileName : str
         The name of the file containing game information.
     Returns
     -------
     tuple
         Tuple containing the necessary game information.
         (nrBotts, bottles, botSize, nrErrors, expertise, fullBottles)
     Raises
     ------
     Exception
         Raises an exception if there is a problem with the file.
         
     File Structure
     --------------
     The file is expected to have the following structure:
     min_expertise: <int>
     max_expertise: <int>
     nrBotts: <int>
     symbols: <string>
     botSize: <int>
     nrErrors: <int>
     letters: <string>
     fullBottles: <int>
    """
    while True:  # Start an infinite loop
        try:
            # Read relevant parameters from the file
            with open(fileName, 'r') as file:
                min_expertise = int(file.readline().split(":")[1].strip())
                max_expertise = int(file.readline().split(":")[1].strip())
                nrBotts = int(file.readline().split(":")[1].strip())
                symbols = file.readline().split(":")[1].strip()
                botSize = int(file.readline().split(":")[1].strip())
                nrErrors = int(file.readline().split(":")[1].strip())
                letters = file.readline().split(":")[1].strip()
                fullBottles = int(file.readline().split(":")[1].strip())

            # Randomly generate expertise level within the specified interval
            expertise = randint(min_expertise, max_expertise)

            # Create a dictionary representing the bottles information
            bottles = buildGameBottles(nrBotts, botSize, expertise, letters, symbols)

            # Return the necessary game information and break the loop
            return nrBotts, bottles, botSize, nrErrors, expertise, fullBottles  

        except FileNotFoundError:
            print("The file name you entered is wrong, please check and enter again.")
            fileName = input("Enter the name of the file containing game information: ")
        except Exception as e:
            raise Exception(f"Error processing file '{fileName}': {e}")

# *****************************************************
def writeGameInfo(fName, expertise, nrBotts, bottles, botSize, nrErrors, fullBottles):
    """
    Writes the game information to a file.

    Parameters
    ----------
    fName : str
        The name of the file to write the information.
    expertise : int
        User expertise level.
    nrBotts : int
        Number of bottles in the game.
    bottles : dict
        Dictionary representing the state of bottles.
    botSize : int
        Capacity of bottles.
    nrErrors : int
        Number of errors in the game.

    Returns
    -------
    None

    """
    try:
        with open(fName, 'w') as file:
            file.write(f"expertise: {expertise}\n")
            file.write(f"nrBotts: {nrBotts}\n")
            file.write(f"botSize: {botSize}\n")
            file.write(f"nrErrors: {nrErrors}\n")
            file.write(f"fullBottles: {fullBottles}\n")
            for letter, content in bottles.items():
                file.write(f"{letter}: {''.join(content)}\n")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")

# *****************************************************
def oldGameInfo(fileName):
    """
    Reads information from the file for an old game and returns a tuple.

    Parameters
    ----------
    fileName : str
        The name of the file containing game information.

    Returns
    -------
    tuple
        Tuple containing the necessary game information.
        (nrBotts, bottles, botSize, nrErrors, expertise, fullBottles)

    Raises
    ------
    Exception
        Raises an exception if there is a problem with the file.
    
    File Structure
    --------------
    The file is expected to have the following structure:
    expertise: <int>
    nrBotts: <int>
    botSize: <int>
    nrErrors: <int>
    fullBottles: <int>
    <letter>: <content>
    
    """
    while True:  # Start an infinite loop
        try:
            # Read relevant parameters from the file
           with open(fileName, 'r') as file:
               expertise = int(file.readline().split(":")[1].strip())
               nrBotts = int(file.readline().split(":")[1].strip())
               botSize = int(file.readline().split(":")[1].strip())
               nrErrors = int(file.readline().split(":")[1].strip())
               fullBottles = int(file.readline().split(":")[1].strip())

               # Read bottles information
               bottles = {}
               line = file.readline().strip()
               while line:
                   letter, content = line.split(":")
                   bottles[letter.strip()] = list(content.strip())
                   line = file.readline().strip()

           # Return the necessary game information
           return nrBotts, bottles, botSize, nrErrors, expertise, fullBottles  

        except FileNotFoundError:
            print("The file name you entered is wrong, please check and enter again.")
            fileName = input("Enter the name of the file containing game information: ")
        except Exception as e:
            raise Exception(f"Error processing file '{fileName}': {e}")

        
