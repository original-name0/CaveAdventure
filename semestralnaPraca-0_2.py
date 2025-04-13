import tkinter as tk
from random import sample, choice, randint
from collections import Counter
from PIL import Image, ImageTk, ImageSequence

win = tk.Tk()

# config
nameOfGame          =   "semestralnaPraca"
winSizeX            =   800
winSizeY            =   600

# setup
win.resizable(width=False, height=False)
win.title(nameOfGame)
winSize = str(winSizeX)+"x"+str(winSizeY)
win.geometry(winSize)

# assets
fntMenuBtn          =   ("PX Sans Nouveaux", 11)
fntMenu             =   ("PX Sans Nouveaux", 15)
fntInGame           =   ("PX Sans Nouveaux", 12)
fntInGameLettets    =   ("PX Sans Nouveaux", 10)

# gameAttributes
vowelsShort         =   ["a", "e", "i", "y", "o", "u", "ä"]
vowelsAndDiphthong  =   ["á", "é", "í", "ó", "ú", "ý", "ô"]
consonantsBothLike  =   ["b", "m", "p", "r", "s", "v", "z", "f"]
consonantsHard      =   ["h", "c", "h", "k", "g", "d", "t", "n", "l"]
consonantsSoft      =   ["č", "d", "ž", "š", "ž", "c", "d", "z", "j", "ď", "ť", "ň", "ľ"]

lettersInUse        =   []
attackBind          =   "<Return>"
healthAttributePlay =   16
healthAttributeEnem =   3
levelAttribute      =   1
mainDelay           =   500
namesOfEnemy        =   ["Skeleton", "Slime", "Bandint", "Spider", "Bat"]

# activeVariables
playerHealth        =   healthAttributePlay
firstEnemyHealth    =   healthAttributeEnem
nextEnemyHealth     =   healthAttributeEnem
level               =   levelAttribute

# functions
# basicFunction
def delayStartGame():
    win.after(mainDelay,startGameButton)

def delayNextLevel():
    win.after(mainDelay,nextLv)

def delayStartMenu():
    win.after(mainDelay,mainMenu)

def clearWidgets():
    for widget in win.winfo_children():
        widget.place_forget()

# mainMenuFunctions
def mainMenu():
    clearWidgets()
    # reset
    returnToFirstLv()
    healPlayer()
    deleteText()
    # placeObjects
    nameGame.place(x=winSizeX/2, y=(winSizeY/2)-40, anchor=tk.CENTER)
    startButton.place(x=winSizeX/2, y=(winSizeY/2)+20, anchor=tk.CENTER)
    endButton.place(x=winSizeX/2, y=(winSizeY/2)+80, anchor=tk.CENTER)

# closeFunction
def endGameButton():
    win.destroy()

# startFirstLevelFunction
def startGameButton():
    clearWidgets()
    global level
    
    # playerTakesDamage
    playerTakesDamage()
    win.bind(attackBind, playerAttack)
    lettersAdder()
    
    # placeObjects
    attackButton.place(x=winSizeX/2, y=winSizeY-40, anchor=tk.CENTER)
    playerHealthPoints.place(x=winSizeX/2+((winSizeX/2)/2)+33, y=(winSizeY/2)+((winSizeY/2)/2)+50, anchor=tk.CENTER)
    playerWriter.place(x=((winSizeX/2)/2)-25, y=(winSizeY/2)+((winSizeY/2)/2)+50, anchor=tk.CENTER)
    playerLetters.place(x=winSizeX/2, y=winSizeY-80, anchor=tk.CENTER)
    enemyHealthPoints.place(x=winSizeX/2, y=20, anchor=tk.CENTER)
    enemyName.place(x=winSizeX/2, y=60, anchor=tk.CENTER)
    levelIndication.place(x=winSizeX-50, y=10, anchor=tk.NE)

# endFightMenuFunction
def afterFightMenu():
    global firstEnemyHealth, playerHealth
    # playerWon
    if firstEnemyHealth <= 0:
        win.unbind(attackBind)
        youWonTitle.place(x=winSizeX/2, y=(winSizeY/2)-30, anchor=tk.CENTER)
        backToMenuButton.place(x=(winSizeX/2)-100, y=(winSizeY/2)+20, anchor=tk.CENTER)
        nextLvButton.place(x=(winSizeX/2)+100, y=(winSizeY/2)+20, anchor=tk.CENTER)
        attackButton.config(state="disabled")
        playerWriter.config(state="disabled")
    # playerLost
    elif playerHealth <= 0:
        win.unbind(attackBind)
        youLostTitle.place(x=winSizeX/2, y=(winSizeY/2)-30, anchor=tk.CENTER)
        backToMenuButton.place(x=(winSizeX/2), y=(winSizeY/2)+30, anchor=tk.CENTER)
        attackButton.config(state="disabled")
        playerWriter.config(state="disabled")

