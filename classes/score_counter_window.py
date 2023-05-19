from kivy.uix.screenmanager import Screen


class ScoreCounterWindow(Screen):
    def submit(self):
        game = {'Team1': self.ids.team1_name.text, 'Team2': self.ids.team2_name.text,
                'Score1': self.ids.score1_input.text, 'Score2': self.ids.score2_input.text}
        with open('../scores.json', 'r+') as file:
            data = json.load(file)
            data["games"].append(game)
            file.seek(0)
            json.dump(data, file, indent=4)

    def addScore(self, team):
        if team == 1:
            score = int(self.ids.score1_input.text)
            score += 1
            self.ids.score1_input.text = str(score)
        else:
            score = int(self.ids.score2_input.text)
            score += 1
            self.ids.score2_input.text = str(score)

    def subScore(self, team):
        if team == 1:
            score = int(self.ids.score1_input.text)
            score -= 1
            self.ids.score1_input.text = str(score)
        else:
            score = int(self.ids.score2_input.text)
            score -= 1
            self.ids.score2_input.text = str(score)
