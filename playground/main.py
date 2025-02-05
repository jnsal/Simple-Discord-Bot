# Tournament print example

# A------
#        | A------
# B------         |
# 		          | B------
# C------         |        |
#        | B------         |
# D------                  |
#                          | B
# E------                  |
#        | E------         |
# F------         |        |
# 		          | E------
# G------         |
#        | G------
# H------

import json

class Participant():
    def __init__(self, name = "foo", alias = "bar"):
        self.__name = name
        self.__alias = ""

        if (alias == "bar"):
            self.__alias = name[0:4]
        else:
            self.__alias = alias
    
    
    
    def getAlias(self):
        return self.__alias
    def getName(self):
        return self.__name


class Tournament():
    def __init__(self):
        self.owner = ""
        self.participants = []
        self.key_tournament = ""
        self.match = []
        self.match_history = []
        self.__joinable = True

    # Create Advance phase to make new matches
    def addParticipant(self, participant):
        if (self.__joinable != True):
            print("Tournament is closed!")
            return 0
        
        self.participants += participant
    def closeTournament(self):
        self.__joinable = False

    def saveTournament(self, name):
        save = {
                "name": name,
        }
        return

    def makeMatch(self):
        if (len(self.participants) == 1):
            print("We have a winner:", self.participants[0])
            return
        
        if (self.match != []):
            self.match_history.append(self.match.copy())
            self.match.clear()

        qnt = len(self.participants)
        for i in range(0, int(qnt/2)):
            self.match.append([self.participants[i]] + [self.participants[int(qnt-1) - i]])
    
    def vsMatch(self, winner):
        if (self.__joinable):
            self.__joinable = False

        for match in self.match:
            if (match[0] == winner):
                self.participants.remove(match[1])
            elif (match[1] == winner):
                self.participants.remove(match[0])

    def printTournament(self):
        print("length of match", len(self.match), '\n')
        for match in self.match:
            for player in match:
                self.key_tournament += player + 5 * '-'
                if (player != match[1]):
                    self.key_tournament += '\n' + 6 * ' ' + '|\n'
                elif (match != self.match[len(self.match) - 1]):
                    self.key_tournament += '\n\n'
        self.p_tournament = True

        print(self.key_tournament)
    
    def printParticipants(self):
        for participant in self.participants:
            print(participant)


def main():
    snooker = Tournament()

    snooker.addParticipant('A')
    snooker.addParticipant('B')
    snooker.addParticipant('C')
    snooker.addParticipant('D')
    snooker.addParticipant('E')
    snooker.addParticipant('F')
    snooker.addParticipant('G')
    snooker.addParticipant('H')
    snooker.closeTournament()
    snooker.makeMatch()
    
    snooker.printTournament()

    #print('\n------------------------------------\n')

    snooker.key_tournament = ''
    snooker.vsMatch('A')
    snooker.vsMatch('B')
    snooker.vsMatch('F')
    snooker.vsMatch('D')
    
    snooker.makeMatch()
    snooker.vsMatch('A')
    snooker.vsMatch('D')
    snooker.makeMatch()

    snooker.vsMatch('A')
    snooker.makeMatch()

    #snooker.printParticipants()
    #snooker.printTournament()



if __name__ == "__main__":
    main()
