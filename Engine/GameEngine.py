from Utils.GameData import GameData as GD
import time
import random

class GameEngine(object):
    def __init__(self, fireclient, waterclient, snowclient):
        self.fclient = fireclient #object id 65 hp 66
        self.wclient = waterclient #object id 67 hp 68
        self.sclient = snowclient #object id 69 hp 70
        self.round = 1
        self.roundEnemys = []
        self.map = None

    def loadGame(self):
        self.map = random.randrange(1, 3)
        #self.loadAllSpritesAndMap()
        self.spawnPenguins()
        self.openUi()
        while not self.hasWonGame() and not self.hasLost():
            self.doNextRound()
        self.goToPayout()
        return

    def doNextRound(self):
        self.playRoundTitle()
        time.sleep(3)
        #wait for received animation done
        for x in GD["Enemies"]:
            if x["Round"+str(self.round)]["x"] != -1:
                self.createAndSpawnEnemy(x)
        while not self.hasWonRound() and not self.hasLost():
            self.showGrid()
            if not self.fclient.hasDisconnected:
                self.getMoves(self.fclient)
            if not self.wclient.hasDisconnected:
                self.getMoves(self.wclient)
            if not self.sclient.hasDisconnected:
                self.getMoves(self.sclient)
            self.startTimer()
            time.sleep(10)
            self.hideTimer()
            self.hideMoves()
            self.hideGrid()
            if not self.fclient.hasDisconnected and not self.fclient.usedPowerCard and not self.fclient.hp<=0:
                self.moveAndAttack(self.fclient)
            if not self.wclient.hasDisconnected and not self.wclient.usedPowerCard and not self.wclient.hp<=0:
                self.moveAndAttack(self.wclient)
            if not self.sclient.hasDisconnected and not self.sclient.usedPowerCard and not self.sclient.hp<=0:
                self.moveAndAttack(self.sclient)
            if self.numPowerCardsUsed()>1:
                self.playCombo()
            if self.fclient.usedPowerCard:
                self.playPowerCard(self.fclient)
            if self.wclient.usedPowerCard:
                self.playPowerCard(self.wclient)
            if self.sclient.usedPowerCard:
                self.playPowerCard(self.sclient)
            for x in self.roundEnemys:
                if x.hp<=0:
                    self.moveAndAttackEnemy(x)
        if self.hasWonRound():
            self.round+=1

    def sendToAllPlayers(self,handler):
        self.fclient.sendLine(handler)
        self.wclient.sendLine(handler)
        self.sclient.sendLine(handler)
        return

    def spawnPenguins(self):
        self.sendToAllPlayers("[O_HERE]|65|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
        self.sendToAllPlayers("[O_MOVE]|65|0.5|1|128")
        self.sendToAllPlayers("[O_ANIM]|65|0:100340|loop|800|1|0|12|1|0|0")

        self.sendToAllPlayers("[O_HERE]|66|0:1|0.5|1.0004|0|1|0|0|0|Actor63|0:30040|0|1|0")
        self.sendToAllPlayers("[O_SPRITE]|66|0:100395|1|")

        self.sendToAllPlayers("[O_HERE]|67|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
        self.sendToAllPlayers("[O_MOVE]|67|0.5|3|128")
        self.sendToAllPlayers("[O_ANIM]|67|0:100361|loop|800|1|0|12|1|0|0")

        self.sendToAllPlayers("[O_HERE]|68|0:1|0.5|3.0004|0|1|0|0|0|Actor64|0:30040|0|1|0")
        self.sendToAllPlayers("[O_SPRITE]|68|0:100395|1|")

        self.sendToAllPlayers("[O_HERE]|69|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
        self.sendToAllPlayers("[O_MOVE]|69|0.5|5|128")
        self.sendToAllPlayers("[O_ANIM]|69|0:100322|loop|700|1|0|13|2|0|0")

        self.sendToAllPlayers("[O_HERE]|70|0:1|0.5|5.0004|0|1|0|0|0|Actor65|0:30040|0|1|0")
        self.sendToAllPlayers("[O_SPRITE]|70|0:100395|1|")
        return

    def hasWonGame(self):
        if self.fclient.hp>0 or self.wclient.hp>0 or self.sclient.hp>0:
            if self.round >=5:
                return True
        return False

    def hasLost(self):
        if self.fclient.hp<=0 or self.wclient.hp<=0 or self.sclient.hp<=0:
            return True
        return False

    def goToPayout(self):
        self.sclient.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","initializationPayload":{"coinsEarned":5,"xpStart":95,"xpEnd":300,"rank":2,"doubleCoins":false,"isBoss":false,"round":2,"damage":0,"showItems":false},"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowpayout.swf","xPercent":0,"yPercent":0}')
        self.fclient.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","initializationPayload":{"coinsEarned":5,"xpStart":95,"xpEnd":300,"rank":2,"doubleCoins":false,"isBoss":false,"round":2,"damage":0,"showItems":false},"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowpayout.swf","xPercent":0,"yPercent":0}')
        self.wclient.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","initializationPayload":{"coinsEarned":5,"xpStart":95,"xpEnd":300,"rank":2,"doubleCoins":false,"isBoss":false,"round":2,"damage":0,"showItems":false},"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowpayout.swf","xPercent":0,"yPercent":0}')
        return

    def openUi(self):
        self.sclient.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","initializationPayload":{ "cardsAssetPath":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/","element":"snow","isMember":true },"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowui.swf","xPercent":0,"yPercent":0}')
        self.fclient.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","initializationPayload":{ "cardsAssetPath":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/","element":"fire","isMember":true },"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowui.swf","xPercent":0,"yPercent":0}')
        self.wclient.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","initializationPayload":{ "cardsAssetPath":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/","element":"water","isMember":true },"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowui.swf","xPercent":0,"yPercent":0}')
        return

    def playRoundTitle(self):
        self.sendToAllPlayers('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","triggerName":"update","initializationPayload":{ "bonusCriteria":"no_ko","roundNumber":'+str(self.round-1)+' },"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowrounds.swf","xPercent":0,"yPercent":0}')
        return

    def hasWonRound(self):
        for x in self.roundEnemys:
            if x.hp>0:
                return False
        return True

    def showGrid(self):
        self.sendToAllPlayers("[O_HERE]|413|0:100300|0|0|0|1|0|0|0||0:1|0|1|0")
        return

    def getMoves(self,client):
        pos1= client.positionX 
        pos2= client.positionY
        if self.isValidMove(pos1-2,pos2):
            client.sendLine("[O_HERE]|400|0:100063|"+str(pos1-2)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1-1,pos2):
            client.sendLine("[O_HERE]|401|0:100063|"+str(pos1-1)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1+2,pos2):
            client.sendLine("[O_HERE]|402|0:100063|"+str(pos1+2)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1+1,pos2):
            client.sendLine("[O_HERE]|403|0:100063|"+str(pos1+1)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1,pos2-2):
            client.sendLine("[O_HERE]|404|0:100063|"+str(pos1)+"|"+str(pos2-2)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1,pos2-1):
            client.sendLine("[O_HERE]|405|0:100063|"+str(pos1)+"|"+str(pos2-1)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1,pos2+2):
            client.sendLine("[O_HERE]|406|0:100063|"+str(pos1)+"|"+str(pos2+2)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1,pos2+1):
            client.sendLine("[O_HERE]|407|0:100063|"+str(pos1)+"|"+str(pos2+1)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1-1,pos2-1):
            client.sendLine("[O_HERE]|408|0:100063|"+str(pos1-1)+"|"+str(pos2-1)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1-1,pos2+1):
            client.sendLine("[O_HERE]|409|0:100063|"+str(pos1-1)+"|"+str(pos2+1)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1+1,pos2+1):
            client.sendLine("[O_HERE]|410|0:100063|"+str(pos1+1)+"|"+str(pos2+1)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1+1,pos2-1):
            client.sendLine("[O_HERE]|411|0:100063|"+str(pos1+1)+"|"+str(pos2-1)+"|0|1|0|0|0||0:1|0|1|0")
        if self.isValidMove(pos1,pos2):
            client.sendLine("[O_HERE]|412|0:100270|"+str(pos1)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
        if client.move==3:
            if self.isValidMove(pos1,pos2-3):
                client.sendLine("[O_HERE]|413|0:100063|"+str(pos1-2)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1-1,pos2-2):
                client.sendLine("[O_HERE]|414|0:100063|"+str(pos1-1)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1-2,pos2-1):
                client.sendLine("[O_HERE]|415|0:100063|"+str(pos1+2)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1-3,pos2):
                client.sendLine("[O_HERE]|416|0:100063|"+str(pos1+1)+"|"+str(pos2)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1-2,pos2+1):
                client.sendLine("[O_HERE]|417|0:100063|"+str(pos1)+"|"+str(pos2-2)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1-1,pos2+2):
                client.sendLine("[O_HERE]|418|0:100063|"+str(pos1)+"|"+str(pos2-1)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1,pos2+3):
                client.sendLine("[O_HERE]|419|0:100063|"+str(pos1)+"|"+str(pos2+2)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1+1,pos2+2):
                client.sendLine("[O_HERE]|420|0:100063|"+str(pos1)+"|"+str(pos2+1)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1+2,pos2+1):
                client.sendLine("[O_HERE]|421|0:100063|"+str(pos1-1)+"|"+str(pos2-1)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1+3,pos2):
                client.sendLine("[O_HERE]|422|0:100063|"+str(pos1-1)+"|"+str(pos2+1)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1+2,pos2+1):
                client.sendLine("[O_HERE]|423|0:100063|"+str(pos1+1)+"|"+str(pos2+1)+"|0|1|0|0|0||0:1|0|1|0")
            if self.isValidMove(pos1+1,pos2+2):
                client.sendLine("[O_HERE]|424|0:100063|"+str(pos1+1)+"|"+str(pos2-1)+"|0|1|0|0|0||0:1|0|1|0")
        return

    def hideMoves(self):
        for x in range(24):
            self.sendToAllPlayers("[O_HERE]|"+str(400+x)+"|0:100063|9999|9999|0|1|0|0|0||0:1|0|1|0")
        return

    def isValidMove(self,pos1,pos2):
        if pos1<=8.5 and pos2<=5 and pos1>=0.5 and pos2>=1:
            if pos1==2.5 and pos2==1 or pos1==6.5 and pos2 ==1 or pos1==2.5 and pos2 ==5 or pos1==6.5 and pos2 ==5:
                return False
            else:
                return True
        else:
            return False

    def startTimer(self):
        self.sendToAllPlayers('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","triggerName":"Timer_Start","initializationPayload":{ "element":"water","phase":1 },"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowtimer.swf","xPercent":0,"yPercent":0}')
        return

    def hideTimer(self):
        self.sendToAllPlayers('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","triggerName":"skipToTransitionOut","initializationPayload":{ "element":"water","phase":1 },"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowtimer.swf","xPercent":0,"yPercent":0}')
        return

    def hideGrid(self):
        self.sendToAllPlayers("[O_HERE]|413|0:100300|100|100|0|1|0|0|0||0:1|0|1|0")
        return

    def moveAndAttack(self,client):
        if client.element == "snow":
            if client.nextPositionX is not client.positionX or client.nextPositionY is not client.positionY:
                self.sendToAllPlayers("[O_ANIM]|67|0:100371|loop|800|1|0|12|1|0|0")
                self.sendToAllPlayers("[O_SLIDE]|67|"+str(client.nextPositionX)+"|"+str(client.nextPositionY)+"|1000")
                self.sendToAllPlayers("[O_SLIDE]|68|"+str(client.nextPositionX)+"|"+str(client.nextPositionY)+"|1000")
                time.sleep(1)
            if client.nextAttack != -1:
                if client.nextAttack == 1:
                    self.sendToAllPlayers("[O_ANIM]|67|0:100362|play_once|800|1|0|12|1|0|0")
                if client.nextAttack == 2:
                    self.sendToAllPlayers("[O_ANIM]|67|0:100377|loop|800|1|0|12|1|0|0")
                time.sleep(1)
                client.nextAttack=-1
            self.sendToAllPlayers("[O_ANIM]|67|0:100361|loop|800|1|0|12|1|0|0")
        if client.element == "fire":
            if client.nextPositionX is not client.positionX or client.nextPositionY is not client.positionY:
                self.sendToAllPlayers("[O_ANIM]|65|0:100341|loop|800|1|0|12|1|0|0")
                self.sendToAllPlayers("[O_SLIDE]|65|"+str(client.nextPositionX)+"|"+str(client.nextPositionY)+"|1000")
                self.sendToAllPlayers("[O_SLIDE]|66|"+str(client.nextPositionX)+"|"+str(client.nextPositionY)+"|1000")
                time.sleep(1)
            if client.nextAttack != -1:
                if client.nextAttack == 1:
                    self.sendToAllPlayers("[O_ANIM]|65|0:100343|play_once|800|1|0|12|1|0|0")
                if client.nextAttack == 2:
                    self.sendToAllPlayers("[O_ANIM]|65|0:100360|loop|800|1|0|12|1|0|0")
                time.sleep(1)
                client.nextAttack=-1
            self.sendToAllPlayers("[O_ANIM]|65|0:100340|loop|800|1|0|12|1|0|0")
        if client.element == "water":
            if client.nextPositionX is not client.positionX or client.nextPositionY is not client.positionY:
                self.sendToAllPlayers("[O_ANIM]|69|0:100323|loop|800|1|0|12|1|0|0")
                self.sendToAllPlayers("[O_SLIDE]|69|"+str(client.nextPositionX)+"|"+str(client.nextPositionY)+"|1000")
                self.sendToAllPlayers("[O_SLIDE]|70|"+str(client.nextPositionX)+"|"+str(client.nextPositionY)+"|1000")
                time.sleep(1)
            if client.nextAttack != -1:
                if client.nextAttack == 1:
                    self.sendToAllPlayers("[O_ANIM]|69|0:100321|play_once|800|1|0|12|1|0|0")
                if client.nextAttack == 2:
                    self.sendToAllPlayers("[O_ANIM]|69|0:100333|play_once|800|1|0|12|1|0|0")
                time.sleep(1)
                client.nextAttack=-1
            self.sendToAllPlayers("[O_ANIM]|69|0:100322|loop|800|1|0|12|1|0|0")
        return

    def numPowerCardsUsed(self):
        powercardsnum=0
        if self.fclient.usedPowerCard:
            powercardsnum+=1
        if self.wclient.usedPowerCard:
            powercardsnum+=1
        if self.sclient.usedPowerCard:
            powercardsnum+=1
        return powercardsnum

    def playCombo(self):
        if self.numPowerCardsUsed()==2:
            powersarray = []
            if self.fclient.usedPowerCard:
                powersarray.append("fire")
            if self.wclient.usedPowerCard:
                powersarray.append("water")
            if self.sclient.usedPowerCard:
                powersarray.append("snow")
            self.sendToAllPlayers('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","initializationPayload":{ "data":["'+str(powersarray[0])+'","'+str(powersarray[1])+'"],"snow":true,"fire":false,"sensei":false,"numSlices":2 },"water":"true","numSlices":2,"snow":true,"fire":false,"sensei":false ,"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowcombos.swf","xPercent":0,"yPercent":0}')
        if self.numPowerCardsUsed()==3:
            self.sendToAllPlayers('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","initializationPayload":{ "data":["snow","fire","water"],"snow":true,"fire":false,"sensei":false,"numSlices":3 },"water":"true","numSlices":2,"snow":true,"fire":false,"sensei":false ,"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowcombos.swf","xPercent":0,"yPercent":0}')
        return

    def playPowerCard(self,client):
        if client.element == "snow": #67 anim id 100371
            self.sendToAllPlayers("[O_ANIM]|67|0:100371|play_once|800|1|0|12|1|0|0")
            time.sleep(1)
            self.sendToAllPlayers("[O_HERE]|80|0:1|"+str(client.positionX)+"|"+str(client.positionY)+"|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|80|0:100370|loop|800|1|0|12|1|0|0")
            self.sendToAllPlayers("[O_HERE]|81|0:1|"+str(client.powerCardX)+"|"+str(client.powerCardY)+"|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|81|0:8740003|loop|800|1|0|12|1|0|0")
            time.sleep(1)
            self.sendToAllPlayers("[O_HERE]|80|0:1|999|999|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_HERE]|81|0:1|999|999|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|67|0:100361|loop|700|1|0|13|2|0|0")
        if client.element == "fire": #65 anim id 100378
            self.sendToAllPlayers("[O_ANIM]|65|0:100378|play_once|800|1|0|12|1|0|0")
            time.sleep(1)
            self.sendToAllPlayers("[O_HERE]|82|0:1|"+str(client.positionX)+"|"+str(client.positionY)+"|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|82|0:100345|loop|800|1|0|12|1|0|0")
            self.sendToAllPlayers("[O_HERE]|83|0:1|"+str(client.powerCardX)+"|"+str(client.powerCardY)+"|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|83|0:100344|loop|800|1|0|12|1|0|0")
            time.sleep(1)
            self.sendToAllPlayers("[O_HERE]|82|0:1|999|999|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_HERE]|83|0:1|999|999|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|65|0:100340|loop|700|1|0|13|2|0|0")
        if client.element == "water": #69 anim id 100329
            self.sendToAllPlayers("[O_ANIM]|69|0:100329|play_once|800|1|0|12|1|0|0")
            time.sleep(1)
            self.sendToAllPlayers("[O_HERE]|84|0:1|"+str(client.positionX)+"|"+str(client.positionY)+"|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|84|0:100330|loop|800|1|0|12|1|0|0")
            self.sendToAllPlayers("[O_HERE]|85|0:1|"+str(client.powerCardX)+"|"+str(client.powerCardY)+"|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|85|0:100328|play_once|800|1|0|12|1|0|0")
            time.sleep(1)
            self.sendToAllPlayers("[O_HERE]|84|0:1|999|999|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_HERE]|85|0:1|999|999|0|1|0|0|0||0:1|0|1|0")
            self.sendToAllPlayers("[O_ANIM]|69|0:100322|loop|700|1|0|13|2|0|0")
        return

    def moveAndAttackEnemy(self,enemy):
        time.sleep(2)
        return

    def createAndSpawnEnemy(self,enemy):
        enemyObject = Enemy(enemy["name"],enemy["IDDesign"],enemy["HP"],enemy["Range"],enemy["Attack"],enemy["Move"])
        self.roundEnemys.append(enemyObject)
        self.sendToAllPlayers("[O_HERE]|"+str(enemyObject.id)+"|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
        self.sendToAllPlayers("[O_MOVE]|"+str(enemyObject.id)+"|"+str(enemyObject.getSpawn("x",self.round))+"|"+str(enemyObject.getSpawn("y",self.round))+"|128")
        self.sendToAllPlayers("[O_ANIM]|"+str(enemyObject.id)+"|0:"+str(enemyObject.getAnim("idle"))+"|loop|800|1|0|12|1|0|0")
        return

    def loadAllSpritesAndMap(self):
        self.sendToAllPlayers('[UI_CLIENTEVENT]|101|receivedJson|{"type":"playAction","action":"closeWindow","targetWindow":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowplayerselect.swf"}')
        self.sendToAllPlayers("[O_GONE]|4")
        self.sendToAllPlayers("[W_PLACE]|0:10001|8|1")
        self.sendToAllPlayers("[W_INPUT]|use|0:10|2|3|0|use|")
        self.sendToAllPlayers("[W_INPUT]|touch-the-terrain|0:8600033|1|6|0|/path_terrain|")
        self.sendToAllPlayers("[W_INPUT]|mouse-the-terrain|0:8600033|1|3|0|/path_terrain|")
        self.sendToAllPlayers("[P_MAPBLOCK]|t|1|1|iVBORw0KGgoAAAANSUhEUgAAAAkAAAAFCAAAAACyOJm3AAAAHUlEQVQImWNgZeRkZARidgZGCGBnZ2CFMVHEoOoADJEAhIsKxDUAAAAASUVORK5CYII=")
        self.sendToAllPlayers("[P_MAPBLOCK]|h|1|1|iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAAAAADfm1AaAAAADklEQVQImWNogAMG8pgA3m8eAacnkzQAAAAASUVORK5CYII=")
        self.sendToAllPlayers("[P_ZOOMLIMIT]|-1.000000|-1.000000")
        self.sendToAllPlayers("[P_RENDERFLAGS]|0|48")
        self.sendToAllPlayers("[P_SIZE]|9|5")
        self.sendToAllPlayers("[P_VIEW]|5")
        self.sendToAllPlayers("[P_START]|4.5|2.5|0")
        self.sendToAllPlayers("[P_LOCKVIEW]|0")
        self.sendToAllPlayers("[P_TILESIZE]|100")
        self.sendToAllPlayers("[P_ELEVSCALE]|0.031250")
        self.sendToAllPlayers("[P_RELIEF]|1")
        self.sendToAllPlayers("[P_LOCKSCROLL]|1|0|0|573321786")
        self.sendToAllPlayers("[P_HEIGHTMAPSCALE]|0.078125|128")
        self.sendToAllPlayers("[P_HEIGHTMAPDIVISIONS]|1")
        self.sendToAllPlayers("[P_CAMERA3D]|0.000000|0.000000|0.000000|0.000000|0.000000|0.000000|0.000000|0.000000|0|0.000000|0.000000|0.000000|0.000000|0.000000|0.000000|864397819904.000000|0.000000|0|0")
        self.sendToAllPlayers("[UI_BGCOLOR]|0|0|0")
        self.sendToAllPlayers("[P_DRAG]|0")
        self.sendToAllPlayers("[P_CAMLIMITS]|0|0|0|0")
        self.sendToAllPlayers("[P_LOCKRENDERSIZE]|0|1024|768")
        self.sendToAllPlayers("[P_LOCKOBJECTS]|0")
        self.sendToAllPlayers("[UI_BGSPRITE]|0:-1|0|1.000000|1.000000")
        self.sendToAllPlayers("[P_TILE]|0||0|0|1|0:2|Empty Tile|0|0|0|0:7940012")
        self.sendToAllPlayers("[P_TILE]|1||0|0|1|0:2|open|0|0|0|0:7940013")
        self.sendToAllPlayers("[P_TILE]|2||0|0|1|0:3|enemy|0|0|0|0:7940014")
        self.sendToAllPlayers("[P_TILE]|3||0|0|1|0:4|penguin|0|0|0|0:7940015")
        self.sendToAllPlayers("[P_TILE]|4||0|0|1|0:100002|penguin_spawn_occupied|0|0|0|0:7940016")
        self.sendToAllPlayers("[P_TILE]|5||0|0|1|0:6|penguin_spawn_unoccupied|0|0|0|0:7940017")
        self.sendToAllPlayers("[P_TILE]|7||0|0|1|0:10003|enemy_spawn_unoccupied|0|0|0|0:7940018")
        self.sendToAllPlayers("[P_TILE]|8||0|0|1|0:10004|enemy_spawn_occupied|0|0|0|0:7940019")
        self.sendToAllPlayers("[P_TILE]|9||0|0|1|0:10005|obstacle|0|0|0|0:7940020")
        self.sendToAllPlayers("[P_PHYSICS]|0|0|0|0|0|0|0|1")
        self.sendToAllPlayers("[P_ASSETSCOMPLETE]|0|0")
        self.sendToAllPlayers("[O_HERE]|9|0:1|10.7667|5.92222|0|1|0|0|0|Actor5|0:30021|0|0|0")
        self.sendToAllPlayers("[O_HERE]|10|0:1|4.48869|-1.11106|0|1|0|0|0|Actor6|0:10002|0|0|0")
        self.sendToAllPlayers("[O_HERE]|11|0:1|4.5|6.1|0|1|0|0|0|Actor7|0:6740006|0|0|0")
        self.sendToAllPlayers("[P_CAMERA]|4.5|2.49333|0|0|1")
        self.sendToAllPlayers("[P_ZOOM]|1.000000")
        self.sendToAllPlayers("[P_LOCKZOOM]|1")
        self.sendToAllPlayers("[P_LOCKCAMERA]|1")
        self.sendToAllPlayers("[O_PLAYER]|4|")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100307")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100319")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100303")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100308")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100318")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100306")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100310")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100312")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100315")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100316")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100317")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100313")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100314")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100302")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100299")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100240")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100241")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100309")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100320")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100304")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:1840011")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:1840012")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:1840010")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100307")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100319")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100303")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100308")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100318")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100306")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100310")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100312")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100315")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100316")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100317")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100313")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100314")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100302")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100299")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100240")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100241")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100309")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100320")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:100304")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:1840011")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:1840012")
        self.sendToAllPlayers("[S_LOADSPRITE]|0:1840010")
        self.sendToAllPlayers('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","assetPath":"","initializationPayload":[null],"layerName":"bottomLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowclose.swf","xPercent":1,"yPercent":0}')
        self.sendToAllPlayers("[O_SPRITE]|10|0:100380|0|")
        self.sendToAllPlayers("[O_SPRITE]|11|0:1|0|")
        self.sendToAllPlayers("[O_HERE]|14|0:1|0.5|0.9998|0|1|0|0|0|Actor14|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|15|0:1|0.5|1.9998|0|1|0|0|0|Actor15|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|16|0:1|0.5|2.9998|0|1|0|0|0|Actor16|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|17|0:1|0.5|3.9998|0|1|0|0|0|Actor17|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|18|0:1|0.5|4.9998|0|1|0|0|0|Actor18|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|19|0:1|1.5|0.9998|0|1|0|0|0|Actor19|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|20|0:1|1.5|1.9998|0|1|0|0|0|Actor20|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|21|0:1|1.5|2.9998|0|1|0|0|0|Actor21|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|22|0:1|1.5|3.9998|0|1|0|0|0|Actor22|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|23|0:1|1.5|4.9998|0|1|0|0|0|Actor23|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|24|0:1|2.5|0.9998|0|1|0|0|0|Actor24|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|25|0:1|2.5|1.9998|0|1|0|0|0|Actor25|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|26|0:1|2.5|2.9998|0|1|0|0|0|Actor26|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|27|0:1|2.5|3.9998|0|1|0|0|0|Actor27|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|28|0:1|2.5|4.9998|0|1|0|0|0|Actor28|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|29|0:1|3.5|0.9998|0|1|0|0|0|Actor29|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|30|0:1|3.5|1.9998|0|1|0|0|0|Actor30|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|31|0:1|3.5|2.9998|0|1|0|0|0|Actor31|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|32|0:1|3.5|3.9998|0|1|0|0|0|Actor32|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|33|0:1|3.5|4.9998|0|1|0|0|0|Actor33|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|34|0:1|4.5|0.9998|0|1|0|0|0|Actor34|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|35|0:1|4.5|1.9998|0|1|0|0|0|Actor35|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|36|0:1|4.5|2.9998|0|1|0|0|0|Actor36|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|37|0:1|4.5|3.9998|0|1|0|0|0|Actor37|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|38|0:1|4.5|4.9998|0|1|0|0|0|Actor38|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|39|0:1|5.5|0.9998|0|1|0|0|0|Actor39|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|40|0:1|5.5|1.9998|0|1|0|0|0|Actor40|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|41|0:1|5.5|2.9998|0|1|0|0|0|Actor41|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|42|0:1|5.5|3.9998|0|1|0|0|0|Actor42|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|43|0:1|5.5|4.9998|0|1|0|0|0|Actor43|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|44|0:1|6.5|0.9998|0|1|0|0|0|Actor44|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|45|0:1|6.5|1.9998|0|1|0|0|0|Actor45|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|46|0:1|6.5|2.9998|0|1|0|0|0|Actor46|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|47|0:1|6.5|3.9998|0|1|0|0|0|Actor47|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|48|0:1|6.5|4.9998|0|1|0|0|0|Actor48|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|49|0:1|7.5|0.9998|0|1|0|0|0|Actor49|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|50|0:1|7.5|1.9998|0|1|0|0|0|Actor50|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|51|0:1|7.5|2.9998|0|1|0|0|0|Actor51|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|52|0:1|7.5|3.9998|0|1|0|0|0|Actor52|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|53|0:1|7.5|4.9998|0|1|0|0|0|Actor53|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|54|0:1|8.5|0.9998|0|1|0|0|0|Actor54|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|55|0:1|8.5|1.9998|0|1|0|0|0|Actor55|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|56|0:1|8.5|2.9998|0|1|0|0|0|Actor56|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|57|0:1|8.5|3.9998|0|1|0|0|0|Actor57|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|58|0:1|8.5|4.9998|0|1|0|0|0|Actor58|0:30020|0|1|0")
        self.sendToAllPlayers("[O_HERE]|59|0:100394|2.5|1|0|1|0|0|0|Actor59|0:100145|0|1|0")
        self.sendToAllPlayers("[O_SPRITE]|59|0:100394|0|")
        self.sendToAllPlayers("[O_HERE]|60|0:100394|6.5|1|0|1|0|0|0|Actor60|0:100145|0|1|0")
        self.sendToAllPlayers("[O_SPRITE]|60|0:100394|0|")
        self.sendToAllPlayers("[O_HERE]|61|0:100394|2.5|5|0|1|0|0|0|Actor61|0:100145|0|1|0")
        self.sendToAllPlayers("[O_SPRITE]|61|0:100394|0|")
        self.sendToAllPlayers("[O_HERE]|62|0:100394|6.5|5|0|1|0|0|0|Actor62|0:100145|0|1|0")
        self.sendToAllPlayers("[O_SPRITE]|62|0:100394|0|")
        self.sendToAllPlayers("[P_TILECHANGE]|0|0|4")
        self.sendToAllPlayers("[P_TILECHANGE]|0|4|4")
        self.sendToAllPlayers("[P_TILECHANGE]|0|2|4")
        return


class Enemy(object):
    def __init__(self,name,id,hp,range,power,move):
        self.name = name
        self.id = id
        self.hp = hp
        self.range = range
        self.power = power
        self.move = move
        self.positionX = 0
        self.positionY = 0

    def getEnemyData(self):
        for x in GD["Enemies"]:
            if x["name"] == self.name:
                return x
        return 0

    def getSpawn(self,cordinate,round):
        enemyData = self.getEnemyData()
        if cordinate == "x":
            self.positionX = enemyData["Round"+str(round)]["x"]
        if cordinate == "y":
            self.positionY = enemyData["Round"+str(round)]["y"]
        return enemyData["Round"+str(round)][cordinate]

    def getAnim(self,anim):
        enemyData = self.getEnemyData()
        return enemyData[anim+"Anim"]
