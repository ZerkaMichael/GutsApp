import json
import random

from kivy.uix.screenmanager import Screen


class AdminWindow(Screen):
    def submitTeams(self):
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            newTeam = self.ids.team_input.text
            data["gamedata"]["teams"].append(newTeam)
            file.seek(0)
            json.dump(data, file, indent=4)

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
                json.dump(data, file, indent=4)

    def startTournament(self):
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            teams = data["gamedata"]["teams"]
            teamCount = len(teams)
            unmatched = list(range(0, teamCount))
            match = 0
            data["gamedata"]["gamedata"][0]["rrRounds"] = int(self.ids.roundrobin_rounds.text)
            if (teamCount % 2) == 0:
                gamesAmount = teamCount / 2
                while match < gamesAmount:
                    random.shuffle(unmatched)
                    selTeam1 = unmatched[0]
                    selTeam2 = unmatched[1]
                    team1 = data["gamedata"]["teams"][selTeam1]
                    team2 = data["gamedata"]["teams"][selTeam2]
                    AdminWindow.constructTeamData(self, data, team1, team2)
                    newMatch = {"Round": 1, "Team1": team1, "Team2": team2, "FinalScore": "0-0",
                                "Text": team1 + " vs " + team2}
                    data["gamedata"]["currentmatches"].append(newMatch)
                    match += 1
                    unmatched.remove(selTeam1)
                    unmatched.remove(selTeam2)
                file.truncate(0)
                file.seek(0)
                json.dump(data, file, indent=4)

    def constructTeamData(self, data, team1, team2):
        newTeam1 = {"Team": team1, "W/L": "0-0", "Round Robin": "0-0", "Dif": 0, "Seed": 0}
        newTeam2 = {"Team": team2, "W/L": "0-0", "Round Robin": "0-0", "Dif": 0, "Seed": 0}
        data["gamedata"]["teamdata"].append(newTeam1)
        data["gamedata"]["teamdata"].append(newTeam2)
