#!/bin/python3

'''Part 1: Set Up'''

import os #Clean slate so people don't cheat
'''os.system('cls')'''

import random #Create the spinner

alphabet = "abcdefghijklmnopqrstuvwxyz"
sections = ["abcdef","abcdef","ghijklm","ghijklm","nopqrs","nopqrs","tuvwxyz","tuvwxyz",alphabet]
usedup = []

class Spinner:
  '''roulette hangman spinner'''
  
  def __init__(self,opt):
    '''Spinner(selections) creates a new spinner, selections is list'''
    self.options = opt
    self.index = self.spin()
    
  def spin(self):
    '''Spinner.spin() spins the wheel!'''
    return random.randrange(0,len(self.options))
    
  def __str__(self):
    return self.options[self.index]

class Player:
  '''roulette hangman player'''
  
  def __init__(self,name):
    '''Player(name) creates a new player'''
    self.name = name
    self.limbs = 0
    self.ingame = True
    
  def __str__(self):
    if self.ingame:
      return self.name + " has " + str(self.limbs) + " limbs"
      
  def check_ingame(self):
    '''Player.check_ingame() -> boolean, determines if one is still in the game'''
    return self.ingame
    
  def count_limbs(self):
    '''Player.count_limbs() -> int, determines number of limbs remaining'''
    return self.limbs
    
  def guess_letter(self,word):
    '''Player.guess_letter(self,word) -> boolean, player guesses letter and checks if in word'''
    options = str(Spinner(sections))
    
    full = 0 #
    for i in usedup:
      if i in options:
        full += 1
        
    if full == len(options):
      print("\nAll the letters in the landed section are used up, so you can't guess.  Too bad!")
      self.limbs += 1
      return False
    else:
      if options != alphabet:
        print('\033[4m' + "\nYou can only guess these letters: " + '\033[1m' + options + '\033[0m')
      else:
        print('\033[4m' + "\nYou can guess any letter!" + '\033[0m')

      while True: #actual guessing
          letter = input("Guess a letter!")
          if len(letter) == 1 and letter.lower() in alphabet:
            if letter.lower() in usedup: #Used up letter
              print("That letter is used up!")
            elif letter.lower() in options:
              usedup.append(letter.lower())
              break
            else:
              print("That letter is not allowed!")
          else:
            print("That's not a letter!")
        
      if letter.lower() in word.lower():
        return True
      else:
        self.limbs += 1
        return False
        
  def guess_word(self,word):
    '''Player.guess_word(self,word) -> boolean, player guesses word and checks if in word'''
    guess = input("Guess the word!  Spelling counts!")
    if guess.lower() == hiddenword.lower():
      if self.limbs > 0:
        self.limbs -= 1
      return True
    else:
      self.limbs += 2
      return False
      
  def eliminate(self):
    '''Player.eliminate() eliminates one from the game'''
    self.ingame = False
      
def importlist(file):
  '''imports a word file for use in roulette hangman'''
  myFile = open(file,"r")
  wordlist = myFile.readlines()
  for i in range(0,len(wordlist)):
    if wordlist[i][-1] == "\n":
      wordlist[i] = wordlist[i].strip()
  return wordlist
      
def fullchecker(string): #Check if section is full
  full = 0
  for i in usedup:
    if i in string:
      full += 1
  return full
  
game = 0
      
'''Part 2: The Game'''

players = 0 #decide number of players
while int(players) < 1:
  choicestr = input("How many players?")
  if choicestr.isdigit():
    players = int(choicestr)
    
if int(players) > 1:
  multiplayer = True
else:
  multiplayer = False
    
playerlist = [] #initialize player list
for i in range(0,players):
  playerlist.append(Player("Player " + str(i+1)))
 
player = 0
eliminated = 0
round = 1
while True:
  if game == 0: #select new word and its display, only done after word is cleared
    usedup = []
    hiddenword = importlist("normalwords.txt")[random.randrange(0,len(importlist("normalwords.txt")))]
    
    shown = ""
    for letter in hiddenword.lower():
      if letter in alphabet:
        shown += "-"
      else:
        shown += letter
    game = 1
    
  if multiplayer:
    print('\033[4m') #standings
    for p in playerlist:
      if p.check_ingame():
        print(p)
    print('\033[0m')
  else:
    print()
    print('\033[4m' + "It's round " + str(round) + ", and you have " + str(playerlist[0].count_limbs()) + " limbs.\n" + '\033[0m')
  
  print('\033[1m' + shown + '\033[0m') #The word to be solved
  print("Below are the used-up letters:")
  print(usedup)
  
  while True: #decide to guess letter or word
    if game == 0:
      decision = 0
      break
    if multiplayer:
      print('\033[4m' + "\nIt's Player " + str(player+1) + "'s turn!" + '\033[0m')
    decision = input("Press 1 to guess a letter, or Press 2 to guess a word!")
    if decision == "1" or decision == "2":
      break
    
  if decision == "1": #guess letter
    success = playerlist[player].guess_letter(hiddenword)
    if success:
      stock = ""
      for i in range(0,len(hiddenword)):
        if usedup[-1].lower() == hiddenword[i].lower():
          stock += hiddenword[i]
        else:
          stock += shown[i]
      shown = stock
  if decision == "2": #guess word
    success = playerlist[player].guess_word(hiddenword)
    if success:
      shown = hiddenword
    else:
      print("\nToo bad!")
      
  if shown == hiddenword: #check if word is revealed
    print("\n" + '\033[1m' + shown + '\033[0m')
    print("Nice!")
    round += 1
    game = 0
    
  if playerlist[player].count_limbs() > 8: #eliminate player
    playerlist[player].eliminate()
    eliminated += 1
    if multiplayer:
      if eliminated < len(playerlist)-1:
        print('\n\033[4m' + "Player " + str(player+1) + " is out of the game!" + '\033[0m')
      if eliminated == len(playerlist)-1:
        print("\nGame!")
        
        for i in range(0,len(playerlist)):
          if not playerlist[player].check_ingame():
            player = i+1
        
        print('\033[1m' + hiddenword + '\033[0m')
        
        print("Player " + str(player+1) + " wins!")
        break
    else:
      if eliminated == 1:
        print("\nGame!")
        print('\033[1m' + hiddenword + '\033[0m')
        print("You survived for " + str(round-1) + " rounds!")
        break
    
  while True:
    player += 1 #Changes players
    if player > len(playerlist)-1:
      player = 0
    if playerlist[player].check_ingame():
      break
