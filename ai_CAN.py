# ai_CAN.py
# AI Wordle player created by Noah Gabryluk and Matt Flammenspeck

import pdb
import random
import utils

def makeguess(wordlist, guesses=[], feedback=[]):
    """Guess a word from the available wordlist, (optionally) using feedback 
    from previous guesses.
    
    Parameters
    ----------
    wordlist : list of str
        A list of the valid word choices. The output must come from this list.
    guesses : list of str
        A list of the previously guessed words, in the order they were made, 
        e.g. guesses[0] = first guess, guesses[1] = second guess. The length 
        of the list equals the number of guesses made so far. An empty list 
        (default) implies no guesses have been made.
    feedback : list of lists of int
        A list comprising one list per word guess and one integer per letter 
        in that word, to indicate if the letter is correct (2), almost 
        correct (1), or incorrect (0). An empty list (default) implies no 
        guesses have been made.
    Output
    ------
    word : str
        The word chosen by the AI for the next guess.
    """
    
    wordlist = [j for j in wordlist if j != '']

    # Hard code the first 3 guesses
    if len(guesses) == 0:
        return 'STAIN'
    if len(guesses) == 1:
        return 'CEORL'
    if len(guesses) == 2:
        return 'UMPED'
    
    
    # Create a list of length 5 representing the amount of possible letters that a given space could have
    #   - We will remove letters from ALL these alphabet strings if not in the word
    #   - We will remove letters from the spot they were in but not the others if yellow
    #   - We will remove all but the letter in the spot but not the others if green
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # valid letters to guess
    possibleLetters = []
    for i in range(5):
        possibleLetters.append(ALPHABET)


    ########################################################
    # Update the possible letters that could be in each spot
    ########################################################
    
    # Get all of the yellow letters mapped to the spots they are incorrect in to filter 
    # wordlist to remove words including these letters in incorrect spots
    yellowLetters = {} 

    # Looping through each of the 5 letter spots in every guess
    for guess in range(len(guesses)):
        
        # Loop through the 5 letters in each of guess
        for i in range(5):
            currentfeedback = feedback[guess][i]
            currentLetter = guesses[guess][i]

            # If correct make the possible letters list at that spot just the letter (Because it's the correct one)
            # Keep in mind this doesn't remove it from other possible spots
            if currentfeedback == 2:
                possibleLetters[i] = currentLetter

                # if letter was yellow before, it is removed from the yellow letter dictionary
                if currentLetter in yellowLetters.keys():
                    yellowLetters.pop(currentLetter)

            # If almost correct (in the word but not the correct spot), remove from list at that spot
            elif currentfeedback == 1:
                possibleLetters[i] = possibleLetters[i].replace(currentLetter, "")
                if len(yellowLetters) == 0:
                    yellowLetters[currentLetter] = [i]
                elif currentLetter not in yellowLetters.keys():
                    yellowLetters[currentLetter] = [i]
                else:
                    yellowLetters[currentLetter].append(i)

            # If incorrect, remove the wrong letter from all possible letter lists
            else:
                # There is a case where if a letter appears twice in the secret word and one of those letters
                # has been correctly guessed or almost correctly guessed but not the other; what happened before 
                # is that we would remove that letter from all the possibleLetters strings, which includes the 
                # string that has the only correct letter in it, breaking the algorithm.

                # Solution: Check if letter has already been guessed correctly in another spot. If it is, only 
                # remove it as a possibility in the current spot. If not, it's not in the word so remove it 
                # from all possible spots
                alreadyInWord = False
                for group in possibleLetters:
                    # If correct
                    if len(group) == 1 and group[0] == currentLetter:
                        possibleLetters[i] = possibleLetters[i].replace(currentLetter, "")
                        alreadyInWord = True
                        break
                    # If almost correct
                    elif currentLetter not in group:
                        possibleLetters[i] = possibleLetters[i].replace(currentLetter, "")
                        alreadyInWord = True
                        break

                if not alreadyInWord:
                    possibleLetters = [list.replace(currentLetter, "") for list in possibleLetters]
        

    ################################################################
    # Filter down the wordlist based on the updated possible letters
    ################################################################
    
    # Loop through each letter spot
    for i in range(5):

        # If there is only one possible letter, that is the letter
        if len(possibleLetters[i]) == 1:
            wordlist = [word for word in wordlist if possibleLetters[i][0] == word[i]]
        
        # If all letters are possible, can't filter down
        elif len(possibleLetters[i]) == 26:
            continue

        # If there are more than one but not all possible letters, gets all the letters that are not in 
        # the current spot's possible letters string and removes words with these incorrect letters in 
        # the current spot
        else:
            incorrectLetters = [j for j in ALPHABET if j not in possibleLetters[i]]

            for wrongLetter in incorrectLetters:
                wordlist = [word for word in wordlist if wrongLetter != word[i]]

    # Filters out words with yellow letters at incorrect spots
    for letter in yellowLetters:
        for spot in yellowLetters[letter]:
            wordlist = [word for word in wordlist if word[spot] != letter]

    # From here filter by the words that still contain the yellow letters
    for letter in yellowLetters:
        wordlist = [word for word in wordlist if letter in word]


    # print(wordlist)
    # pdb.set_trace()
   
    # Make a random guess from the remaining possible words
    guess = random.choice(wordlist)   
    
    wordlist = utils.readwords("allwords5.txt")
    return guess


if __name__ == "__main__":
    wordlist = utils.readwords("allwords5.txt")
    print(f"AI: \"My next choice would be {makeguess(wordlist)}\"")