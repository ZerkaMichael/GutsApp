import json
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from os import path

filename = 'C:/Users/Michael/Documents/Python/ScoreApp/scores.json'

class HomeWindow(Screen):
    pass

class ScoreCounterWindow(Screen):
    def submit(self):
        t1 = self.ids.team1_name.text
        t2 = self.ids.team2_name.text
        s1 = self.ids.score1_input.text
        s2 = self.ids.score2_input.text
        game = {'Team1': t1, 'Team2': t2, 'Score1': s1, 'Score2': s2}
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
                return str(info)
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
	pass

class WindowManager(ScreenManager):
	pass

class MyApp(App):
    def build(self):
        kv = Builder.load_file('screens.kv')
        return kv

if __name__ == '__main__':
	MyApp().run()
