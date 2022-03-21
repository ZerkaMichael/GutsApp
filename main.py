import json
import kivy
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from os import path

filename = 'scores.json'

class HomeWindow(Screen):
    pass

class ScoreCounterWindow(Screen):
    def submit(self):
        game = {'Team1': self.ids.team1_name.text, 'Team2': self.ids.team2_name.text, 'Score1': self.ids.score1_input.text, 'Score2': self.ids.score2_input.text}
        with open(filename, 'r+') as file:
            data = json.load(file)
            data["games"].append(game)
            file.seek(0)
            json.dump(data, file, indent = 4)

    def addScore(self, team):
        if team == 1:
            score1 = int(self.ids.score1_input.text)
            score1 += 1
            self.ids.score1_input.text = str(score1)
        else:
            score2 = int(self.ids.score2_input.text)
            score2 += 1
            self.ids.score2_input.text = str(score2)

    def subScore(self, team):
        if team == 1:
            score1 = int(self.ids.score1_input.text)
            score1 -= 1
            self.ids.score1_input.text = str(score1)
        else:
            score2 = int(self.ids.score2_input.text)
            score2 -= 1
            self.ids.score2_input.text = str(score2)

class MatchHistoryWindow(Screen):
    def history(self, i):
        with open(filename, 'r+') as file:
            data = json.load(file)
            if i <= len(data["games"]):
                info = str(data["games"][-abs(i)]).replace(', ', '\n')
                info = info.replace('{', '')
                info = info.replace('}', '')
                info = info.replace("'", '')
                return info
            else:
                return str("N/A")

    def updateGames(self):
        self.ids.match1.text = self.history(1)
        self.ids.match2.text = self.history(2)
        self.ids.match3.text = self.history(3)
        self.ids.match4.text = self.history(4)
        self.ids.match5.text = self.history(5)
        self.ids.match6.text = self.history(6)
        self.ids.match7.text = self.history(7)
        self.ids.match8.text = self.history(8)

class TournamentWindow(Screen):
    teamList = ListProperty(["[None]"])
    finishedTeamList = ListProperty(["[None]"])
    def getMatches(self):
        with open('currentTournament.json', 'r') as file:
            data = json.load(file)
            teamList = []
            for i in range(len(data["gamedata"]["currentmatches"])):
                temp = str(data["gamedata"]["currentmatches"][i]["Round"]) + " | " + data["gamedata"]["currentmatches"][i]["Text"]
                teamList.append(temp)
            self.teamList = teamList

    def getFinishedMatches(self):
        with open('currentTournament.json', 'r') as file:
            data = json.load(file)
            finishedTeamList = []
            for i in range(len(data["gamedata"]["finishedmatches"])):
                temp = str(data["gamedata"]["finishedmatches"][i]["Round"]) + " | " + data["gamedata"]["finishedmatches"][i]["Text"] + " | " + str(data["gamedata"]["finishedmatches"][i]["FinalScore"])
                finishedTeamList.append(temp)
            self.finishedTeamList = finishedTeamList

    def matchSelection(self, text):
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            text = text.split(" | ")
            for i in range(len(data["gamedata"]["currentmatches"])):
                temp = data["gamedata"]["currentmatches"][i]
                if text[1] in temp["Text"]:
                    temp["FinalScore"] = self.ids.score1_input.text+'-'+self.ids.score2_input.text
                    file.seek(0)
                    json.dump(data, file, indent = 4)

    def nextRound(self):
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            currentRound = data["gamedata"]["currentmatches"][0]["Round"]
            round = currentRound+1
            TournamentWindow.wlHandler(self, data, 0)
            temp = data["gamedata"]["currentmatches"]
            data["gamedata"]["currentmatches"] = []
            data["gamedata"]["finishedmatches"] += temp
            file.truncate(0)
            file.seek(0)
            TournamentWindow.constructNextRound(self, round, data)
            json.dump(data, file, indent = 4)



    def wlHandler(self, data, type):
        if type == 0:
            type = "Round Robin"
        elif type == 1:
            type = "W/L"
        for i in range(len(data["gamedata"]["currentmatches"])):
            score = data["gamedata"]["currentmatches"][i]["FinalScore"].split('-')
            team1Name = data["gamedata"]["currentmatches"][i]["Team1"]
            team2Name = data["gamedata"]["currentmatches"][i]["Team2"]
            dif = int(score[0])-int(score[1])
            print(score)
            for x in range(len(data["gamedata"]["teamdata"])):
                temp = 0
                if data["gamedata"]["teamdata"][x]["Team"] == team1Name:
                    if int(score[0]) >= 21 & int(score[0]) > int(score[1]):
                        newWL = data["gamedata"]["teamdata"][x][type].split('-')
                        temp = int(newWL[0])+1
                        data["gamedata"]["teamdata"][x][type] = str(temp)+"-"+str(newWL[1])
                        data["gamedata"]["teamdata"][x]["Dif"] += dif
                        print(data["gamedata"]["teamdata"][x][type])
                    elif int(score[1]) >= 21 & int(score[1]) > int(score[0]):
                        newWL = data["gamedata"]["teamdata"][x][type].split('-')
                        temp = int(newWL[1])+1
                        data["gamedata"]["teamdata"][x][type] = str(newWL[0])+"-"+str(temp)
                        print(data["gamedata"]["teamdata"][x][type])
                        data["gamedata"]["teamdata"][x]["Dif"] -= dif
                if data["gamedata"]["teamdata"][x]["Team"] == team2Name:
                    if int(score[0]) >= 21 & int(score[0]) > int(score[1]):
                        newWL = data["gamedata"]["teamdata"][x][type].split('-')
                        temp = int(newWL[1])+1
                        data["gamedata"]["teamdata"][x][type] = str(newWL[0])+"-"+str(temp)
                        data["gamedata"]["teamdata"][x]["Dif"] -= dif
                        print(data["gamedata"]["teamdata"][x][type])
                    elif int(score[1]) >= 21 & int(score[1]) > int(score[0]):
                        newWL = data["gamedata"]["teamdata"][x][type].split('-')
                        temp = int(newWL[0])+1
                        data["gamedata"]["teamdata"][x][type] = str(temp)+"-"+str(newWL[1])
                        print(data["gamedata"]["teamdata"][x][type])
                        data["gamedata"]["teamdata"][x]["Dif"] += dif



    def constructNextRound(self, round, data):
        teams = data["gamedata"]["teams"]
        teamCount = len(teams)
        unmatched = list(range(0,teamCount))
        match = 0
        rounds = data["gamedata"]["gamedata"][0]["rrRounds"]
        if round <= rounds:
            if (teamCount % 2) == 0:
                i = 1
                gamesAmount = teamCount/2
                while match < gamesAmount:
                    random.shuffle(unmatched)
                    selTeam1 = unmatched[0]
                    selTeam2 = unmatched[1]
                    team1 = data["gamedata"]["teams"][selTeam1]
                    team2 = data["gamedata"]["teams"][selTeam2]
                    newMatch = {"Round": round, "Team1": team1, "Team2": team2, "FinalScore": "0-0", "Text": team1+" vs "+team2}
                    data["gamedata"]["currentmatches"].append(newMatch)
                    i += 1
                    match += 1
                    unmatched.remove(selTeam1)
                    unmatched.remove(selTeam2)
        else:
            if (teamCount % 2) == 0:
                print('smaids')

    def seedCalculation(self, data):
        for i in range(len(data["gamedata"]["teamdata"])):
            name = data["gamedata"]["teamdata"][i]["Team"]
            rr = data["gamedata"]["teamdata"][i]["Round Robin"].split('-')
            dif = data["gamedata"]["teamdata"][i]["Dif"]



