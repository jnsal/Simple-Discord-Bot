# States:
# -1 - Deadlole
# 0  - Open
# 1  - Closed
# 2  - Finished?
import json
import os


class Tournament():
    def __init__(self, name = "Default_Tournament", desc = '', date = '', prize = 'Pika'):
        self.__name = name
        self.__winner = None
        self.__count = 0
        self.__match = []
        self.__state = 0

        self.__player_name   = []
        self.__active_player = []
        self.__desc = desc
        self.__date = date # TODO: Need to implement date of tournament
        self.__prize = prize
        self.__icon = '' # TODO: Add a icon to the tournament _Optional_

        self.__tournament_path = str(os.getenv('TOURNAMENT_PATH'))

        self.__prev_match = []

        self.__bo = 5
        
        if name != "Default_Tournament":
            self.saveFile()


    def removePlayer(self, player):
        if self.__state != 0 or len(self.__player_name) < 1:
            return False
        found = False

        for name in self.__player_name:
            if player == name:
                found = True
                break
        if not found:
            return False

        self.__player_name.remove(player)
        self.__active_player.remove(player)
        self.saveFile(True)
        return True
    
    def setDesc(self, desc):
        self.__desc = desc

    def addPlayer(self, *player):
        if self.__state == 0:
            self.__player_name += player
            self.__active_player += player
            self.__count += 1
            self.saveFile(True)
        else: # Tornament closed!
            return -1 

    def __checkActiveParticipant(self):
        for match in self.__match:
            if match[2] > match[3]:
                self.__active_player.remove(match[1])
                self.__count -= 1
            else:
                self.__active_player.remove(match[0])
                self.__count -= 1

    def key(self, rematch = False):
        if rematch:
            self.__prev_match.append(self.__match.copy())
            self.__checkActiveParticipant()
            self.__match.clear()
        if self.__state == 0:
            self.__state = 1
        if self.__count % 2 == 0:
            for i in range(int(self.__count / 2)):# PLAYER1 PLAYER2 V1 V2
                self.__match.append([self.__active_player[i], self.__player_name[self.__count - i - 1], 0, 0])
                i += 1
            self.saveFile(True)
        else:
            return

    def setMode(self, best_of = 3):
        self.__bo = best_of
        self.saveFile(True)


    def getMatches(self):
        return self.__match
    def getName(self):
        return self.__name
    def getDesc(self):
        return self.__desc
    def getPrize(self):
        return self.__prize
    def getHistory(self):
        return self.__prev_match
    def getType(self):
        return self.__bo

    def __checkMatch(self, match):
        return (self.__match[match][2] > self.__bo / 2) or (self.__match[match][3] > self.__bo / 2)

        # return ((self.__match[match][2] + self.__match[match][3]) > self.__bo + 1) or (self.__match[match][2] >= self.__bo / 2) or (self.__match[match][3] >= self.__bo / 2) 


    def vsMatch(self, match, w):
        if self.__checkMatch(match) == True:
            return
        n = -69
        if self.__match[match][0] == w:
            n = 2
        else:
            n = 3

        self.__match[match][n] += 1 
        if self.__checkMatch(match):
            ended = True
            for i in range(len(self.__match)):
                if not self.__checkMatch(i):
                    ended = False
            if ended:
                self.key(True)

        self.saveFile(True)

    def closeTournament(self):
        self.__state = 1

    def saveFile(self, overwrite = False):
        with open(self.__tournament_path, 'r') as file:
            data = json.load(file)

        found = False
        for tournament in data:
            if tournament == self.__name:
                found = True
                if not overwrite:
                    return False
        export = {
        self.__name: {
            "State": self.__state,
            "Type": self.__bo,
            "Players": self.__player_name,
            "Active": self.__active_player,
            "History": self.__prev_match,
            "Match": self.__match,
            "Prize": self.__prize,
            "Description": self.__desc
        }}

        if not found:
            data = {**export, **data}
        else:
            data.update(export)

        with open(self.__tournament_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return

    def loadFile(self, name, path):
        with open(path, 'r') as file:
            data = json.load(file)
        found = False

        for tournament in data:
            if tournament == name:
                found = True
        if not found:
            return False

        self.__name = name
        self.__bo = data[name]['Type']
        self.__player_name = data[name]['Players']
        self.__active_player = data[name]['Active']
        self.__prev_match = data[name]['History']
        self.__match = data[name]['Match']
        self.__state = data[name]['State']
        self.__count = len(self.__active_player)
        self.__desc = data[name]['Description']
        self.__prize = data[name]['Prize']

        return True









































