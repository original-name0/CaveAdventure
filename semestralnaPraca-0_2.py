from tkinter import *
from random import randint
from PIL import Image, ImageTk, ImageSequence
import time

win = Tk()

# config
nameOfGame          =   "semestralnaPraca"
winSizeX            =   600
winSizeY            =   400

# setup
win.resizable(width=False, height=False)
win.title(nameOfGame)
winSize = str(winSizeX)+"x"+str(winSizeY)
win.geometry(winSize)

# assets
fntMenuBtn          =   ("PX Sans Nouveaux", 11)
fntMenu             =   ("PX Sans Nouveaux", 15)
fntInGame           =   ("PX Sans Nouveaux", 12)

# gameAttributes
healthAttributePlay =   11
healthAttributeEnem =   10
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
    # placeObjects
    nameGame.place(x=winSizeX/2, y=(winSizeY/2)-40, anchor=CENTER)
    startButton.place(x=winSizeX/2, y=(winSizeY/2)+20, anchor=CENTER)
    endButton.place(x=winSizeX/2, y=(winSizeY/2)+80, anchor=CENTER)

# closeFunction
def endGameButton():
    win.destroy()

# startFirstLevelFunction
def startGameButton():
    clearWidgets()
    global level
    
    # playerTakesDamage
    playerTakesDamage()
    
    # placeObjects
    attackButton.place(x=winSizeX/2, y=winSizeY-40, anchor=CENTER)
    playerHealthPoints.place(x=winSizeX/2+((winSizeX/2)/2)+33, y=(winSizeY/2)+((winSizeY/2)/2)+50, anchor=CENTER)
    playerWriter.place(x=((winSizeX/2)/2)-25, y=(winSizeY/2)+((winSizeY/2)/2)+50, anchor=CENTER)
    playerLetters.place(x=winSizeX/2, y=60, anchor=CENTER)
    enemyHealthPoints.place(x=winSizeX/2, y=20, anchor=CENTER)
    enemyName.place(x=winSizeX/2, y=60, anchor=CENTER)
    levelIndication.place(x=winSizeX-50, y=10, anchor=NE)

# endFightMenuFunction
def afterFightMenu():
    global firstEnemyHealth, playerHealth
    # playerWon
    if firstEnemyHealth <= 0:
        youWonTitle.place(x=winSizeX/2, y=(winSizeY/2)-30, anchor=CENTER)
        backToMenuButton.place(x=(winSizeX/2)-100, y=(winSizeY/2)+20, anchor=CENTER)
        nextLvButton.place(x=(winSizeX/2)+100, y=(winSizeY/2)+20, anchor=CENTER)
        attackButton.config(state="disabled")
        playerWriter.config(state="disabled")
    # playerLost
    elif playerHealth <= 0:
        youLostTitle.place(x=winSizeX/2, y=(winSizeY/2)-30, anchor=CENTER)
        backToMenuButton.place(x=(winSizeX/2), y=(winSizeY/2)+30, anchor=CENTER)
        attackButton.config(state="disabled")
        playerWriter.config(state="disabled")

# resetForReturnToMainMenu
def returnToFirstLv():
    global firstEnemyHealth, level, nextEnemyHealth
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
    healPlayer()
    
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
def playerAttack():
    global firstEnemyHealth
    damage = 3
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
        win.after(1000, playerTakesDamage)
    # endFightMenuFunction
    afterFightMenu()

def damagePerLetter():
    pass

# objects on screen
# mainMenu !!!
nameGame            =   Label(win,text=nameOfGame,font=fntMenu)
startButton         =   Button(win,text="start",font=fntMenuBtn,command=delayStartGame,bg="grey",fg="white", width=9)
endButton           =   Button(win,text="close",font=fntMenuBtn,command=endGameButton,bg="grey",fg="white", width=9)

# fightEndedMenu !!!
youWonTitle         =   Label(win,text="you_defeated_enemy",font=fntMenu, fg="blue")
youLostTitle        =   Label(win,text="you_lost",font=fntMenu, fg="red")
backToMenuButton    =   Button(win, command=delayStartMenu, text="Back", font=fntMenuBtn, bg="blue", fg="white")
nextLvButton        =   Button(win, command=delayNextLevel, text="Next", font=fntMenuBtn, bg="blue", fg="white")

# gameStarted !!!
attackButton        =   Button(win,command=playerAttack,text="Attack", font=fntInGame, bg="red", fg="white")
playerHealthPoints  =   Label(win,text=str(playerHealth)+" hp",font=fntInGame,fg="red")
playerWriter        =   Entry(win, font=fntInGame, width=10)
playerLetters       =   Label(win)
enemyHealthPoints   =   Label(win,text=str(firstEnemyHealth),font=fntInGame,fg="red")
enemyName           =   Label(win,text=namesOfEnemy[randint(0, 3)], font=fntInGame)
levelIndication     =   Label(win,text=str(level)+"LV",font=fntInGame, fg="black")

# mainLoop !!!
mainMenu()
win.mainloop()