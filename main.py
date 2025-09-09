import tkinter as tk
from random import sample, randint, choice, shuffle
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
skeletonGif         =   "skeleton.gif"
slimeGif            =   "slime.gif"
spiderGif           =   "spider.gif"
levelBackground     =   Image.open("firstLayer.png")
menuBackground      =   Image.open("menuLayer.png")
saveMenuBackground  =   ImageTk.PhotoImage(menuBackground)
saveLevelBackground =   ImageTk.PhotoImage(levelBackground)
pathOfADictionary   =   "words.txt"
with open(pathOfADictionary, "r", encoding="utf-8") as f:
    words = [rowOftext.strip().upper() for rowOftext in 
             f if len(rowOftext.strip()) >= 3]

# gameAttributes
frames = []
currentFrameIndex = 0
animationAfterId = None
characterLabel = tk.Label(win, bg="black")
allPools            =   [
    "A", "Á", "Ä", "B", "C", "Č", "D", "Ď",
    "E", "É", "F", "G", "H", "I", "Í", "J", "K",
    "L", "Ĺ", "Ľ", "M", "N", "Ň", "O", "Ó", "Ô", "P",
    "Q", "R", "Ŕ", "S", "Š", "T", "Ť", "U", "Ú", "V",
    "W", "X", "Y", "Ý", "Z", "Ž"
]
specialLetters      =   ["Q","W"]
levelLetters        =   []
wordsAlreadyUsed    =   []
letterLabels        =   []
maxPerRow           =   15
letterSpacingY      =   17
letterSpacingX      =   30
startLettersX       =   winSizeX-302
startLettersY       =   (winSizeY/2)+50
attackBind          =   "<Return>"
healthAttributePlay =   21
healthAttributeEnem =   3
levelAttribute      =   1
mainDelay           =   1000
namesOfEnemy        =   ["Slime", "Spider","Skeleton"]

# activeVariables
playerHealth        =   healthAttributePlay
firstEnemyHealth    =   healthAttributeEnem
nextEnemyHealth     =   healthAttributeEnem
level               =   levelAttribute
enemyNamesShow      =   randint(0,2)

# functions
# basicFunction
def forceUppercase(event):
    widget = event.widget
    currenText = widget.get()
    widget.delete(0, tk.END)
    widget.insert(0, currenText.upper())

def delayStartGame():
    win.after(mainDelay,startGameButton)
    startButton.config(state="disabled")
    endButton.config(state="disabled")

def delayNextLevel():
    win.after(mainDelay,nextLv)
    backToMenuButton.config(state="disabled")
    nextLvButton.config(state="disabled")

def delayStartMenu():
    win.after(mainDelay,mainMenu)
    backToMenuButton.config(state="disabled")

def clearWidgets():
    for widget in win.winfo_children():
        widget.place_forget()

# mainMenuFunctions
def mainMenu():
    startButton.config(state="normal")
    endButton.config(state="normal")
    clearWidgets()
    # reset
    returnToFirstLv()
    healPlayer()
    deleteText()
    # placeObjects
    gameBackgroundMenu.place(x=-1,y=-1)
    gameBackgroundMenu.lower()
    nameGame.place(x=winSizeX/2, y=(winSizeY/2)-40, anchor=tk.CENTER)
    startButton.place(x=winSizeX/2, y=(winSizeY/2)+40, anchor=tk.CENTER)
    endButton.place(x=winSizeX/2, y=(winSizeY/2)+100, anchor=tk.CENTER)

# closeFunction
def endGameButton():
    f.close()
    win.destroy()

# startFirstLevelFunction
def startGameButton():
    global level
    clearWidgets()  
    for h in allPools:
        if h in specialLetters:
            allPools.remove(h)  
    # playerTakesDamage
    enemyShow()
    playerTakesDamage()
    randomizer()
    updateLetterDisplay()
    win.bind(attackBind, playerAttack)
    # placeObjects
    gameBackgroundLevel.place(x=-1, y=-1)
    gameBackgroundLevel.lower()
    characterLabel.place(x=winSizeX/2, y=(winSizeY/2)-90, anchor=tk.CENTER)
    attackButton.place(x=winSizeX/2, y=winSizeY-40, anchor=tk.CENTER)
    playerHealthPoints.place(x=((winSizeX/2)/2)-36, y=(winSizeY/2)+((winSizeY/2)/2)+48, anchor=tk.CENTER)
    playerWriter.place(x=winSizeX/2, y=winSizeY-90, anchor=tk.CENTER)
    enemyHealthPoints.place(x=winSizeX/2, y=13, anchor=tk.CENTER)
    enemyName.place(x=winSizeX/2, y=60, anchor=tk.CENTER)
    levelIndication.place(x=45, y=10, anchor=tk.NW)             