class AdminWindow(Screen):
    def submitTeams(self):
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            newTeam = self.ids.team_input.text
            data["gamedata"]["teams"].append(newTeam)
            file.seek(0)
            json.dump(data, file, indent = 4)

    def getTeams(self):
        with open('currentTournament.json', 'r') as file:
            data = json.load(file)
            return data["gamedata"]["teams"]

    def removeTeam(self, team):
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            if team in data["gamedata"]["teams"]:
                data["gamedata"]["teams"].remove(team)
                file.truncate(0)
                file.seek(0)
                json.dump(data, file, indent = 4)

    def startTournament(self):
        unmatched = []
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            teams = data["gamedata"]["teams"]
            teamCount = len(teams)
            unmatched = list(range(0,teamCount))
            match = 0
            data["gamedata"]["gamedata"][0]["rrRounds"] = int(self.ids.roundrobin_rounds.text)
            if (teamCount % 2) == 0:
                i = 1
                gamesAmount = teamCount/2
                while match < gamesAmount:
                    random.shuffle(unmatched)
                    selTeam1 = unmatched [0]
                    selTeam2 = unmatched[1]
                    team1 = data["gamedata"]["teams"][selTeam1]
                    team2 = data["gamedata"]["teams"][selTeam2]
                    AdminWindow.constructTeamData(self, data, team1, team2)
                    newMatch = {"Round": 1, "Team1": team1, "Team2": team2, "FinalScore": "0-0", "Text": team1+" vs "+team2}
                    data["gamedata"]["currentmatches"].append(newMatch)
                    i += 1
                    match += 1
                    unmatched.remove(selTeam1)
                    unmatched.remove(selTeam2)
                file.truncate(0)
                file.seek(0)
                json.dump(data, file, indent = 4)

    def constructTeamData(self, data, team1, team2):
        newTeam1 = {"Team": team1, "W/L": "0-0", "Round Robin": "0-0", "Dif": 0}
        newTeam2 = {"Team": team2, "W/L": "0-0", "Round Robin": "0-0", "Dif": 0}
        data["gamedata"]["teamdata"].append(newTeam1)
        data["gamedata"]["teamdata"].append(newTeam2)


class WindowManager(ScreenManager):
	pass

class MyApp(App):
    def build(self):
        kv = Builder.load_file('screens.kv')
        return kv

if __name__ == '__main__':
	MyApp().run()
