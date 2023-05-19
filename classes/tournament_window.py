import json
import random

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen


class TournamentWindow(Screen):
    teamList = ListProperty(["[None]"])
    finishedTeamList = ListProperty(["[None]"])
    loserTeamList = ListProperty(["[None]"])
    loserFinishedTeamList = ListProperty(["[None]"])

    def getMatches(self):
        with open('currentTournament.json', 'r') as file:
            data = json.load(file)
            teamList = []
            for i in range(len(data["gamedata"]["currentmatches"])):
                temp = str(data["gamedata"]["currentmatches"][i]["Round"]) + " | " + \
                       data["gamedata"]["currentmatches"][i]["Text"]
                teamList.append(temp)
            self.teamList = teamList
            loserTeamList = []
            for i in range(len(data["gamedata"]["losermatches"])):
                temp = str(data["gamedata"]["losermatches"][i]["Round"]) + " | " + \
                       data["gamedata"]["losermatches"][i]["Text"]
                loserTeamList.append(temp)
            self.loserTeamList = loserTeamList

    def getFinishedMatches(self):
        with open('currentTournament.json', 'r') as file:
            data = json.load(file)
            finishedTeamList = []
            for i in range(len(data["gamedata"]["finishedmatches"])):
                temp = str(data["gamedata"]["finishedmatches"][i]["Round"]) + " | " + \
                       data["gamedata"]["finishedmatches"][i]["Text"] + " | " + str(
                    data["gamedata"]["finishedmatches"][i]["FinalScore"])
                finishedTeamList.append(temp)
            self.finishedTeamList = finishedTeamList
            loserFinishedTeamList = []
            for i in range(len(data["gamedata"]["finishedlosermatches"])):
                temp = str(data["gamedata"]["finishedlosermatches"][i]["Round"]) + " | " + \
                       data["gamedata"]["finishedlosermatches"][i]["Text"] + " | " + str(
                    data["gamedata"]["finishedlosermatches"][i]["FinalScore"])
                loserFinishedTeamList.append(temp)
            self.loserFinishedTeamList = loserFinishedTeamList

    def matchSelection(self, text, type):
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            rrRounds = data["gamedata"]["gamedata"][0]["rrRounds"]
            currentRound = data["gamedata"]["currentmatches"][0]["Round"]
            if currentRound <= rrRounds:
                type = 3
            text = text.split(" | ")
            print(text)
            if type == 1:
                for i in range(len(data["gamedata"]["currentmatches"])):
                    temp = data["gamedata"]["currentmatches"][i]
                    if text[1] in temp["Text"] and text[2] in temp["Text"]:
                        temp["FinalScore"] = self.ids.score1_input.text + '-' + self.ids.score2_input.text
                        file.truncate(0)
                        file.seek(0)
                        json.dump(data, file, indent=4)
            if type == 2:
                for i in range(len(data["gamedata"]["losermatches"])):
                    temp = data["gamedata"]["losermatches"][i]
                    if text[1] in temp["Text"]:
                        temp["FinalScore"] = self.ids.score1_input.text + '-' + self.ids.score2_input.text
                        file.truncate(0)
                        file.seek(0)
                        json.dump(data, file, indent=4)
            if type == 3:
                for i in range(len(data["gamedata"]["currentmatches"])):
                    temp = data["gamedata"]["currentmatches"][i]
                    if text[1] in temp["Text"]:
                        temp["FinalScore"] = self.ids.score1_input.text + '-' + self.ids.score2_input.text
                        file.truncate(0)
                        file.seek(0)
                        json.dump(data, file, indent=4)

    def nextRound(self):
        with open('currentTournament.json', 'r+') as file:
            data = json.load(file)
            rrRounds = data["gamedata"]["gamedata"][0]["rrRounds"]
            currentMatches = data["gamedata"]["currentmatches"]
            if len(currentMatches) > 1:
                currentRound = data["gamedata"]["currentmatches"][0]["Round"]
                round = currentRound + 1
            else:
                currentRound = data["gamedata"]["losermatches"][0]["Round"]
                round = currentRound + 1
            finals = data["gamedata"]["gamedata"][0]["finals"]
            losersFinals = data["gamedata"]["gamedata"][0]["losersfinals"]
            losers = []
            finalist = []
            loserMatches = data["gamedata"]["losermatches"]
            if len(currentMatches) in [3, 0] and currentRound > rrRounds:
                if finals is True:
                    TournamentWindow.determineWinner(self, data, finals)

                    # Adjust record and move games to finished for winners bracket
                    temp = data["gamedata"]["currentmatches"]
                    data["gamedata"]["currentmatches"] = []
                    data["gamedata"]["finishedmatches"] += temp

                if len(currentMatches) == 3 and finals is False:
                    # Find the winner of losers finals
                    TournamentWindow.determineWinner(self, data, finals)

                    # Adjust record and move games to finished for winners bracket
                    TournamentWindow.wlHandler(self, data, 1)
                    temp = data["gamedata"]["currentmatches"]
                    data["gamedata"]["currentmatches"] = []
                    data["gamedata"]["finishedmatches"] += temp

                if len(currentMatches) == 3 and data["gamedata"]["gamedata"][0]["WinnerBracketWinner"] == '':
                    # Find the winner of losers finals
                    TournamentWindow.determineWinner(self, data, finals)

                    # Adjust record and move games to finished for winners bracket
                    TournamentWindow.wlHandler(self, data, 1)
                    temp = data["gamedata"]["currentmatches"]
                    data["gamedata"]["currentmatches"] = []
                    data["gamedata"]["finishedmatches"] += temp

                if len(loserMatches) >= 2:
                    # Adjust record and move games to finished for losers bracket
                    TournamentWindow.wlHandler(self, data, 3)
                    temp1 = data["gamedata"]["losermatches"]
                    data["gamedata"]["losermatches"] = []
                    data["gamedata"]["finishedlosermatches"] += temp1

                    # Progress losers bracket
                    TournamentWindow.progressLosersBracket(self, data, losers, round)

                if len(loserMatches) == 1:
                    # Adjust record and move games to finished for losers bracket
                    TournamentWindow.wlHandler(self, data, 3)
                    temp1 = data["gamedata"]["losermatches"]
                    data["gamedata"]["losermatches"] = []
                    data["gamedata"]["finishedlosermatches"] += temp1

                    if losersFinals:
                        # Set mode to finals
                        data["gamedata"]["gamedata"][0]["finals"] = True

                        finalist.append(data["gamedata"]["gamedata"][0]["WinnerBracketWinner"])
                        print(finalist)

                        # Determine loser's finals winner
                        game = data["gamedata"]["finishedlosermatches"][-1]
                        if game["Round"] == round - 1:
                            score = game["FinalScore"].split('-')
                            team1 = game["Team1"]
                            team2 = game["Team2"]
                            if int(score[0]) != 0 and int(score[1]) != 0:
                                if int(score[0]) > int(score[1]):
                                    finalist.append(team1)
                                elif int(score[0]) < int(score[1]):
                                    finalist.append(team2)
                        print(finalist)

                        # Create bracket in json
                        for i in range(3):
                            game = i + 1
                            newMatch = {"Round": round, "Team1": finalist[0], "Team2": finalist[1], "FinalScore": "0-0",
                                        "Text": str(finalist[0]) + " vs " + str(finalist[1]) + " | Game: " + str(game)}
                            data["gamedata"]["currentmatches"].append(newMatch)

                    if not losersFinals:
                        # Set mode to losers Finals
                        data["gamedata"]["gamedata"][0]["losersfinals"] = True

                        # Create losers finals
                        wbl = {"name": data["gamedata"]["gamedata"][0]["WinnerBracketLoser"]}
                        losers.append(wbl)
                        TournamentWindow.progressLosersBracket(self, data, losers, round)

                # Update json
                file.truncate(0)
                file.seek(0)
                json.dump(data, file, indent=4)
            else:
                if currentRound <= rrRounds:
                    type = 0
                elif currentRound > rrRounds:
                    type = 1
                TournamentWindow.wlHandler(self, data, type)
                temp = data["gamedata"]["currentmatches"]
                data["gamedata"]["currentmatches"] = []
                data["gamedata"]["finishedmatches"] += temp
                if round > rrRounds + 2:
                    TournamentWindow.wlHandler(self, data, 3)
                    temp1 = data["gamedata"]["losermatches"]
                    data["gamedata"]["losermatches"] = []
                    data["gamedata"]["finishedlosermatches"] += temp1
                TournamentWindow.constructNextRound(self, round, data, temp)
                file.truncate(0)
                file.seek(0)
                json.dump(data, file, indent=4)

    def wlHandler(self, data, type):
        if type == 0:
            type = "Round Robin"
            for i in range(len(data["gamedata"]["currentmatches"])):
                score = data["gamedata"]["currentmatches"][i]["FinalScore"].split('-')
                team1Name = data["gamedata"]["currentmatches"][i]["Team1"]
                team2Name = data["gamedata"]["currentmatches"][i]["Team2"]
                dif = abs(int(score[0]) - int(score[1]))
                print(score)
                for x in range(len(data["gamedata"]["teamdata"])):
                    if data["gamedata"]["teamdata"][x]["Team"] == team1Name:
                        if int(score[0]) >= 21 & int(score[0]) > int(score[1]):
                            newWL = data["gamedata"]["teamdata"][x][type].split('-')
                            temp = int(newWL[0]) + 1
                            data["gamedata"]["teamdata"][x][type] = str(temp) + "-" + str(newWL[1])
                            data["gamedata"]["teamdata"][x]["Dif"] += dif
                            print(data["gamedata"]["teamdata"][x][type])
                        elif int(score[1]) >= 21 & int(score[1]) > int(score[0]):
                            newWL = data["gamedata"]["teamdata"][x][type].split('-')
                            temp = int(newWL[1]) + 1
                            data["gamedata"]["teamdata"][x][type] = str(newWL[0]) + "-" + str(temp)
                            print(data["gamedata"]["teamdata"][x][type])
                            data["gamedata"]["teamdata"][x]["Dif"] -= dif
                    elif data["gamedata"]["teamdata"][x]["Team"] == team2Name:
                        if int(score[0]) >= 21 & int(score[0]) > int(score[1]):
                            newWL = data["gamedata"]["teamdata"][x][type].split('-')
                            temp = int(newWL[1]) + 1
                            data["gamedata"]["teamdata"][x][type] = str(newWL[0]) + "-" + str(temp)
                            data["gamedata"]["teamdata"][x]["Dif"] -= dif
                            print(data["gamedata"]["teamdata"][x][type])
                        elif int(score[1]) >= 21 & int(score[1]) > int(score[0]):
                            newWL = data["gamedata"]["teamdata"][x][type].split('-')
                            temp = int(newWL[0]) + 1
                            data["gamedata"]["teamdata"][x][type] = str(temp) + "-" + str(newWL[1])
                            print(data["gamedata"]["teamdata"][x][type])
                            data["gamedata"]["teamdata"][x]["Dif"] += dif
        elif type == 1:
            type = "W/L"
            for i in range(len(data["gamedata"]["currentmatches"])):
                game = data["gamedata"]["currentmatches"][i]
                match = game["Text"].split("|")
                match = match[1]
                match = game["Text"].split(": ")
                match = match[1]
                score = game["FinalScore"].split('-')
                team1Name = data["gamedata"]["currentmatches"][i]["Team1"]
                team2Name = data["gamedata"]["currentmatches"][i]["Team2"]
                dif = abs(int(score[0]) - int(score[1]))
                print(score)
                print(match)
                if int(match) == 3:
                    if int(score[0]) != 0 and int(score[1]) != 0:
                        for x in range(len(data["gamedata"]["teamdata"])):
                            if data["gamedata"]["teamdata"][x]["Team"] == team1Name:
                                if int(score[0]) >= 21 and int(score[0]) > int(score[1]):
                                    newWL = data["gamedata"]["teamdata"][x][type].split('-')
                                    temp = int(newWL[0]) + 1
                                    data["gamedata"]["teamdata"][x][type] = str(temp) + "-" + str(newWL[1])
                                    data["gamedata"]["teamdata"][x]["Dif"] += dif
                                    print(data["gamedata"]["teamdata"][x][type])
                                elif int(score[1]) >= 21 and int(score[1]) > int(score[0]):
                                    newWL = data["gamedata"]["teamdata"][x][type].split('-')
                                    temp = int(newWL[1]) + 1
                                    data["gamedata"]["teamdata"][x][type] = str(newWL[0]) + "-" + str(temp)
                                    print(data["gamedata"]["teamdata"][x][type])
                                    data["gamedata"]["teamdata"][x]["Dif"] -= dif
                            elif data["gamedata"]["teamdata"][x]["Team"] == team2Name:
                                if int(score[0]) >= 21 and int(score[0]) > int(score[1]):
                                    newWL = data["gamedata"]["teamdata"][x][type].split('-')
                                    temp = int(newWL[1]) + 1
                                    data["gamedata"]["teamdata"][x][type] = str(newWL[0]) + "-" + str(temp)
                                    data["gamedata"]["teamdata"][x]["Dif"] -= dif
                                    print(data["gamedata"]["teamdata"][x][type])
                                elif int(score[1]) >= 21 and int(score[1]) > int(score[0]):
                                    newWL = data["gamedata"]["teamdata"][x][type].split('-')
                                    temp = int(newWL[0]) + 1
                                    data["gamedata"]["teamdata"][x][type] = str(temp) + "-" + str(newWL[1])
                                    print(data["gamedata"]["teamdata"][x][type])
                                    data["gamedata"]["teamdata"][x]["Dif"] += dif
                    elif int(score[0]) == 0 and int(score[1]) == 0:
                        game = data["gamedata"]["currentmatches"][i - 1]
                        match = game["Text"].split("|")
                        match = match[1]
                        match = game["Text"].split(": ")
                        match = match[1]
                        score = game["FinalScore"].split('-')
                        team1 = game["Team1"]
                        team2 = game["Team2"]
                        print(score)
                        print(match)
                        if int(match) == 2 and int(score[0]) != 0 or int(score[1]) != 0:
                            for x in range(len(data["gamedata"]["teamdata"])):
                                if data["gamedata"]["teamdata"][x]["Team"] == team1:
                                    if int(score[0]) >= 21 and int(score[0]) > int(score[1]):
                                        print("AB")
                                        newWL = data["gamedata"]["teamdata"][x][type].split('-')
                                        temp = int(newWL[0]) + 1
                                        data["gamedata"]["teamdata"][x][type] = str(temp) + "-" + str(newWL[1])
                                        data["gamedata"]["teamdata"][x]["Dif"] += dif
                                        print(data["gamedata"]["teamdata"][x][type])
                                    elif int(score[1]) >= 21 and int(score[1]) > int(score[0]):
                                        print("CD")
                                        newWL = data["gamedata"]["teamdata"][x][type].split('-')
                                        temp = int(newWL[1]) + 1
                                        data["gamedata"]["teamdata"][x][type] = str(newWL[0]) + "-" + str(temp)
                                        print(data["gamedata"]["teamdata"][x][type])
                                        data["gamedata"]["teamdata"][x]["Dif"] -= dif
                                elif data["gamedata"]["teamdata"][x]["Team"] == team2:
                                    if int(score[0]) >= 21 and int(score[0]) > int(score[1]):
                                        newWL = data["gamedata"]["teamdata"][x][type].split('-')
                                        print("EF")
                                        temp = int(newWL[1]) + 1
                                        data["gamedata"]["teamdata"][x][type] = str(newWL[0]) + "-" + str(temp)
                                        data["gamedata"]["teamdata"][x]["Dif"] -= dif
                                        print(data["gamedata"]["teamdata"][x][type])
                                    elif int(score[1]) >= 21 and int(score[1]) > int(score[0]):
                                        newWL = data["gamedata"]["teamdata"][x][type].split('-')
                                        temp = int(newWL[0]) + 1
                                        print("GH")
                                        data["gamedata"]["teamdata"][x][type] = str(temp) + "-" + str(newWL[1])
                                        print(data["gamedata"]["teamdata"][x][type])
                                        data["gamedata"]["teamdata"][x]["Dif"] += dif
        if type == 3:
            type = "W/L"
            for i in range(len(data["gamedata"]["losermatches"])):
                score = data["gamedata"]["losermatches"][i]["FinalScore"].split('-')
                team1Name = data["gamedata"]["losermatches"][i]["Team1"]
                team2Name = data["gamedata"]["losermatches"][i]["Team2"]
                dif = abs(int(score[0]) - int(score[1]))
                print(score)
                for x in range(len(data["gamedata"]["teamdata"])):
                    if data["gamedata"]["teamdata"][x]["Team"] == team1Name:
                        if int(score[0]) >= 21 & int(score[0]) > int(score[1]):
                            newWL = data["gamedata"]["teamdata"][x][type].split('-')
                            temp = int(newWL[0]) + 1
                            data["gamedata"]["teamdata"][x][type] = str(temp) + "-" + str(newWL[1])
                            data["gamedata"]["teamdata"][x]["Dif"] += dif
                            print(data["gamedata"]["teamdata"][x][type])
                        elif int(score[1]) >= 21 & int(score[1]) > int(score[0]):
                            newWL = data["gamedata"]["teamdata"][x][type].split('-')
                            temp = int(newWL[1]) + 1
                            data["gamedata"]["teamdata"][x][type] = str(newWL[0]) + "-" + str(temp)
                            print(data["gamedata"]["teamdata"][x][type])
                            data["gamedata"]["teamdata"][x]["Dif"] -= dif
                    elif data["gamedata"]["teamdata"][x]["Team"] == team2Name:
                        if int(score[0]) >= 21 & int(score[0]) > int(score[1]):
                            newWL = data["gamedata"]["teamdata"][x][type].split('-')
                            temp = int(newWL[1]) + 1
                            data["gamedata"]["teamdata"][x][type] = str(newWL[0]) + "-" + str(temp)
                            data["gamedata"]["teamdata"][x]["Dif"] -= dif
                            print(data["gamedata"]["teamdata"][x][type])
                        elif int(score[1]) >= 21 & int(score[1]) > int(score[0]):
                            newWL = data["gamedata"]["teamdata"][x][type].split('-')
                            temp = int(newWL[0]) + 1
                            data["gamedata"]["teamdata"][x][type] = str(temp) + "-" + str(newWL[1])
                            print(data["gamedata"]["teamdata"][x][type])
                            data["gamedata"]["teamdata"][x]["Dif"] += dif

    def constructNextRound(self, round, data, temp):
        teams = data["gamedata"]["teams"]
        teamCount = len(teams)
        gameCount = len(temp)
        unmatched = list(range(0, teamCount))
        match = 0
        rounds = data["gamedata"]["gamedata"][0]["rrRounds"]
        if round <= rounds:
            gamesAmount = teamCount / 2
            while match < gamesAmount:
                random.shuffle(unmatched)
                selTeam1 = unmatched[0]
                selTeam2 = unmatched[1]
                team1 = data["gamedata"]["teams"][selTeam1]
                team2 = data["gamedata"]["teams"][selTeam2]
                newMatch = {"Round": round, "Team1": team1, "Team2": team2, "FinalScore": "0-0",
                            "Text": team1 + " vs " + team2}
                data["gamedata"]["currentmatches"].append(newMatch)
                match += 1
                unmatched.remove(selTeam1)
                unmatched.remove(selTeam2)
        elif round == rounds + 1:
            TournamentWindow.seedCalculation(self, data)
            TournamentWindow.bracketBuilder(self, data, teams, teamCount, round)
        elif round > rounds + 1 and gameCount != 1:
            TournamentWindow.progressBracket(self, data, teamCount, round)

    def seedCalculation(self, data):
        names = []
        rrws = []
        difs = []
        for i in range(len(data["gamedata"]["teamdata"])):
            names.append(data["gamedata"]["teamdata"][i]["Team"])
            temp = data["gamedata"]["teamdata"][i]["Round Robin"].split('-')
            rrws.append(temp[0])
            difs.append(data["gamedata"]["teamdata"][i]["Dif"])
        unSeeded = len(names)
        seed = 1
        while unSeeded > 0:
            seedName = ''
            for i in range(len(rrws)):
                if difs[i] == max(difs):
                    seedName = names[i]
            for x in range(len(data["gamedata"]["teamdata"])):
                if data["gamedata"]["teamdata"][x]["Team"] == seedName:
                    data["gamedata"]["teamdata"][x]["Seed"] = seed
                    seed += 1
                    unSeeded -= 1
                    pos = names.index(seedName)
                    difs.remove(difs[pos])
                    rrws.remove(rrws[pos])
                    names.remove(seedName)

    def bracketBuilder(self, data, teams, seeds, round):
        unmatched = []
        seed = 1
        while seed <= seeds:
            for i in range(len(data["gamedata"]["teamdata"])):
                if data["gamedata"]["teamdata"][i]["Seed"] == seed:
                    unmatched.append(data["gamedata"]["teamdata"][i]["Team"])
                    seed += 1
        while len(unmatched) > 0:
            selTeam1 = unmatched[0]
            selTeam2 = unmatched[-1]
            for i in range(3):
                game = i + 1
                newMatch = {"Round": round, "Team1": selTeam1, "Team2": selTeam2, "FinalScore": "0-0",
                            "Text": selTeam1 + " vs " + selTeam2 + " | Game: " + str(game)}
                data["gamedata"]["currentmatches"].append(newMatch)
            unmatched.remove(selTeam1)
            unmatched.remove(selTeam2)

    def progressBracket(self, data, teamCount, round):
        spot = 1
        spots = []
        losers = []
        for i in range(len(data["gamedata"]["finishedmatches"])):
            game = data["gamedata"]["finishedmatches"][i]
            if game["Round"] == round - 1:
                match = game["Text"].split("|")
                match = match[1]
                match = game["Text"].split(": ")
                match = match[1]
                score = game["FinalScore"].split('-')
                team1 = game["Team1"]
                team2 = game["Team2"]
                if int(match) == 3:
                    if int(score[0]) != 0 and int(score[1]) != 0:
                        if int(score[0]) > int(score[1]):
                            winnerName = {"name": team1}
                            loserName = {"name": team2}
                            spots.append(winnerName)
                            losers.append(loserName)
                        elif int(score[0]) < int(score[1]):
                            winnerName = {"name": team2}
                            loserName = {"name": team1}
                            spots.append(winnerName)
                            losers.append(loserName)
                        spot += 1
                    elif int(score[0]) == 0 and int(score[1]) == 0:
                        tempGame = data["gamedata"]["finishedmatches"][i - 1]
                        match = tempGame["Text"].split("|")
                        match = match[1]
                        match = game["Text"].split(": ")
                        match = match[1]
                        score = tempGame["FinalScore"].split('-')
                        team1 = tempGame["Team1"]
                        team2 = tempGame["Team2"]
                        if int(match) == 2 and int(score[0]) != 0 or int(score[1]) != 0:
                            if int(score[0]) > int(score[1]):
                                winnerName = {"name": team1}
                                loserName = {"name": team2}
                                spots.append(winnerName)
                                losers.append(loserName)
                            elif int(score[0]) < int(score[1]):
                                winnerName = {"name": team2}
                                loserName = {"name": team1}
                                spots.append(winnerName)
                                losers.append(loserName)
                            spot += 1
        num = len(spots)
        num2 = 0
        num3 = num - 1
        while num > 0:
            team1 = spots[num2]["name"]
            team2 = spots[num3]["name"]
            print(team1, team2)
            for i in range(3):
                game = i + 1
                newMatch = {"Round": round, "Team1": team1, "Team2": team2, "FinalScore": "0-0",
                            "Text": team1 + " vs " + team2 + " | Game: " + str(game)}
                data["gamedata"]["currentmatches"].append(newMatch)
            # spots.remove(team1)
            # spots.remove(team2)
            num -= 2
            num2 += 1
            num3 -= 1
        TournamentWindow.progressLosersBracket(self, data, losers, round)

    def progressLosersBracket(self, data, losers, round):
        losersData = data["gamedata"]["losermatches"]
        spot = 1
        spots = []
        rrRounds = data["gamedata"]["gamedata"][0]["rrRounds"]
        if round == rrRounds + 2:
            num = len(losers)
            num2 = 0
            num3 = num - 1
            while num > 0:
                team1 = losers[num2]["name"]
                team2 = losers[num3]["name"]
                print(team1, team2)
                newMatch = {"Round": round, "Team1": team1, "Team2": team2, "FinalScore": "0-0",
                            "Text": team1 + " vs " + team2 + " | Game: L1"}
                losersData.append(newMatch)
                num -= 2
                num2 += 1
                num3 -= 1
        if round > rrRounds + 2:
            for i in range(len(data["gamedata"]["finishedlosermatches"])):
                game = data["gamedata"]["finishedlosermatches"][i]
                if game["Round"] == round - 1:
                    score = game["FinalScore"].split('-')
                    team1 = game["Team1"]
                    team2 = game["Team2"]
                    if int(score[0]) != 0 and int(score[1]) != 0:
                        if int(score[0]) > int(score[1]):
                            winnerName = {"name": team1}
                            losers.append(winnerName)
                        elif int(score[0]) < int(score[1]):
                            winnerName = {"name": team2}
                            losers.append(winnerName)
            print(losers)
            num = len(losers)
            num2 = 0
            num3 = num - 1
            while num > 0:
                team1 = losers[num2]["name"]
                team2 = losers[num3]["name"]
                print(team1, team2)
                newMatch = {"Round": round, "Team1": team1, "Team2": team2, "FinalScore": "0-0",
                            "Text": team1 + " vs " + team2 + " | Game: L" + str(round)}
                losersData.append(newMatch)
                num -= 2
                num2 += 1
                num3 -= 1

    def determineWinner(self, data, finals):
        for i in range(len(data["gamedata"]["currentmatches"])):
            game = data["gamedata"]["currentmatches"][i]
            match = game["Text"].split("|")
            match = match[1]
            match = game["Text"].split(": ")
            match = match[1]
            score = game["FinalScore"].split('-')
            team1 = game["Team1"]
            team2 = game["Team2"]
            if finals is True:
                first, second = '', ''
                if int(match) == 3:
                    if int(score[0]) != 0 and int(score[1]) != 0:
                        if int(score[0]) > int(score[1]):
                            first = game["Team1"]
                            second = game["Team2"]
                        elif int(score[0]) < int(score[1]):
                            first = game["Team2"]
                            second = game["Team1"]
                        f = {"1st": first, "2nd": second}
                        print(f)
                        data["gamedata"]["finish"].append(f)
                    elif int(score[0]) == 0 and int(score[1]) == 0:
                        tempGame = data["gamedata"]["currentmatches"][i - 1]
                        match = tempGame["Text"].split("|")
                        match = match[1]
                        match = game["Text"].split(": ")
                        match = match[1]
                        score = tempGame["FinalScore"].split('-')
                        team1 = tempGame["Team1"]
                        team2 = tempGame["Team2"]
                        if int(match) == 2 and int(score[0]) != 0 or int(score[1]) != 0:
                            if int(score[0]) > int(score[1]):
                                first = game["Team1"]
                                second = game["Team2"]
                            elif int(score[0]) < int(score[1]):
                                first = game["Team2"]
                                second = game["Team1"]
                            f = {"1st": first, "2nd": second}
                            print(f)
                            data["gamedata"]["finish"].append(f)
            else:
                winnerBracketWinner = data["gamedata"]["gamedata"][0]["WinnerBracketWinner"]
                WinnerBracketLoser = data["gamedata"]["gamedata"][0]["WinnerBracketLoser"]
                if int(match) == 3:
                    if int(score[0]) != 0 and int(score[1]) != 0:
                        if int(score[0]) > int(score[1]):
                            data["gamedata"]["gamedata"][0]["WinnerBracketWinner"] = game["Team1"]
                            data["gamedata"]["gamedata"][0]["WinnerBracketLoser"] = game["Team2"]
                        elif int(score[0]) < int(score[1]):
                            data["gamedata"]["gamedata"][0]["WinnerBracketWinner"] = game["Team2"]
                            data["gamedata"]["gamedata"][0]["WinnerBracketLoser"] = game["Team1"]
                        f = {"WBW": winnerBracketWinner, "WBL": WinnerBracketLoser}
                        print(f)
                    elif int(score[0]) == 0 and int(score[1]) == 0:
                        tempGame = data["gamedata"]["currentmatches"][i - 1]
                        match = tempGame["Text"].split("|")
                        match = match[1]
                        match = game["Text"].split(": ")
                        match = match[1]
                        score = tempGame["FinalScore"].split('-')
                        team1 = tempGame["Team1"]
                        team2 = tempGame["Team2"]
                        if int(match) == 2 and int(score[0]) != 0 or int(score[1]) != 0:
                            if int(score[0]) > int(score[1]):
                                data["gamedata"]["gamedata"][0]["WinnerBracketWinner"] = game["Team1"]
                                data["gamedata"]["gamedata"][0]["WinnerBracketLoser"] = game["Team2"]
                            elif int(score[0]) < int(score[1]):
                                data["gamedata"]["gamedata"][0]["WinnerBracketWinner"] = game["Team2"]
                                data["gamedata"]["gamedata"][0]["WinnerBracketLoser"] = game["Team1"]
                            f = {"WBW": winnerBracketWinner, "WBL": WinnerBracketLoser}
                            print(f)