# endFightMenuFunction
def afterFightMenu():
    global firstEnemyHealth, playerHealth
    backToMenuButton.config(state="normal")
    nextLvButton.config(state="normal")
    if firstEnemyHealth <= 0 and len(allPools) == len(levelLetters):
        
        win.unbind(attackBind)
        youWonGameTitle.place(x=winSizeX/2, y=(winSizeY/2)-30, anchor=tk.CENTER)
        backToMenuButton.place(x=(winSizeX/2), y=(winSizeY/2)+30, anchor=tk.CENTER)
        attackButton.config(state="disabled")
        playerWriter.config(state="disabled")
        stopAnimation()
        
    elif playerHealth <= 0:
        win.unbind(attackBind)
        youLostTitle.place(x=winSizeX/2, y=(winSizeY/2)-30, anchor=tk.CENTER)
        backToMenuButton.place(x=(winSizeX/2), y=(winSizeY/2)+30, anchor=tk.CENTER)
        attackButton.config(state="disabled")
        playerWriter.config(state="disabled")
                                                                                
    elif firstEnemyHealth <= 0 and len(allPools) != len(levelLetters):
        
        win.unbind(attackBind)                                    
        youWonTitle.place(x=winSizeX/2, y=(winSizeY/2)-30, anchor=tk.CENTER)
        backToMenuButton.place(x=(winSizeX/2)-100, y=(winSizeY/2)+20, anchor=tk.CENTER)
        nextLvButton.place(x=(winSizeX/2)+100, y=(winSizeY/2)+20, anchor=tk.CENTER)
        attackButton.config(state="disabled")
        playerWriter.config(state="disabled")
        stopAnimation()

# resetForReturnToMainMenu
def returnToFirstLv():
    global firstEnemyHealth, level, nextEnemyHealth, wordsAlreadyUsed
    wordsAlreadyUsed = []
    level = levelAttribute
    firstEnemyHealth = healthAttributeEnem
    nextEnemyHealth = healthAttributeEnem
    attackButton.config(state="normal")
    playerWriter.config(state="normal")
    enemyHealthPoints.config(text=str(firstEnemyHealth))
    levelIndication.config(text=str(level)+"LV")

# nextLevel
def nextLv():
    global level, firstEnemyHealth, nextEnemyHealth, enemyNamesShow
    # healsPlayer
    win.bind(attackBind, playerAttack)
    healPlayer()
    deleteText()
    # nextEnemyAndCounterOfLevel
    level += 1
    for letter in specialLetters:
        if letter not in allPools and level == 5:
            allPools.append(letter)
    generateNewLetters(5)
    updateLetterDisplay()
    nextEnemyHealth += 2
    firstEnemyHealth = nextEnemyHealth
    levelIndication.config(text=str(level)+"LV")
    enemyHealthPoints.config(text=str(firstEnemyHealth))
    enemyNamesShow = randint(0,2)
    enemyName.config(text=namesOfEnemy[enemyNamesShow])
    enemyShow()
    playerTakesDamage()
    playerHealthPoints.config(text=playerHealth)
    attackButton.config(state="normal")
    playerWriter.config(state="normal")
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
        win.after(2000, playerTakesDamage)
    # endFightMenuFunction
    afterFightMenu()

# damagePerLetter
def damagePerLetter():
    global words, levelLetters, wordsAlreadyUsed
    wordInWriter = playerWriter.get()
    damage = len(wordInWriter)
    if damage <= 2:
        #print(1)
        return False
    if wordInWriter not in words:
        #print(2)
        return False
    lettersInWriter = Counter(wordInWriter)
    for letter in lettersInWriter:
        if letter not in levelLetters:
            #print(3)
            return False
    if wordInWriter in wordsAlreadyUsed:
        #print(4)
        return False
    wordsAlreadyUsed.append(wordInWriter)
    return damage

# removeTextFromWriter
def deleteText():
    playerWriter.delete(0, tk.END)

