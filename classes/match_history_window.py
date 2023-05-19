import json

from kivy.uix.screenmanager import Screen


class MatchHistoryWindow(Screen):
    def history(self, i):
        with open('scores.json', 'r+') as file:
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