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
    def getMatches(self):
        with open('currentTournament.json', 'r') as file:
            data = json.load(file)
            teamList = []
            for i in range(len(data["gamedata"]["currentmatches"])):
                temp = data["gamedata"]["currentmatches"][i]["Text"]
                teamList.append(temp)
            self.teamList = teamList

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
            if (teamCount % 2) == 0:
                i = 1
                gamesAmount = teamCount/2
                while match < gamesAmount:
                    random.shuffle(unmatched)
                    selTeam1 = unmatched[0]
                    selTeam2 = unmatched[1]
                    team1 = data["gamedata"]["teams"][selTeam1]
                    team2 = data["gamedata"]["teams"][selTeam2]
                    #print("Pair {}: {} and {}".format(i, team1, team2))
                    newMatch = {"Team1": team1, "Team2": team2, "FinalScore": "0-0", "Text": team1+" vs "+team2}
                    data["gamedata"]["currentmatches"].append(newMatch)
                    i += 1
                    match += 1
                    unmatched.remove(selTeam1)
                    unmatched.remove(selTeam2)
                file.truncate(0)
                file.seek(0)
                json.dump(data, file, indent = 4)

class WindowManager(ScreenManager):
	pass

class MyApp(App):
    def build(self):
        kv = Builder.load_file('screens.kv')
        return kv

if __name__ == '__main__':
	MyApp().run()