# resetForReturnToMainMenu
def returnToFirstLv():
    global firstEnemyHealth, level, nextEnemyHealth, lettersInUse
    lettersInUse = []
    level = levelAttribute
    firstEnemyHealth = healthAttributeEnem
    nextEnemyHealth = healthAttributeEnem
    attackButton.config(state="normal")
    playerWriter.config(state="normal")
    enemyHealthPoints.config(text=str(firstEnemyHealth))
    levelIndication.config(text=str(level)+"LV")

# nextLevel
def nextLv():
    global level, firstEnemyHealth, nextEnemyHealth
    # healsPlayer
    win.bind(attackBind, playerAttack)
    healPlayer()
    deleteText()
    
    # nextEnemyAndCounterOfLevel
    level += 1
    if level > 1:
        nextEnemyHealth += 5
        firstEnemyHealth = nextEnemyHealth
    levelIndication.config(text=str(level)+"LV")
    enemyHealthPoints.config(text=str(firstEnemyHealth))
    enemyName.config(text=namesOfEnemy[randint(0, 4)])
    
    # setsForNewLvGameplayFunctions
    playerTakesDamage()
    playerHealthPoints.config(text=playerHealth)
    attackButton.config(state="normal")
    playerWriter.config(state="normal")
    
    # clearsEndFightMenu
    youWonTitle.place_forget()
    nextLvButton.place_forget()
    backToMenuButton.place_forget()
    
# healsPlayer
def healPlayer():
    global playerHealth
    playerHealth = healthAttributePlay

# takesHealthFromEnemy
def playerAttack(event=None):
    global firstEnemyHealth
    damage = damagePerLetter()
    deleteText()
    firstEnemyHealth -= damage
    enemyHealthPoints.config(text=str(firstEnemyHealth))
    # endFightMenuFunction
    afterFightMenu()

# takesHealthFromPlayer
def playerTakesDamage():
    global playerHealth
    if playerHealth > 0 and firstEnemyHealth > 0:
        playerHealth -= 1
        playerHealthPoints.config(text=str(playerHealth))
        win.after(1500, playerTakesDamage)
    # endFightMenuFunction
    afterFightMenu()

def damagePerLetter():
    wordInWriter = playerWriter.get()
    #letersInDesposal = "aeio"
    damage = len(wordInWriter)
    words = ["name"]
    if damage <= 2:
        return False

    if wordInWriter not in words:
        return False

    # Skontroluj, či sú všetky písmená dostupné v zásobe
    lettersInFound = Counter(lettersInUse)
    lettersInWriter = Counter(wordInWriter)

    for letter, count in lettersInWriter.items():
        if lettersInFound[letter] < count:
            return False
    
    return damage

def deleteText():
    playerWriter.delete(0, tk.END)

def randomizer():
    global lettersInUse
    lettersInUse.extend(sample(vowelsShort, 3))


    lettersInUse.append(choice(vowelsAndDiphthong))
    lettersInUse.extend(sample(consonantsBothLike, 2))
    lettersInUse.extend(sample(consonantsHard, 2))
    lettersInUse.extend(sample(consonantsSoft, 2))
    
    return lettersInUse
        
def lettersAdder():
    global level, lettersInUse
    arrayOfLetters = randomizer()
    playerLetters.config(text=arrayOfLetters)
    print(arrayOfLetters)
    return arrayOfLetters
    
# objects on screen
# mainMenu !!!
nameGame            =   tk.Label(win,text=nameOfGame,font=fntMenu)
startButton         =   tk.Button(win,text="Start",font=fntMenuBtn,command=delayStartGame,bg="grey",fg="white", width=9)
endButton           =   tk.Button(win,text="Close",font=fntMenuBtn,command=endGameButton,bg="grey",fg="white", width=9)

# fightEndedMenu !!!
youWonTitle         =   tk.Label(win,text="youDefeatedEnemy",font=fntMenu, fg="blue")
youLostTitle        =   tk.Label(win,text="youLost",font=fntMenu, fg="red")
backToMenuButton    =   tk.Button(win, command=delayStartMenu, text="Back", font=fntMenuBtn, bg="blue", fg="white")
nextLvButton        =   tk.Button(win, command=delayNextLevel, text="Next", font=fntMenuBtn, bg="blue", fg="white")

# gameStarted !!!
attackButton        =   tk.Button(win,command=playerAttack,text="Attack", font=fntInGame, bg="red", fg="white")
playerHealthPoints  =   tk.Label(win,text=str(playerHealth)+" hp",font=fntInGame,fg="red")
playerWriter        =   tk.Entry(win, font=fntInGame, width=10)
playerLetters       =   tk.Label(win,text=lettersInUse,font=fntInGameLettets)
enemyHealthPoints   =   tk.Label(win,text=str(firstEnemyHealth),font=fntInGame,fg="red")
enemyName           =   tk.Label(win,text=namesOfEnemy[randint(0, 3)], font=fntInGame)
levelIndication     =   tk.Label(win,text=str(level)+"LV",font=fntInGame, fg="black")

# mainLoop !!!
mainMenu()
win.mainloop()