# randomizerOfLetters
def randomizer(totalLetters=15):
    global levelLetters
    word = choice(words)
    lettersFromWord = list(set(word))
    needed = totalLetters - len(lettersFromWord)
    remainingPool = list(set(allPools) - set(lettersFromWord))
    extraLetters = sample(remainingPool, needed)
    levelLetters = lettersFromWord + extraLetters
    shuffle(levelLetters)
        
def generateNewLetters(count):
    global levelLetters
    available = list(set(allPools) - set(levelLetters))
    newLetters = sample(available, min(count, len(available)))
    levelLetters.extend(newLetters)
    
def updateLetterDisplay():
    global levelLetters, letterLabels
    for letterLbl in letterLabels:
        letterLbl.destroy()
    letterLabels.clear()
    for index, letter in enumerate(levelLetters):
        row = index // maxPerRow
        col = index % maxPerRow
        x = startLettersX + col * letterSpacingY
        y = startLettersY + row * letterSpacingX
        lbl = tk.Label(win, text=letter, font=fntInGameLettets, bg="#a8bec2", fg="black")
        lbl.place(x=x, y=y)
        letterLabels.append(lbl)

def enemyShow():
    global enemyNamesShow
    if enemyNamesShow == 0:                                                    
        loadCharacterAnimation(slimeGif)
    elif enemyNamesShow == 1:
        loadCharacterAnimation(spiderGif)
    elif enemyNamesShow == 2:                                                  
        loadCharacterAnimation(skeletonGif)

def animateCharacter():
    global currentFrameIndex, frames, characterLabel, animationAfterId
    if not frames:
        return
    frame = frames[currentFrameIndex]
    characterLabel.config(image=frame)
    characterLabel.image = frame
    currentFrameIndex = (currentFrameIndex + 1) % len(frames)
    animationAfterId = characterLabel.after(600, animateCharacter)

def stopAnimation():
    global animationAfterId
    if animationAfterId is not None:
        characterLabel.after_cancel(animationAfterId)
        animationAfterId = None

def loadCharacterAnimation(filepath):
    global frames, currentFrameIndex
    stopAnimation()
    gif = Image.open(filepath)
    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
    currentFrameIndex = 0
    animateCharacter()
    
# objects on screen
# mainMenu !!!
nameGame            =   tk.Label(win,text=nameOfGame,font=fntMenu, fg="white", bg="black")
startButton         =   tk.Button(win,text="Start",font=fntMenuBtn,command=delayStartGame,bg="#4a5e62",fg="#a8bec2", width=9)
endButton           =   tk.Button(win,text="Close",font=fntMenuBtn,command=endGameButton,bg="#4a5e62",fg="#a8bec2", width=9)

# fightEndedMenu !!!
youWonTitle         =   tk.Label(win,text="youDefeatedEnemy",font=fntMenu, fg="white", bg="black")
youWonGameTitle     =   tk.Label(win,text="youWonAGame",font=fntMenu, fg="green", bg="black")
youLostTitle        =   tk.Label(win,text="youLost",font=fntMenu, fg="red", bg="black")
backToMenuButton    =   tk.Button(win, command=delayStartMenu, text="Back", font=fntMenuBtn, bg="#4a5e62", fg="#a8bec2")
nextLvButton        =   tk.Button(win, command=delayNextLevel, text="Next", font=fntMenuBtn, bg="#4a5e62", fg="#a8bec2")

# gameStarted !!!
gameBackgroundLevel = tk.Label(win, image=saveLevelBackground)
gameBackgroundLevel.image = saveLevelBackground
gameBackgroundMenu  = tk.Label(win, image=saveMenuBackground)
gameBackgroundMenu.image = saveMenuBackground

attackButton        =   tk.Button(win,command=playerAttack,text="Attack", font=fntInGame, bg="red", fg="white")
playerHealthPoints  =   tk.Label(win,text=str(playerHealth)+" hp",font=fntInGame,fg="#93a8bd", bg="#dde4dd")
playerWriter        =   tk.Entry(win, font=fntInGame, width=10, bg="#a8bec2")
playerWriter.bind("<KeyRelease>", forceUppercase)
enemyHealthPoints   =   tk.Label(win,text=str(firstEnemyHealth),font=fntInGame,fg="red", bg="black")
enemyName           =   tk.Label(win,text=namesOfEnemy[enemyNamesShow], font=fntInGame, bg="black", fg="red")
levelIndication     =   tk.Label(win,text=str(level)+"LV",font=fntInGame, fg="#463539", bg="#995e6b")

# mainLoop !!!
mainMenu()
win.mainloop()