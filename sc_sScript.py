import importlib
import statistics

def main(name):
    i = importlib.import_module("bot vs bot."+name)

    NUM_RUNS = 1000

    wins1 = 0
    wins2 = 0

    totalPoints1 = 0
    totalPoints2 = 0

    points1 = []
    points2 = []

    totalMarginOfVictory1 = 0
    totalMarginOfVictory2 = 0

    marginOfVictories1 = []
    marginOfVictories2 = []

    totalSilver1 = 0
    totalSilver2 = 0

    silvers1 = []
    silvers2 = []

    totalTurnGold1 = 0
    totalTurnGold2 = 0

    turnGolds1 = []
    turnGolds2 = []

    totalGameLength = 0
    gameLengths = []

    for number in range(NUM_RUNS):
        game = i.SingleGame()
        game.simulateRun()

        # Different scoring method for workshop garden simulations
        if name.startswith("WkspGar"):
            p1Score = int((len(game.deck1) + len(game.discard1) + len(game.hand1)) / 10) * game.numGarden1 + game.numEstate1
        else:
            p1Score = game.numProvinces1 * 6 + game.numDuchies1 * 3 + game.numEstate1 - game.numCurse1
    
        totalPoints1 += p1Score
        points1.append(p1Score)

        p2Score = game.numProvinces2 * 6 + game.numDuchies2 * 3 + game.numEstate2 - game.numCurse2
        totalPoints2 += p2Score
        points2.append(p2Score)

        if(p1Score > p2Score):
            wins1 += 1
            totalMarginOfVictory1 += (p1Score - p2Score)
            marginOfVictories1.append(p1Score - p2Score)
        elif(p1Score < p2Score):
            wins2 += 1
            totalMarginOfVictory2 += (p2Score - p1Score)
            marginOfVictories2.append(p2Score - p1Score)

        totalSilver1 += game.numSilver1
        totalSilver2 += game.numSilver2

        silvers1.append(game.numSilver1)
        silvers2.append(game.numSilver2)

        totalTurnGold1 += game.turnGold1
        totalTurnGold2 += game.turnGold2
        
        turnGolds1.append(game.turnGold1)
        turnGolds2.append(game.turnGold2)

        totalGameLength += int((game.turnNumber / 2))
        gameLengths.append(int((game.turnNumber / 2)))

    text = []
    text.append("Player 1 Winrate: " + str(wins1 / NUM_RUNS))
    text.append("Player 2 Winrate: " + str(wins2 / NUM_RUNS))
    text.append("Player 1 Average Points: " + str(totalPoints1 / NUM_RUNS))
    text.append("Player 2 Average Points: " + str(totalPoints2 / NUM_RUNS))
    text.append("Player 1 Points Standard Deviation: " + str(statistics.stdev(points1)))
    text.append("Player 2 Points Standard Deviation: " + str(statistics.stdev(points2)))
    text.append("Player 1 Average Margin of Victory: " + str(totalMarginOfVictory1 / NUM_RUNS))
    text.append("Player 2 Average Margin of Victory: " + str(totalMarginOfVictory2 / NUM_RUNS))

    if wins1 > 0: 
        text.append("Player 1 Margin of Victory Standard Deviation: " + str(statistics.stdev(marginOfVictories1)))
    else:
        text.append("Player 1 Margin of Victory Standard Deviation: " + "N/A")

    if wins2 > 0:
        text.append("Player 2 Margin of Victory Standard Deviation: " + str(statistics.stdev(marginOfVictories2)))
    else:
        text.append("Player 2 Margin of Victory Standard Deviation: " + "N/A")

    text.append("Player 1 Average Silvers: " + str(totalSilver1 / NUM_RUNS))
    text.append("Player 2 Average Silvers: " + str(totalSilver2 / NUM_RUNS))
    text.append("Player 1 Silvers Standard Deviation: " + str(statistics.stdev(silvers1)))
    text.append("Player 2 Silvers Standard Deviation: " + str(statistics.stdev(silvers2)))
    text.append("Player 1 Average Turn for First Gold: " + str(totalTurnGold1 / NUM_RUNS))
    text.append("Player 2 Average Turn for First Gold: " + str(totalTurnGold2 /   NUM_RUNS))
    text.append("Player 1 Turn for First Gold Standard Deviation: " + str(statistics.stdev(turnGolds1)))
    text.append("Player 2 Turn for First Gold Standard Deviation: " + str(statistics.stdev(turnGolds2)))
    text.append("Average Game Length: " + str(totalGameLength / NUM_RUNS))
    text.append("Game Length Standard Deviation: " + str(statistics.stdev(gameLengths)))

    return text