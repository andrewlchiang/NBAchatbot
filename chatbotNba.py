"""
The readme has some sample conversations
"""
from emora_stdm import KnowledgeBase, DialogueFlow, Macro
from enum import Enum, auto
import requests
from sportsreference.nba.schedule import Schedule
from sportsreference.nba.roster import Player
import json
from random import randrange
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--debug", help="enable debugging", type = bool, default = False)
args = parser.parse_args()

class State(Enum):
  #states for trade conversation
    START = auto()
    TURN0 = auto()
    TURNTRADE0S = auto()
    TURNTRADE0AS = auto()
    TURNTRADE0BS = auto()
    TURNTRADE0U = auto()
    TURNTRADE0AU = auto()
    TURN0DK1S = auto()
    TURN0DK1U = auto()
    TURNTRADE0ERR = auto()
    TURNTRADE1S = auto()
    TURNTRADE1S_GEN = auto()
    TURNTRADE1S1 = auto()
    TURNTRADE1S3 = auto()
    TURNTRADE1U = auto()
    TURNTRADE1ERR = auto()
    TURNTRADE1U_ERR = auto()
    TURNTRADE1AS = auto()
    TURNTRADE1BS = auto()
    TURNTRADE1BU = auto()
    TURNTRADE2U = auto()
    TURNTRADE2AS = auto()
    TURNTRADE2S = auto()
    TURNTRADE2AU = auto()
    TURNTRADE2DK1S = auto()
    TURNTRADE2ERR = auto()
    TURNTRADE3S1 = auto()
    TURNTRADE3AS = auto()
    TURNTRADE3BS = auto()
    TURNTRADE3CS = auto()
    TURNTRADE3S2 = auto()
    TURNTRADE3U = auto()
    TURNTRADE3DK1S = auto()
    TURNTRADE3ERR = auto()
    TURNTRADE4S = auto()
    TURNTRADE4S1 = auto()
    TURNTRADE4U = auto()
    TURNTRADE4DK1S = auto()
    TURNTRADE4ERR = auto()
    TURNTRADE5U = auto()
    TURNTRADE5S = auto()
    TURNTRADE5AS = auto()
    TURNTRADE5BS = auto()
    TURNTRADE5CS = auto()
    TURNTRADE3UERR = auto()
    TURNTRADE5U_ERR = auto()
    TURNTRADE6AS = auto()
    TURNTRADE6BS = auto()

    
    #states for playoff conversation
    TURNPF1S = auto()
    TURNPF1U = auto()
    TURNPF1ERR = auto()
    TURNPF1ERRU = auto()
    TURNPF1ERR1S = auto()
    TURNPF2AS = auto()
    TURNPF2AU = auto()
    TURNPF2A_DK = auto()
    TURNPF2BS = auto()
    TURNPF2BS1_OP_GOOD1 = auto()
    TURNPF2BS1_OP_GOOD2 = auto()
    TURNPF2BS1_OP_GOOD3 = auto()
    TURNPF2BS1_OP_GOOD4 = auto()
    TURNPF2BS1_OP_GOOD5 = auto()
    TURNPF2BS1_OP_GOOD6 = auto()
    TURNPF2BS1_OP_GOOD7 = auto()
    TURNPF2BS2 = auto()
    TURNPF2BU = auto()
    TURNPF2BU1 = auto()
    TURNPF2CS = auto()
    TURNPF2BDK = auto()
    TURNPF2ERR = auto()
    TURNPF2AERR = auto()
    TURNPF2BU_ERR1 = auto()
    TURNPF2BU_ERR2= auto()
    TURNPF2BU_ERR3 = auto()
    TURNPF3AS = auto()
    TURNPF3AERR = auto()
    TURNPF3BS = auto()
    TURNPF3CS = auto()
    TURNPF3DS = auto()
    TURNPF3DU = auto()
    TURNPF3ES = auto()
    TURNPF3FS = auto()
    TURNPF3AU = auto()
    TURNPF3U = auto()
    TURNPF3U_ERR = auto()
    TURNPF4S_OP_GOOD1 = auto()
    TURNPF4S_OP_GOOD2 = auto()
    TURNPF4S_OP_GOOD3 = auto()
    TURNPF4S_OP_GOOD4 = auto()
    TURNPF4S_OP_GOOD5 = auto()
    TURNPF4S_OP_GOOD6 = auto()
    TURNPF4S_OP_GOOD7 = auto()
    TURNPF4S_OP_BAD1 = auto()
    TURNPF4S_OP_BAD2 = auto()
    TURNPF4S_OP_BAD3 = auto()
    TURNPF4S_OP_BAD4 = auto()
    TURNPF4S_OP_BAD5 = auto()
    TURNPF4S_OP_BAD6 = auto()
    TURNPF4S_OP_BAD7 = auto()
    TURNPF4S_OP_GEN = auto()
    TURNPF5S = auto()
    TURNPF5U = auto()
    TURNPF5AS = auto()
    TURNPF5U_ERR = auto()
    TURNPF6S = auto()
    TURNPF6S_OP_GOOD1 = auto()
    TURNPF6S_OP_GOOD2 = auto()
    TURNPF6S_OP_GOOD3 = auto()
    TURNPF6S_OP_GOOD4 = auto()
    TURNPF6S_OP_GOOD5 = auto()
    TURNPF6S_OP_GOOD6 = auto()
    TURNPF6S_OP_GOOD7 = auto()
    TURNPF6S_OP_BAD1 = auto()
    TURNPF6S_OP_BAD2 = auto()
    TURNPF6S_OP_BAD3 = auto()
    TURNPF6S_OP_BAD4 = auto()
    TURNPF6S_OP_BAD5 = auto()
    TURNPF6S_OP_BAD6 = auto()
    TURNPF6S_OP_BAD7 = auto()
    TURNPF6S_OP_GEN = auto()
    TURNPF6U = auto()
    TURNPF7S = auto()
    TURNPF7S1 = auto()
    TURNPF7BS = auto()
    TURNPF7AS = auto()
    TURNPF8AS = auto()
    TURNPF8BS = auto()
    TURNPF8CS = auto()
    TURNPF8DS = auto()
    TURNPF8ES = auto()
    TURNPF8FS = auto()
    TURNPF8GS = auto()
    TURNPF8HS = auto()
    TURNNOPF1S = auto()
    TURNNOPF1U = auto()
    TURNNOPF1ERR = auto()
    TURNNOPF2S = auto()
    END = auto()
    EARLYEND = auto()


# ONTOLOGY IS LOADED FROM teams.json
ontology = {
    "ontology": {

        }
}

class news(Macro):
    def run (self, ngrams, vars, args):
        endpoint = "Lakers sign guard dion waiters".replace(" ", "%20")
        endpoint = "http://newsapi.org/v2/everything?q="+endpoint+"&apiKey=d50b19bb1c7445b588bb694ecc2a119f"
        news = requests.get(endpoint)
        formatted_news = news.json()
        formatted_news = formatted_news['articles']

        ## THINGS TO RETURN #####
        title = formatted_news[0]['title']
        description = formatted_news[0]['description']
        #########################

        return "{}".format(description)

class newsPlayer(Macro):
    def run (self, ngrams, vars, args):
        endpoint = vars['player'].replace(" ", "%20")
        endpoint = "http://newsapi.org/v2/everything?q="+endpoint+"&apiKey=d50b19bb1c7445b588bb694ecc2a119f"
        news = requests.get(endpoint)
        formatted_news = news.json()
        formatted_news = formatted_news['articles']

        ## THINGS TO RETURN #####
        title = formatted_news[0]['title']
        description = formatted_news[0]['description']
        #########################

        return "I found this recent news headline. {}. It says that {}".format(title, description)

class newsTeam(Macro):
    def run (self, ngrams, vars, args):

        endpoint = vars['favoriteTeam'].replace(" ", "%20") +"%20basketball"
        endpoint = "http://newsapi.org/v2/everything?q="+endpoint+"&apiKey=d50b19bb1c7445b588bb694ecc2a119f"
        news = requests.get(endpoint)
        formatted_news = news.json()
        formatted_news = formatted_news['articles']

        ## THINGS TO RETURN #####
        title = formatted_news[0]['title']
        description = formatted_news[0]['description']
        #########################
        
        #is this line useful?
        result = ""

        return "I found this recent news headline about {}. {}. It says {}".format(vars['favoriteTeam'], title, description)

class teamStats(Macro):
    def run (self, ngrams, vars, args):
        response = requests.get("https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json")
        test = response.json()
        trades = [x for x in test['NBA_Player_Movement']['rows'] if x['Transaction_Type'] == 'Trade']
        trade = trades[0]['TRANSACTION_DESCRIPTION']
        receivingTeam = trade.split(' received')[0]
        givingTeam = trade.split('from ')[1]
        givingTeam = givingTeam[:-1]
        player = trade.split('received ')[1]
        player = player.split('from')[0]

        playerList = player.split(' ')
        role = playerList[0]
        playerList.pop(0)
        player = ' '.join(playerList)
        #Assume input is team name, all lowercase

        if vars['receivingTeam'] == "Atlanta Hawks" or vars['receivingTeam'] == "Atlanta" or  vars['receivingTeam'] == "Hawks":
            team = 'ATL'
        elif vars['receivingTeam'] == "Boston Celtics" or vars['receivingTeam'] == "Boston" or vars['receivingTeam'] == "Celtics":
            team = 'BOS'
        elif vars['receivingTeam'] == "Brooklyn Nets" or vars['receivingTeam'] == "Brooklyn" or vars['receivingTeam'] == "Nets":
            team = 'BKN'
        elif vars['receivingTeam'] == "Charlotte Hornets" or vars['receivingTeam'] == "Charlotte" or vars['receivingTeam'] == "Hornets":
            team = 'CHA'
        elif vars['receivingTeam'] == "Chicago Bulls" or vars['receivingTeam'] == "Chicago" or vars['receivingTeam'] == "Bulls":
            team = 'CHI'
        elif vars['receivingTeam'] == "Cleveland Cavaliers" or vars['receivingTeam'] == "Cleveland" or vars['receivingTeam'] == "Cavaliers":
            team = 'CLE'
        elif vars['receivingTeam'] == "Dallas Mavericks" or vars['receivingTeam'] == "Dallas" or vars['receivingTeam'] == "Mavericks":
            team = 'DAL'
        elif vars['receivingTeam'] == "Denver Nuggets" or vars['receivingTeam'] == "Denver" or vars['receivingTeam'] == "Nuggets":
            team = 'DEN'
        elif vars['receivingTeam'] == "Detroit Pistons" or vars['receivingTeam'] == "Detroit" or vars['receivingTeam'] == "Pistons":
            team = 'DET'
        elif vars['receivingTeam'] == "Golden State Warriors" or vars['receivingTeam'] == "GSW" or vars['receivingTeam'] == "Warriors":
            team = 'GSW'
        elif vars['receivingTeam'] == "Houston Rockets" or vars['receivingTeam'] == "Houston" or vars['receivingTeam'] == "Rockets":
            team = 'HOU'
        elif vars['receivingTeam'] == "Indiana Pacers" or vars['receivingTeam'] == "Indiana" or vars['receivingTeam'] == "Pacers":
            team = 'IND'
        elif vars['receivingTeam'] == "LA Clippers" or vars['receivingTeam'] == "Clippers":
            team = 'LAC'
        elif vars['receivingTeam'] == "Los Angeles Lakers" or vars['receivingTeam'] == "Lakers":
            team = 'LAL'
        elif vars['receivingTeam'] == "Memphis Grizzlies" or vars['receivingTeam'] == "Memphis" or vars['receivingTeam'] == "Grizzlies":
            team = 'MEM'
        elif vars['receivingTeam'] == "Miami Heat" or vars['receivingTeam'] == "Miami":
            team = 'MIA'
        elif vars['receivingTeam'] == "Milwaukee Bucks" or vars['receivingTeam'] == "Milwaukee" or vars['receivingTeam'] == "Bucks":
            team = 'MIL'
        elif vars['receivingTeam'] == "Minnesota Timberwolves" or vars['receivingTeam'] == "Minnesota" or vars['receivingTeam'] == "Timberwolves":
            team = 'MIN'
        elif vars['receivingTeam'] == "New Orleans Pelicans" or vars['receivingTeam'] == "Pelicans" or vars['receivingTeam'] == "NoLa":
            team = 'NOP'
        elif vars['receivingTeam'] == "New York Knicks" or vars['receivingTeam'] == "Knicks" or vars['receivingTeam'] == "NY":
            team = 'NYK'
        elif vars['receivingTeam'] == "Oklahoma City Thunder" or vars['receivingTeam'] == "Thunder" or vars['receivingTeam'] == "OKC":
            team = 'OKC'
        elif vars['receivingTeam'] == "Orlando Magic" or vars['receivingTeam'] == "Orlando" or vars['receivingTeam'] == "Magic":
            team = 'ORL'
        elif vars['receivingTeam'] == "Philadelphia SeventySixers" or vars['receivingTeam'] == "Philly" or vars['receivingTeam'] == "SeventySixers" or vars['receivingTeam'] == "76ers":
            team = 'PHI'
        elif vars['receivingTeam'] == "Phoenix Suns" or vars['receivingTeam'] == "Phoenix" or vars['receivingTeam'] == "Suns":
            team = 'PHX'
        elif vars['receivingTeam'] == "Portland Trail Blazers" or vars['receivingTeam'] == vars['receivingTeam'] == "Portland" or vars['receivingTeam'] == "Trail Blazers":
            team = 'POR'
        elif vars['receivingTeam'] == "Sacramento Kings" or vars['receivingTeam'] == "Sacramento" or vars['receivingTeam'] == "Kings":
            team = 'SAC'
        elif vars['receivingTeam'] == "San Antonio Spurs" or vars['receivingTeam'] == "San Antonio" or vars['receivingTeam'] == "Spurs":
            team = 'SAS'
        elif vars['receivingTeam'] == "Toronto Raptors" or vars['receivingTeam'] == "Toronto" or vars['receivingTeam'] == "Raptors":
            team = 'TOR'
        elif vars['receivingTeam'] == "Utah Jazz" or vars['receivingTeam'] == "Utah" or vars['receivingTeam'] == "Jazz":
            team = 'UTA'
        elif vars['receivingTeam'] == "Washington Wizards" or vars['receivingTeam'] == "Washington" or vars['receivingTeam'] == "Wizards":
            team = 'WAS'
        else:
            # error handling? idk if needed
            return "I didn't get that"

        wins = 0
        losses = 0
        teamSchedule = Schedule(team)
        for game in teamSchedule:
            if game.result == 'Win':
                wins += 1
            else:
                losses += 1

        return "The {} are currently {} and {} ".format(vars['receivingTeam'], wins, losses)

class tradeNewsOld(Macro):
    def run (self, ngrams, vars, args):
        response = requests.get("https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json")
        test = response.json()
        trades = [x for x in test['NBA_Player_Movement']['rows'] if x['Transaction_Type'] == 'Trade']
        trade = trades[0]['TRANSACTION_DESCRIPTION']
        receivingTeam = trade.split(' received')[0]
        givingTeam = trade.split('from ')[1]
        givingTeam = givingTeam[:-1]
        player = trade.split('received ')[1]
        player = player.split('from')[0]

        playerList = player.split(' ')
        role = playerList[0]
        playerList.pop(0)
        player = ' '.join(playerList)

        vars['receivingTeam'] = receivingTeam
        vars['givingTeam'] = givingTeam
        vars['player'] = player

        return "I found this most recent trade news that {} from {} is going to {}".format(player, givingTeam, receivingTeam)

class tradeNews(Macro):
    def run (self, ngrams, vars, args):
        with open('trades.json') as f:
            data = json.load(f)
        trades = data['trades']
        n = randrange(len(trades))
        trade = trades[n]['TRANSACTION_DESCRIPTION']
        vars['date'] = trades[n]["TRANSACTION_DATE"].split('-')[1]
        receivingTeam = trade.split(' received')[0]
        givingTeam = trade.split('from ')[1]
        givingTeam = givingTeam[:-1]
        player = trade.split('received ')[1]
        player = player.split('from')[0]

        playerList = player.split(' ')
        role = playerList[0]
        playerList.pop(0)
        player = ' '.join(playerList)

        vars['receivingTeam'] = receivingTeam
        vars['givingTeam'] = givingTeam
        vars['player'] = player
        vars['tradeTeamInPlayoffs'] = receivingTeam

        return "{} from {} is going to {}".format(player, givingTeam, receivingTeam)

class tradeNewsByTeam(Macro):
    def run (self, ngrams, vars, args):
        with open('trades.json') as f:
            data = json.load(f)
        all_trades = data['trades']

        if 'favUserTeam' in vars:
            trades = [x for x in all_trades if vars['favUserTeam'].lower() in x['TRANSACTION_DESCRIPTION'].lower()]
            #vars['receivingTeam'] = 'favUserTeam'
            if not trades:
                trades = [x for x in all_trades if vars['favSysTeam'].lower() in x['TRANSACTION_DESCRIPTION'].lower()]
        else: 
            trades = [x for x in all_trades if vars['favSysTeam'].lower() in x['TRANSACTION_DESCRIPTION'].lower()]

        trade = trades[randrange(len(trades))]['TRANSACTION_DESCRIPTION']
        receivingTeam = trade.split(' received')[0]
        givingTeam = trade.split('from ')[1]
        givingTeam = givingTeam[:-1]
        player = trade.split('received ')[1]
        player = player.split('from')[0]

        playerList = player.split(' ')
        role = playerList[0]
        playerList.pop(0)
        player = ' '.join(playerList)

        if 'favUserTeam' in vars:
            vars['tradeTeamInPlayoffs'] = vars['favUserTeam']
        else:
            vars['tradeTeamInPlayoffs'] = vars['favSysTeam']
        vars['receivingTeam'] = receivingTeam
        vars['givingTeam'] = givingTeam
        vars['player'] = player

        return "{} from {} went to {}".format(player, givingTeam, receivingTeam)


class goodBadTrade(Macro):
    def run (self, ngrams, vars, args):
        if vars['goodBadPlayer'] == 'good':
            return "this is a good trade for the {}".format(vars['receivingTeam'])
        else:
            return "this is a bad trade for the {}".format(vars['receivingTeam'])

class botFavTeam(Macro):
    def run (self, ngrams, vars, args):
        if 'favUserTeam' in vars:
            if vars['favUserTeam'] in 'los angeles clippers' or vars['favUserTeam'] in 'lA clippers' or vars['favUserTeam'] in 'clippers':
                vars['favSysTeam'] = 'Miami Heat'
                vars['favSysPlayer'] = 'Jimmy Butler'
                vars['favSysPlayerPER'] = 23.41
                vars['favSysPlayerPTS'] = 20.2
                vars['favSysPlayerREB'] = 6.6
                vars['favSysPlayerAST'] = 6.1
                return

        if 'favUserTeam' in vars:
            if vars['favUserTeam'] in 'miami heat' or vars['favUserTeam'] in 'heat' or vars['favUserTeam'] in 'miami':
                vars['favSysTeam'] = 'Clippers'
                vars['favSysPlayer'] = 'Kawhi Leonard'
                vars['favSysPlayerPER'] = 26.76
                vars['favSysPlayerPTS'] = 26.9
                vars['favSysPlayerREB'] = 7.3
                vars['favSysPlayerAST'] = 5.0
                return

        vars['favSysTeam'] = 'Clippers'
        vars['favSysPlayer'] = 'Kawhi Leonard'
        vars['favSysPlayerPER'] = 26.76
        vars['favSysPlayerPTS'] = 26.9
        vars['favSysPlayerREB'] = 7.3
        vars['favSysPlayerAST'] = 5.0
        return

class nextYearPlayoffImpact(Macro):
    def run(self, ngrams, vars, args):
        n = vars['player'].lower().split()
        playerid = ""
        if (len(n[1]) >= 5):  # edge case for names with shorter than 5 characters/jr. resolved
            for i in range(5):
                playerid += n[1][i]
        else:
            for i in range(len(n[1])):
                playerid += n[1][i]
        for i in range(2):
            playerid += n[0][i]
        if playerid == "morrima":
            playerid = "morrima03"
        elif playerid == "thomais":
            playerid = "thomais02"
        else:
            playerid += "01"
        player = Player(playerid)
        playerBirthDate = player.birth_date
        playerBirthYear = int(playerBirthDate.strftime("%Y"))
        if playerBirthYear <= 1993:
            str = "I do not think he will play a big role. I think he is past his prime."
        else:
            str = "I think he is young enough to get better in the future."

        return str



        
class playerRating(Macro): #*** *** *** ***
    def run (self, ngrams, vars, args):
        n = vars['player'].lower().split()
        playerid = ""
        if (len(n[1]) >= 5):    #edge case for names with shorter than 5 characters/jr. resolved
            for i in range(5):
                playerid += n[1][i]
        else:
            for i in range(len(n[1])):
                playerid += n[1][i]
        for i in range(2):
            playerid += n[0][i]
        if playerid == "morrima":
            playerid = "morrima03"
        elif playerid == "thomais":
            playerid = "thomais02"
        else:
            playerid += "01"
        player = Player(playerid)
        position = player.position
        exp = player.games_played
        # career stats: average points/rebounds/blocks/etc per game
        C_REB = player.total_rebounds / player.games_played
        C_PTS = player.points / player.games_played
        C_AST = player.assists / player.games_played
        # current year stats: average points/rebounds/blocks/etc per game
        player = player('2019-20')
        REB = player('2019-20').total_rebounds / player('2019-20').games_played
        # BLK = player.shots_blocked / player.minutes_played * 40
        PTS = player('2019-20').points / player('2019-20').games_played
        time = player('2019-20').minutes_played / player('2019-20').games_played
        # FLD_GOAL = player.field_goal_percentage
        # THR_PT = player.three_point_percentage
        # TW_PT = player.two_point_percentage
        AST = player('2019-20').assists / player('2019-20').games_played
        PER = player('2019-20').player_efficiency_rating
        response = ''
        if (PER > 14):
            vars['goodBadPlayer'] = 'good'
            if (exp < 246):
                response = response + "As an unexperienced player, I think " + player.name
                if (C_PTS >= 16 or C_AST >= 5 or C_REB >= 9):
                    response += " had a great career so far."
            elif (exp < 500):
                response = response + "As a player who have some experience, I think " + player.name
                if (C_PTS >= 16 or C_AST >= 5 or C_REB >= 9):
                    response += " had a great career so far."
            else:
                response = response + "As a veteran player, I think " + player.name
                if (C_PTS >= 16 or C_AST >= 5 or C_REB >= 9):
                    response += " is one of exceptional players that ever played the game."
                else:
                    response += " had a stable career."
            if (REB > 7 and PTS > 15 and AST > 5):
                response = response + "I think he became the core of the team. And his points, rebounds, and assists reflect that."
            elif (REB > 7):
                response = response + "With his rebounding skills, I think the team has really benefited from receiving " + player.name + "."
            elif (PTS > 15):
                response = response + "He has been scoring really well making a good contribution to " + vars['receivingTeam']
            elif (AST > 5):
                response = response + "His distribution of ball has really lifted " + vars['receivingTeam']
            else:
                response += "He has been making stable contribution to the team even though his stats don't stand out."
            response += " And I think his contribution can get even better if playoff was to start."
            return response
        else:
            vars['goodBadPlayer'] = 'bad'
            if (PTS <= 8): #it prints this part all the time
                response += "for this season, he's not contributing enough to the team especially with scoring "
            elif (position == "C" or position == "PF" and REB <= 4):
                if (PTS <= 8):
                    response += "and rebounds"
                else:
                    response += "in the current season, He's not a good rebounder for his position. "
            elif (position == "PG" and AST <= 3):
                if(PTS <= 8):
                    response += "and assists even though he is a point guard."
                else:
                    response += "He is not that great with his assists even though he is a point guard. "
            else:
                response += "I dont think he is too terrible but he doesnt seem to have a huge impact to the game."
            if (player('2019-20').minutes_played / player('2019-20').games_played < 12 or player('2019-20').minutes_played == None):
                response += "Also, he barely has any games played this season!"
            else:
                if (C_PTS >= 15):
                    response + "He had a decent career though."
            return response

class comparePlayers(Macro): #*** *** *** ***
    def run (self, ngrams, vars, args):
        n = vars['favUserPlayer'].split()
        s = ""
        if (len(n[1]) >= 5):    #edge case for names with shorter than 5 characters/jr. resolved
            for i in range(5):
                s += n[1][i]
        else:
            for i in range(len(n[1])):
                s += n[1][i]
        for i in range(2):
            s += n[0][i]
        s += "01"
        playerid = s.lower()
        player = Player(playerid)
        games_played = player('2019-20').games_played
        vars['favUserPlayerPER'] = player('2019-20').player_efficiency_rating
        vars['favUserPlayerPTS'] = player('2019-20').points/games_played
        vars['favUserPlayerREB'] = player('2019-20').total_rebounds/games_played
        vars['favUserPlayerAST'] = player('2019-20').assists/games_played

        ##PER was not mentioned so idk if its something we want to add
        if vars['favUserPlayerPTS']  > 20 or vars['favUserPlayerAST'] > 8 or vars['favUserPlayerREB'] > 10:
            return "I see {} is having an exceptional season. Personally, I think {} will win because {} is more clutch".format(vars['favUserPlayer'], vars['favSysTeam'], vars['favSysPlayer'])
        return "Its interesting that you like {} because he is not the top player statistically speaking. Personally, I think {} will win because of {}".format(vars['favUserPlayer'], vars['favSysTeam'], vars['favSysPlayer'])


class playerRationale(Macro): #*** *** *** ***
    def run (self, ngrams, vars, args):
        if vars['playerRationale'] == 'efficient' or vars['playerRationale'] == 'efficiency':
            if vars['favSysPlayerPER'] > vars['favUserPlayerPER']:
                return "Did you know that {} is actually more efficient than {}?".format(vars['favSysPlayer'], vars['favUserPlayer'])
            else:
                return "Yeah, you are right {} is more efficient than my favorite player, {}".format(vars['favUserPlayer'], vars['favSysPlayer'])
        if vars['playerRationale'] == 'points':
            if vars['favSysPlayerPTS'] > vars['favUserPlayerPTS']:
                return "Did you know that {} actually scores more points per game than {}?".format(vars['favSysPlayer'], vars['favUserPlayer'])
            else:
                return "Yeah, you are right {} scores more points per game than my favorite player, {}".format(vars['favUserPlayer'], vars['favSysPlayer'])
        if vars['playerRationale'] == 'rebounds' or vars['playerRationale'] == 'rebound':
            if vars['favSysPlayerREB'] > vars['favUserPlayerREB']:
                return "Did you know that {} actually has more rebounds per game than {}?".format(vars['favSysPlayer'], vars['favUserPlayer'])
            else:
                return "Yeah, you are right {} has more rebounds per game than my favorite player, {}".format(vars['favUserPlayer'], vars['favSysPlayer'])
        if vars['playerRationale'] == 'assists' or vars['playerRationale'] == 'assist':
            if vars['favSysPlayerAST'] > vars['favUserPlayerAST']:
                return "Did you know that {} actually has more assists per game than {}?".format(vars['favSysPlayer'], vars['favUserPlayer'])
            else:
                return "Yeah, you are right {} has more assists per game than my favorite player, {}".format(vars['favUserPlayer'], vars['favSysPlayer'])
class negativeSeedingImpact(Macro):
    def run (self, ngrams, vars, args):
        test = vars['playerImpact']
        with open('trades.json') as f:
            data = json.load(f)
        trades = data['trades']
        n = randrange(len(trades))
        #trade = trades[n]['TRANSACTION_DESCRIPTION']
        vars['date'] = trades[n]["TRANSACTION_DATE"].split('-')[1]
        if 2 <= int(vars['date']) < 9:
            return "actually though, i do not think he had enough time to impact the team because he was traded close to the covid shutdown"
        else:
            return "I agree, the trade was early in the season and he has not shown he was worth it"

class positiveSeedingImpact(Macro):
    def run (self, ngrams, vars, args):
        test = vars['playerImpact']
        with open('trades.json') as f:
            data = json.load(f)
        trades = data['trades']
        n = randrange(len(trades))
        #trade = trades[n]['TRANSACTION_DESCRIPTION']
        vars['date'] = trades[n]["TRANSACTION_DATE"].split('-')[1]
        if int(vars['date']) >=2 and int(vars['date']) < 9:
            return "he was traded quite recently before covid shutdown so maybe the stats wont be the same but who knows?"
        else:
            return "It certainly seems like he meshes well with the team"

class nicknameToPlayer(Macro):
    def run (self, ngrams, vars, args):
        with open('original_names.json') as f:
            data = json.load(f)
        new_dict= data['ontology']

        with open('teams.json') as g:
            data1 = json.load(g)
        onto_dict = data1['ontology']

        player_name_list = list(new_dict.values())

        if 'favUserPlayer' in vars:
            if vars['favUserPlayer'] not in (item for sublist in player_name_list for item in sublist):
                for key,value in onto_dict.items():
                    if vars['favUserPlayer'] in value:
                        vars['favUserPlayer'] = key

        return



class teamPlayerCheck(Macro):
    def run (self, ngrams, vars, args):
        with open('teams.json') as f:
            data = json.load(f)
        new_dict = data['ontology']

        vars['sameTeam'] = ""

        if 'favUserPlayer' in vars and 'favUserTeam' in vars:
            temp_dict = { key:value for (key,value) in new_dict.items() if vars['favUserPlayer'] in value}

            if vars['favUserTeam'] in list(temp_dict.keys()):
                vars['sameTeam'] = "yes"
            else:
                vars['sameTeam'] = "no"
        return

class sentiAnalyserFavSysTeam(Macro): #*** *** *** ***
    def run (self, ngrams, vars, args):
        sid = SentimentIntensityAnalyzer()

        text = vars["userOpinionSysTeamGen"]

        scores = sid.polarity_scores(text)


        if scores['neg'] < scores['pos']:
            return "Yes, I can tell that you have a very high opinion about the {}. I also think that they will win because of {}. What do you think of him?".format(vars['favSysTeam'], vars['favSysPlayer'])
        elif scores['pos'] < scores['neg']:

            return "Hmmm... I can tell you dont have a very high opinion about the {}, and I cant say I agree with your assessment. Even if youre right, I still think they can win because of {}. What do you think of him?".format(vars['favSysTeam'], vars['favSysPlayer'])
        else:

            return "Thats a very interesting opinion about the {}. I also think that they will win because of {}. What do you think of him?".format(vars['favSysTeam'],vars['favSysPlayer'])

class sentiAnalyserFavSysPlayer(Macro):
    def run (self, ngrams, vars, args):
        sid = SentimentIntensityAnalyzer()

        text = vars["userOpinionSysPlayerGen"]

        scores = sid.polarity_scores(text)

        if scores['neg'] < scores['pos']:
            return "Right! I can tell that you like {}, just like me! He's also really clutch at the end of games!".format(vars['favSysPlayer'])
        elif scores['pos'] < scores['neg']:

            return "Hmmm... okay I see you dont really like {}. I think that he is still pretty clutch in games".format(vars['favSysPlayer'])
        else:

            return "Thats a very interesting take on {}. For what its worth, I think he is pretty clutch in games".format(vars['favSysPlayer'] )

class sentiAnalyserTradePlayer(Macro):
    def run (self, ngrams, vars, args):
        sid = SentimentIntensityAnalyzer()

        text = vars["userOpinionTradePlayerGen"]

        scores = sid.polarity_scores(text)


        if scores['neg'] < scores['pos']:
            return "I can tell that you like {}".format(vars['player'])
        elif scores['pos'] < scores['neg']:

            return "Okay, I can tell that you dont like {}".format(vars['player'])
        else:
            return "Okay, I can tell youre pretty neutral about {}".format(vars['player'])


knowledge = KnowledgeBase()
knowledge.load_json_file("teams.json")
df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.SYSTEM, kb=knowledge, macros={'news': news(), 'newsPlayer': newsPlayer(), 'newsTeam': newsTeam(),
                                                                                                  'teamStats': teamStats(), 'playerRating' : playerRating(),
                                                                                                  'goodBadTrade' : goodBadTrade(), 'tradeNews' : tradeNews(),
                                                                                                  'botFavTeam': botFavTeam(), 'tradeNewsByTeam' : tradeNewsByTeam(),
                                                                                                  'comparePlayers' : comparePlayers(), 'positiveSeedingImpact' : positiveSeedingImpact(),
                                                                                                  'negativeSeedingImpact' : negativeSeedingImpact(),
                                                                                                  'teamPlayerCheck': teamPlayerCheck(), 'sentiAnalyserFavSysTeam': sentiAnalyserFavSysTeam(),
                                                                                                  'nicknameToPlayer': nicknameToPlayer(), 'nextYearPlayoffImpact': nextYearPlayoffImpact(),
                                                                                                  'sentiAnalyserFavSysPlayer': sentiAnalyserFavSysPlayer(),
                                                                                                  'sentiAnalyserTradePlayer':sentiAnalyserTradePlayer()})

# natex expressions
dont_know = '[{' \
            'dont know,do not know,unsure,maybe, do not have, [not,{sure,certain}],hard to say,no idea,uncertain,i guess,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[{dont,do not}, have, {one,opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[!{cant,cannot} {think,remember,recall}]' \
            '}]'


possible_results = '[{' \
                   'better,worse,obliterate,crush,destroy,change,effect,difference,improve,adjust,adapt,implications,good,bad,weird' \
                   '}]'

end = '[{'\
      'end,stop,terminate,cease'\
      '}]'

proceed = '[{'\
          'keep,continue,proceed,go on,carry on,ok,okay,fine,sounds good,yes'\
          '}]'

"""playoffs turns"""
#turn 1
df.add_system_transition(State.START, State.TURNPF1U, r'[! "Hi I am NBA chatbot. The NBA season has been" {shutdown,suspended,put on hold} "because of COVID-19. '
                                                      r' If we had playoffs" {based off the current standings,today,right now} ", which team do you think would win?"]')
df.add_user_transition(State.TURNPF1U, State.TURNPF2AS, dont_know)
df.add_user_transition(State.TURNPF1U, State.TURNPF2CS, '[$favUserTeam={#ONT(nonplayoffteams)}]')
df.add_user_transition(State.TURNPF1U, State.TURNPF2BS, '[$favUserTeam={#ONT(playoffteams)}]')

df.set_error_successor(State.TURNPF1U, State.TURNPF1ERR)
df.add_system_transition(State.TURNPF1ERR, State.TURNPF1ERRU, r'[! "Hmm," {I dont think that is an NBA team,I dont think thats a team going into the playoffs,yea not sure if thats a team going into playoffs} ". Do you want to keep talking? '
                                                            r'We can either stop the conversation here and talk about something else, or I can keep on talking with you about a team that I think can win!"]')
df.add_user_transition(State.TURNPF1ERRU, State.END, end)
df.add_user_transition(State.TURNPF1ERRU, State.TURNPF1ERR1S, proceed)
df.add_system_transition(State.TURNPF1ERR1S, State.TURNPF2AU, r'[! #botFavTeam {[! "Okay!"],[! "Aight!"],[! "Alrighty then!"]}{I hope that this will still be fun,I hope that this will still be entertaining,Hopefully this will still be interesting}'
                                                              r'"for you. I think that" $favSysTeam "can win the playoffs" {even with the unpredictability of the whole thing,if we were to play today,just based off current standings}'
                                                              r'". What do you think?"]')

#favUserTeam not in playoffs scenario
df.add_system_transition(State.TURNPF2CS, State.TURNNOPF1U, r'[! #botFavTeam "Based off the standings I dont think that the " $favUserTeam " would be in the playoffs. Who is your favorite player on the " $favUserTeam "?"]')
df.add_user_transition(State.TURNNOPF1U, State.TURNNOPF2S, '[$favUserPlayer={#ONT(teams)}]') #todo double check that it does not catch on teams and apply the favUserPlayer is on favUserTeam macro
df.add_user_transition(State.TURNNOPF1U, State.TURNPF5AS, dont_know) #todo double check the variables in TURNPF5AS and make sure they are all declared and no declaring macro needs to be called
df.set_error_successor(State.TURNNOPF1U, State.TURNNOPF1ERR)
df.add_system_transition(State.TURNNOPF1ERR, State.TURNPF5U, r'[! #nicknameToPlayer "My friend who is also a" $favUserTeam " fan thinks that too. Personally, I think" $favSysTeam "will win because they have" $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')

df.add_system_transition(State.TURNNOPF2S, State.TURNPF5U, '[! #nicknameToPlayer #comparePlayers() "What do you think of " $favSysPlayer "?"]')

#idk scenario
df.add_system_transition(State.TURNPF2AS, State.TURNPF2AU, r'[! #botFavTeam{Its okay to be unsure because predictability of playoffs is difficult without more data.,Its okay to be unsure.,'
                                                           r'Its definitely hard to tell right now.} "I think that the" $favSysTeam "can win" {if we were to play today.,given the available data.} "Do you agree?"]')
# 2AU takes agree, disagree, dont know, and error.
df.add_user_transition(State.TURNPF2AU, State.TURNPF3AS, '[#ONT(agree)]')
df.add_user_transition(State.TURNPF2AU, State.TURNPF3BS, '[#ONT(disagree)]')
df.add_user_transition(State.TURNPF2AU, State.TURNPF2A_DK, dont_know)
df.set_error_successor(State.TURNPF2AU, State.TURNPF2AERR)
df.add_system_transition(State.TURNPF2AERR, State.TURNPF5U, r'[! "Thats an interesting take for sure. Personally, I think" $favSysTeam "will win primarily because they have" $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')

df.add_system_transition(State.TURNPF3AS, State.TURNPF3AU, r'[! "Im glad you agree with me about" {them,[! "the" $favSysTeam]} ". "'
                                                           r' {Do you have any reason why you think,Why do you think,Why do you agree with me that}'
                                                           r' {they,[!"the" $favSysTeam]} "are going to win?"]')
df.add_system_transition(State.TURNPF3BS, State.TURNPF3AU, r'[! "Oh thats interesting! Why do you think the" $favSysTeam "will not win?"]')

# PF2A-dont know goes straight to 5U
df.add_system_transition(State.TURNPF2A_DK, State.TURNPF5U, r'[! "Oh, are you not sure? Personally, I think the" $favSysTeam "will win because they have" $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')

# good opinions
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_GOOD1, '[#NOT(#ONT(not)) $favSysTeamAdj={#ONT(adjPositive)}, $favSysTeamRationale={#ONT(rationale)}]') # they have a solid playstyle
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_GOOD2, '[#NOT(#ONT(not)) $favSysTeamRationale={#ONT(rationale)}, $favSysTeamAdj={#ONT(adjPositive)}]') # their playstyle is very solid
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_GOOD3, '[#NOT(#ONT(not)) $favSysTeamAdj={#ONT(adjPositive)}]') # they are very reliable
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_GOOD4, '[$favSysTeamRationale={#ONT(rationaleVerb)}, $favSysTeamAdv={#ONT(advPositive)}]') # they steal really well (verb + adv)
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_GOOD5, '[#NOT(#ONT(not)) $not={#ONT(not)}, $favSysTeamAdj={#ONT(adjNegative)}]') # they arent bad
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_GOOD6, '[#NOT(#ONT(not)) $favSysTeamRationale={#ONT(rationale)}]') # because of their efficiency
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_GOOD7, '[#NOT(#ONT(not)) $favSysTeamAdj={#ONT(adjPositive)}, $favSysTeamRationale={#ONT(rationalePerson)}]')
# bad opinions
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_BAD1, '[#NOT(#ONT(not)) $favSysTeamAdj={#ONT(adjNegative)}, $favSysTeamRationale={#ONT(rationale)}]')
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_BAD2, '[#NOT(#ONT(not)) $favSysTeamRationale={#ONT(rationale)}, $favSysTeamAdj={#ONT(adjNegative)}]')
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_BAD3, '[#NOT(#ONT(not)) $favSysTeamAdj={#ONT(adjNegative)}]')
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_BAD4, '[#NOT(#ONT(not)) $favSysTeamRationale={#ONT(rationaleVerb)}, $favSysTeamAdv={#ONT(advNegative)}]') # they steal really poorly
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_BAD5, '[$not={#ONT(not)}, $favSysTeamAdj={#ONT(adjPositive)}]') # they arent good
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_BAD6, '[#NOT(#ONT(not)) $favSysTeamRationale={#ONT(rationaleVerbNegative)}]') # they choke/underperform
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_BAD7, '[#NOT(#ONT(not)) $favSysTeamAdj={#ONT(adjNegative)}, $favSysTeamRationale={#ONT(rationalePerson)}]')
# generic error catcher
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S_OP_GEN, '[$userOpinionSysTeamGen=[/.*/] #NOT(#ONT(rationaleVerbNegative)},#ONT(rationale),#ONT(adjPositive),#ONT(adjNegative))]')


# 4S good opinion system
df.add_system_transition(State.TURNPF4S_OP_GOOD1, State.TURNPF5U, r'[! "Yes! I whole heartedly agree that the" $favSysTeam "has a really solid" $favSysTeamRationale'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_GOOD2, State.TURNPF5U, r'[! "Yes! I whole heartedly agree that the" $favSysTeam "has a really solid" $favSysTeamRationale'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_GOOD3, State.TURNPF5U, r'[! "Yes! I also agree that the" $favSysTeam "is really" $favSysTeamAdj'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_GOOD4, State.TURNPF5U, r'[! "Yes! I also agree that the" $favSysTeam "can" $favSysTeamRationale "extremely well"'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_GOOD5, State.TURNPF5U, r'[! "Yes! I also agree that the" $favSysTeam "are not" $favSysTeamAdj'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_GOOD6, State.TURNPF5U, r'[! "Yes! I whole heartedly agree that the" $favSysTeam "have a really solid" $favSysTeamRationale'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_GOOD7, State.TURNPF5U, r'[! "Yes! I whole heartedly agree that the" $favSysTeam "have really solid" $favSysTeamRationale'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
# 4S bad opinion system
df.add_system_transition(State.TURNPF4S_OP_BAD1, State.TURNPF5U, r'[! {Hmm..., I dont know., What...} "I mean maybe youre right that the" $favSysTeam "might not win because of their mediocre" '
                                                                r'$favSysTeamRationale ". I still think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_BAD2, State.TURNPF5U, r'[! {Hmm..., I dont know., What...} "I mean maybe youre right that the" $favSysTeam "might have poor" '
                                                                r'$favSysTeamRationale ". I still think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_BAD3, State.TURNPF5U, r'[! {Hmm..., I dont know., What...} "I actually dont agree with you that the" $favSysTeam "are" '
                                                                r'$favSysTeamAdj ". I still think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_BAD4, State.TURNPF5U, r'[! {Hmm..., I dont know., What...} "I actually dont think that the" $favSysTeam $favSysTeamRationale "badly"'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_BAD5, State.TURNPF5U, r'[! {Hmm..., I dont know., What...} "I actually dont agree with you when you say that the" $favSysTeam "are not" $favSysTeamAdj'
                                                                 r' ". In addition, I also think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_BAD6, State.TURNPF5U, r'[! {Hmm..., I dont know., What...} "I actually dont agree with you on your assessment that the" $favSysTeam "always" '
                                                                r'$favSysTeamRationale ". I still think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')
df.add_system_transition(State.TURNPF4S_OP_BAD7, State.TURNPF5U, r'[! {Hmm..., I dont know., What...} "I actually dont agree with you on your assessment that the" $favSysTeam "have poor" $favSysTeamRationale '
                                                                r'$favSysTeamRationale ". I still think that the" $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')

df.add_system_transition(State.TURNPF4S_OP_GEN, State.TURNPF5U, r'[! #sentiAnalyserFavSysTeam()]')
df.set_error_successor(State.TURNPF3AU, State.TURNPF3AERR)
df.add_system_transition(State.TURNPF3AERR, State.TURNPF5U, r'[! "That is a good opinion. Personally, I think " $favSysTeam "will win because of " $favSysPlayer ". " {What do you think of,Do you have any opinions about} $favSysPlayer "?"]')

df.add_user_transition(State.TURNPF2BU, State.TURNPF3FS, dont_know)
df.add_system_transition(State.TURNPF3FS, State.TURNPF3U, r'[! #botFavTeam {Its okay to be unsure, it can be hard to tell} "the" $favUserTeam "certainly have many strengths. I think that" $favSysTeam "can win" {if we were to play today,given the available data} " because of" $favSysPlayer ". What do you think of him?"]')

# Playoff Turn 2 (not idk scenario)
df.add_system_transition(State.TURNPF2BS, State.TURNPF2BU, r'[! #botFavTeam "Why do you think the" $favUserTeam "will win?"]')

df.add_user_transition(State.TURNPF2BU, State.TURNPF2BS1_OP_GOOD1, '[#NOT(#ONT(not)) $favUserTeamAdj={#ONT(adjPositive)}, $favUserTeamRationale={#ONT(rationale)}]') # they have a solid playstyle
df.add_user_transition(State.TURNPF2BU, State.TURNPF2BS1_OP_GOOD2, '[#NOT(#ONT(not)) $favUserTeamRationale={#ONT(rationale)}, $favUserTeamAdj={#ONT(adjPositive)}]') # their playstyle is very solid
df.add_user_transition(State.TURNPF2BU, State.TURNPF2BS1_OP_GOOD3, '[#NOT(#ONT(not),#ONT(rationale),#ONT(rationalePerson)) $favUserTeamAdj={#ONT(adjPositive)}]') # they are very reliable
df.add_user_transition(State.TURNPF2BU, State.TURNPF2BS1_OP_GOOD4, '[#NOT(#ONT(not)) $favUserTeamRationale={#ONT(rationaleVerb)}, $favUserTeamAdv={#ONT(advPositive)}]') # they steal really well (verb + adv)
df.add_user_transition(State.TURNPF2BU, State.TURNPF2BS1_OP_GOOD5, '[$not={#ONT(not)}, $favUserTeamAdj={#ONT(adjNegative)}]') # they arent bad
df.add_user_transition(State.TURNPF2BU, State.TURNPF2BS1_OP_GOOD6, '[#NOT(#ONT(not)) $favUserTeamRationale={#ONT(rationale)}]') # because of their efficiency
df.add_user_transition(State.TURNPF2BU, State.TURNPF2BS1_OP_GOOD7, '[#NOT(#ONT(not)) $favUserTeamAdj={#ONT(adjPositive)}, $favUserTeamRationale={#ONT(rationalePerson)}]')

# 2BU if they give a player name
df.add_user_transition(State.TURNPF2BU, State.TURNPF3CS,'[$favUserPlayer={#ONT(playoffteams),#ONT(nonplayoffteams)}]')

df.set_error_successor(State.TURNPF2BU, State.TURNPF2BU_ERR2)
df.add_system_transition(State.TURNPF2BU_ERR2, State.TURNPF2BU1, r'[! {Hmm..., I dont know., What...} "Personally, I do not think that the" $favUserTeam "are that good. '
                                                                 r' Which player do you think is most" {integral,important} "to the" $favUserTeam "?"]') #todo make sure this transition goes into the correct user transition

df.add_system_transition(State.TURNPF2BS1_OP_GOOD1, State.TURNPF2BU1, r'[! "Okay, having a really solid the" $favUserTeamRationale "is really important for" $favUserTeam'
                                                                 r' ". Do you think there is a player that is" {super,extremely,exceptionally} {integral,important} "to the" $favUserTeam "?"]')
df.add_system_transition(State.TURNPF2BS1_OP_GOOD2, State.TURNPF2BU1, r'[! "Okay, Ive heard that the" $favUserTeam "has a really solid" $favUserTeamRationale'
                                                                 r' ". Do you think there is a player that is" {really,super,extremely,exceptionally} {integral,important} "to the" $favUserTeam "?"]')
df.add_system_transition(State.TURNPF2BS1_OP_GOOD3, State.TURNPF2BU1, r'[! "Okay, Ive also heard that the" $favUserTeam "are really" $favUserTeamAdj'
                                                                 r' ". Do you think there is a player that is" {super,extremely,exceptionally} {integral,important} "to the" $favUserTeam "?"]')
df.add_system_transition(State.TURNPF2BS1_OP_GOOD4, State.TURNPF2BU1, r'[! "Okay, Ive also heard that the" $favUserTeam "can" $favUserTeamRationale "extremely well"'
                                                                 r' ". Do you think there is a player that is" {really,super,extremely,exceptionally} {integral,important} "to the" $favUserTeam "?"]')
df.add_system_transition(State.TURNPF2BS1_OP_GOOD5, State.TURNPF2BU1, r'[! "Okay, Ive also heard that the" $favUserTeam "are not" $favUserTeamAdj'
                                                                 r' ". Do you think there is a player that is" {super,extremely,exceptionally} {integral,important} "to the" $favUserTeam "?"]')
df.add_system_transition(State.TURNPF2BS1_OP_GOOD6, State.TURNPF2BU1, r'[! "Okay, Ive also heard that the" $favUserTeam "have really solid" $favUserTeamRationale'
                                                                 r' ". Do you think there is a player that is" {really,super,extremely,exceptionally} {integral,important} "to the" $favUserTeam "?"]')
df.add_system_transition(State.TURNPF2BS1_OP_GOOD7, State.TURNPF2BU1, r'[! "Okay, Ive also heard that the" $favUserTeam "have really solid" $favUserTeamRationale'
                                                                 r' ". Do you think there is a player that is" {super,extremely,exceptionally} {integral,important} "to the" $favUserTeam "?"]')

df.add_user_transition(State.TURNPF2BU1, State.TURNPF3CS, '[$favUserPlayer={#ONT(playoffteams),#ONT(nonplayoffteams)}]')
df.add_user_transition(State.TURNPF2BU1, State.TURNPF3DS, '[#ONT(agree) #NOT(#ONT(playoffteams),#ONT(nonplayoffteams),#NER(person))]')
df.add_user_transition(State.TURNPF2BU1, State.TURNPF3ES, '[{#NER(person)} #NOT(#ONT(playoffteams),#ONT(nonplayoffteams))]')
df.add_user_transition(State.TURNPF2BU1, State.TURNPF5AS, '[#ONT(disagree) #NOT(#ONT(playoffteams),#ONT(nonplayoffteams),#NER(person))]')


df.add_user_transition(State.TURNPF2BU1, State.TURNPF2BDK, dont_know)
df.add_system_transition(State.TURNPF2BDK, State.TURNPF5U, r'[! "Fair enough, there might actually be many good players on" $favUserTeam ". The best player on my favorite playoff team is " $favSysPlayer ". What do you think of him?"]')

df.add_system_transition(State.TURNPF3DS, State.TURNPF3DU, r'[! "Which player is that?"]')
df.add_user_transition(State.TURNPF3DU, State.TURNPF3CS, '[$favUserPlayer={#ONT(playoffteams),#ONT(nonplayoffteams)}]')
df.add_user_transition(State.TURNPF3DU, State.TURNPF3ES, '[{#NER(person)} #NOT(#ONT(playoffteams),#ONT(nonplayoffteams))]')
df.add_system_transition(State.TURNPF3ES, State.TURNPF5U, r'[! "I dont think thats a player on the" $favUserTeam ", but thats okay!'
                                                          r' Personally, I think that" $favSysTeam "has the best chance of winning because of" $favSysPlayer ". He is my hometown hero. What do you think of" {him,$favSysPlayer} "?"]')

df.set_error_successor(State.TURNPF2BU1, State.TURNPF2BU_ERR3)
df.add_system_transition(State.TURNPF2BU_ERR3, State.TURNPF5U, r'[! "Thats a fair" {reason.,rationale.,line of thought.} "Personally, I think that" $favSysTeam "has the best chance of winning because of" $favSysPlayer ". He is my hometown hero. What do you think of" {him,$favSysPlayer} "?"]')

# Playoff Turn 3

df.add_system_transition(State.TURNPF3CS, State.TURNPF3U, r'[! #nicknameToPlayer #teamPlayerCheck #GATE(sameTeam:yes) #comparePlayers {[! ". What do you think of"],[! ". Whats your opinion of"]} {him,$favSysPlayer}"?"]')
df.add_system_transition(State.TURNPF3CS, State.TURNPF5U, r'[! #nicknameToPlayer #teamPlayerCheck #GATE(sameTeam:no) "Huh, I dont think thats a player on the" $favUserTeam'
                                                          r'", but" #comparePlayers {[! ". What do you think of"],[! ". Whats your opinion of"]} {him,$favSysPlayer}"?"]')
# todo: revise this to also be able to catch "I guess i can agree with you" and similar phrasing

df.add_user_transition(State.TURNPF3U, State.TURNPF8AS, "[#GATE(favSysPlayer:Jimmy Butler) $butlerOpinion={#ONT(butlerNeg)}]") #handles situation with butlerNeg verb
df.add_user_transition(State.TURNPF3U, State.TURNPF8BS, "[#GATE(favSysPlayer:Jimmy Butler) $butlerOpinion={#ONT(butlerIsNeg)}]") #handles butlerNeg adj
df.add_user_transition(State.TURNPF3U, State.TURNPF8CS, "[#GATE(favSysPlayer:Jimmy Butler) $butlerOpinion={#ONT(butlerIsPos)}]") #handles butlerPos adj
df.add_user_transition(State.TURNPF3U, State.TURNPF8DS, "[#GATE(favSysPlayer:Jimmy Butler) $butlerOpinion={#ONT(butlerPos)}]") #handles butlerPos verb
df.add_user_transition(State.TURNPF3U, State.TURNPF8ES, "[#GATE(favSysPlayer:Kawhi Leonard) $kawhiOpinion={#ONT(kawhiHasPos)}]") #handles KawhiPos adj
df.add_user_transition(State.TURNPF3U, State.TURNPF8FS, "[#GATE(favSysPlayer:Kawhi Leonard) $kawhiOpinion={#ONT(kawhiIsPos)}]") #handles KawhiPos verb
df.add_user_transition(State.TURNPF3U, State.TURNPF8GS, "[#GATE(favSysPlayer:Kawhi Leonard) $kawhiOpinion={#ONT(kawhiIsNeg)}]") #handles KawhiNeg adj
df.add_user_transition(State.TURNPF3U, State.TURNPF8HS, "[#GATE(favSysPlayer:Kawhi Leonard) $kawhiOpinion={#ONT(kawhiNeg)}]") #handles KawhiNeg verb

# df.add_user_transition(State.TURNPF3U, State.TURNTRADE0S, "[$playerRationale={#ONT(rationale)}]")
# df.add_user_transition(State.TURNPF3U, State.TURNTRADE0BS, "{#ONT(agree)}")
df.add_user_transition(State.TURNPF3U, State.TURNPF6S, '[{why,[what makes you {think,say,believe}],[whats {your,the} reason]}]') #todo *** there is a bug here ***

df.add_system_transition(State.TURNPF8AS, State.TURNTRADE0U, r'[! "You might think that" {he, Butler} $butlerOpinion "but I think he always comes out clutch in playoffs. Speaking of playoffs, I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]') #handles situation with butlerNeg verb
df.add_system_transition(State.TURNPF8BS, State.TURNTRADE0U, r'[! "I have also heard others say that" {he, Butler} $butlerOpinion "but I think he turns into a carry player during playoffs. Speaking of playoffs, I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]') #handles situation with butlerNeg verb
df.add_system_transition(State.TURNPF8CS, State.TURNTRADE0U, r'[! "I agree that" {he, Butler} "is a" {great, big} $butlerOpinion ", I think that is his " {top, best} "quality. Earlier in the season, I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]') #handles situation with butlerPos adj
df.add_system_transition(State.TURNPF8DS, State.TURNTRADE0U, r'[! "I agree that" {he, Butler} $butlerOpinion ". It is those intangibles that make him a " {superstar, top player, allstar} ". Earlier in the season, I saw that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]') #handles situation with butlerPos verb verb
df.add_system_transition(State.TURNPF8ES, State.TURNTRADE0U, r'[! "Yeah," {he, Kawhi} "definitely has" $kawhiOpinion ". They have helped him be a " {superstar, top player, allstar} " year after year. Earlier in the season, I saw that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]') #handles situation with butlerPos verb verb
df.add_system_transition(State.TURNPF8FS, State.TURNTRADE0U, r'[! "Yeah," {he, Kawhi} "definitely is a" $kawhiOpinion ". But he " {shows up, steps up, performs} " very well in playoffs. Earlier in the season, I saw that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]') #handles situation with butlerPos verb verb
df.add_system_transition(State.TURNPF8GS, State.TURNTRADE0U, r'[! "Even though" {he, Kawhi} "is" $kawhiOpinion " he always " {shows up, overperforms} " in playoffs. Anyways, I saw that" {#tradeNewsByTeam()} ". What are your thoughts about " $player "?"]') #handles situation with Kawhi neg adj
df.add_system_transition(State.TURNPF8HS, State.TURNTRADE0U, r'[! "I actually agree with you that" {he, Kawhi} $kawhiOpinion "but he always " {shows up, overperforms} " in playoffs. Anyways, I saw that" {#tradeNewsByTeam()} ". What are your thoughts about " $player "?"]') #handles situation with Kawhi neg verb

# good opinions
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_GOOD1, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjPositive)}, $favSysPlayerRationale={#ONT(rationale)}]') # they have a solid playstyle
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_GOOD2, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationale)}, $favSysPlayerAdj={#ONT(adjPositive)}]') # their playstyle is very solid
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_GOOD3, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjPositive)}]') # they are very reliable
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_GOOD4, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationaleVerb)}, $favSysPlayerAdv={#ONT(advPositive)}]') # they steal really well (verb + adv)
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_GOOD5, '[$not={#ONT(not)}, $favSysPlayerAdj={#ONT(adjNegative)}]') # they arent bad
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_GOOD6, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationale)}]') # because of their efficiency
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_GOOD7, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjPositive)}, $favSysPlayerRationale={#ONT(rationalePerson)}]')
# bad opinions
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_BAD1, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjNegative)}, $favSysPlayerRationale={#ONT(rationale)}]') # he has poor shooting
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_BAD2, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationale)}, $favSysPlayerAdj={#ONT(adjNegative)}]')
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_BAD3, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjNegative)}]')
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_BAD4, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationaleVerb)}, $favSysPlayerAdv={#ONT(advNegative)}]') # they steal really poorly
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_BAD5, '[$not={#ONT(not)}, $favSysPlayerAdj={#ONT(adjPositive)}]') # they arent good
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_BAD6, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationaleVerbNegative)}]') # they choke/underperform
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_BAD7, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjNegative)}, $favSysPlayerRationale={#ONT(rationalePerson)}]')
# generic error catcher that throws to a sentiment analyzer
df.add_user_transition(State.TURNPF3U, State.TURNPF6S_OP_GEN, '[$userOpinionSysPlayerGen=[/.*/] '
                                                              '#NOT(#ONT(rationaleVerbNegative),#ONT(rationale),#ONT(adjPositive),#ONT(adjNegative),'
                                                              '#ONT(butlerNeg),#ONT(butlerIsNeg),#ONT(butlerIsPos),#ONT(butlerPos),#ONT(kawhiHasPos),'
                                                              '#ONT(kawhiIsPos),#ONT(kawhiIsNeg),#ONT(kawhiNeg),#ONT(questionWords))]')

# Error succ for PF3U
df.set_error_successor(State.TURNPF3U, State.TURNPF3U_ERR)
df.add_system_transition(State.TURNPF3U_ERR, State.TURNTRADE0U, r'[! "Huh, I never thought about it that way. Speaking about the teams though, earlier in the season" #tradeNewsByTeam() " What do you think about" $player "?"]')


df.add_system_transition(State.TURNPF5AS, State.TURNPF5U, r'[! "It sounds like you do not think there is a star player on the" $favUserTeam ". I think that the" $favSysTeam "will win because of their star player," $favSysPlayer ". What do you think of him?"]')
df.add_user_transition(State.TURNPF5U, State.TURNPF8AS, "[#GATE(favSysPlayer:Jimmy Butler) $butlerOpinion={#ONT(butlerNeg)}]") #handles situation with butlerNeg verb
df.add_user_transition(State.TURNPF5U, State.TURNPF8BS, "[#GATE(favSysPlayer:Jimmy Butler) $butlerOpinion={#ONT(butlerIsNeg)}]") #handles butlerNeg adj
df.add_user_transition(State.TURNPF5U, State.TURNPF8CS, "[#GATE(favSysPlayer:Jimmy Butler) $butlerOpinion={#ONT(butlerIsPos)}]") #handles butlerPos adj
df.add_user_transition(State.TURNPF5U, State.TURNPF8DS, "[#GATE(favSysPlayer:Jimmy Butler) $butlerOpinion={#ONT(butlerPos)}]") #handles butlerPos verb
df.add_user_transition(State.TURNPF5U, State.TURNPF8ES, "[#GATE(favSysPlayer:Kawhi Leonard) $kawhiOpinion={#ONT(kawhiHasPos)}]") #handles KawhiPos adj
df.add_user_transition(State.TURNPF5U, State.TURNPF8FS, "[#GATE(favSysPlayer:Kawhi Leonard) $kawhiOpinion={#ONT(kawhiIsPos)}]") #handles KawhiPos verb
df.add_user_transition(State.TURNPF5U, State.TURNPF8GS, "[#GATE(favSysPlayer:Kawhi Leonard) $kawhiOpinion={#ONT(kawhiIsNeg)}]") #handles KawhiNeg adj
df.add_user_transition(State.TURNPF5U, State.TURNPF8HS, "[#GATE(favSysPlayer:Kawhi Leonard) $kawhiOpinion={#ONT(kawhiNeg)}]") #handles KawhiNeg verb
df.add_user_transition(State.TURNPF5U, State.TURNPF6S, '[{why,[what makes you {think,say,believe}],[whats {your,the} reason]}]')

# 5U picks up all states where favUserPlayer has not been called (so no compare players)

# Error succ for PF5U
df.set_error_successor(State.TURNPF5U, State.TURNPF5U_ERR)
df.add_system_transition(State.TURNPF5U_ERR, State.TURNTRADE0U, r'[! "I see, thats a fair opinion. Speaking about the teams, earlier in the season" #tradeNewsByTeam() " What do you think about" $player "?"]')


# good opinions
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_GOOD1, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjPositive)}, $favSysPlayerRationale={#ONT(rationale)}]') # they have a solid playstyle
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_GOOD2, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationale)}, $favSysPlayerAdj={#ONT(adjPositive)}]') # their playstyle is very solid
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_GOOD3, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjPositive)}]') # they are very reliable
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_GOOD4, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationaleVerb)}, $favSysPlayerAdv={#ONT(advPositive)}]') # they steal really well (verb + adv)
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_GOOD5, '[$not={#ONT(not)}, $favSysPlayerAdj={#ONT(adjNegative)}]') # they arent bad
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_GOOD6, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationale)}]') # because of their efficiency
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_GOOD7, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjPositive)}, $favSysPlayerRationale={#ONT(rationalePerson)}]')
# bad opinions
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_BAD1, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjNegative)}, $favSysPlayerRationale={#ONT(rationale)}]') # he has poor shooting
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_BAD2, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationale)}, $favSysPlayerAdj={#ONT(adjNegative)}]')
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_BAD3, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjNegative)}]')
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_BAD4, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationaleVerb)}, $favSysPlayerAdv={#ONT(advNegative)}]') # they steal really poorly
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_BAD5, '[$not={#ONT(not)}, $favSysPlayerAdj={#ONT(adjPositive)}]') # they arent good
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_BAD6, '[#NOT(#ONT(not)) $favSysPlayerRationale={#ONT(rationaleVerbNegative)}]') # they choke/underperform
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_BAD7, '[#NOT(#ONT(not)) $favSysPlayerAdj={#ONT(adjNegative)}, $favSysPlayerRationale={#ONT(rationalePerson)}]')
# generic error catcher that throws to a sentiment analyzer
df.add_user_transition(State.TURNPF5U, State.TURNPF6S_OP_GEN, '[$userOpinionSysPlayerGen=[/.*/] '
                                                              '#NOT(#ONT(rationaleVerbNegative),#ONT(rationale),#ONT(adjPositive),#ONT(adjNegative),'
                                                              '#ONT(butlerNeg),#ONT(butlerIsNeg),#ONT(butlerIsPos),#ONT(butlerPos),#ONT(kawhiHasPos),'
                                                              '#ONT(kawhiIsPos),#ONT(kawhiIsNeg),#ONT(kawhiNeg),#ONT(questionWords))]')

# good opinion responses
df.add_system_transition(State.TURNPF6S_OP_GOOD1, State.TURNTRADE0U, r'[! {Exactly,Yes,Right,Wow} "! I completely agree with you that" $favSysPlayer "has a really solid" $favSysPlayerRationale'
                                                                 r' ". Lets go back to the teams now. I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_GOOD2, State.TURNTRADE0U, r'[! {Exactly,Yes,Right,Wow} "! I completely agree with you that" $favSysPlayer "has a really solid" $favSysPlayerRationale'
                                                                 r' ". Lets go back to the teams now. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_GOOD3, State.TURNTRADE0U, r'[! {Exactly,Yes,Right,Wow} "! I also agree that" $favSysPlayer "is really" $favSysPlayerAdj'
                                                                 r' ". Lets go back to the teams now. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_GOOD4, State.TURNTRADE0U, r'[! {Exactly,Yes,Right,Wow} "! I completely agree with you that" $favSysPlayer "can" $favSysPlayerRationale "extremely well"'
                                                                 r' ". Lets go back to the teams now. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_GOOD5, State.TURNTRADE0U, r'[! {Exactly,Yes,Right,Wow} "! I completely agree with you that" $favSysPlayer "are not" $favSysPlayerAdj'
                                                                 r' ". Lets go back to the teams now. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_GOOD6, State.TURNTRADE0U, r'[! {Exactly,Yes,Right,Wow} "! I completely agree with you that" $favSysPlayer "has a really solid" $favSysPlayerRationale'
                                                                 r' ". Lets go back to the teams now. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_GOOD7, State.TURNTRADE0U, r'[! {Exactly,Yes,Right,Wow} "! I completely agree with you that" $favSysPlayer "is a really solid" $favSysPlayerRationale'
                                                                 r' ". Lets go back to the teams now. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
# bad opinion responses
df.add_system_transition(State.TURNPF6S_OP_BAD1, State.TURNTRADE0U, r'[! {Hmm..., What...} "I mean I hear you when you say" $favSysPlayer "has bad" $favSysPlayerRationale ", but hes also extremely clutch!"'
                                                                 r' ". Lets go back to the teams for now though. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_BAD2, State.TURNTRADE0U, r'[! {Hmm..., What...} "I mean maybe youre right that the" $favSysPlayer "might have poor" $favSysPlayerRationale ", but hes also extremely clutch!"'
                                                                 r' ". Lets go back to the teams for now though. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_BAD3, State.TURNTRADE0U, r'[! {Hmm..., What...} "I actually dont agree with you." $favSysPlayer "is not" $favSysPlayerAdj ". Hes actually really clutch in the games"'
                                                                 r' ". Lets go back to the teams for now though. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_BAD4, State.TURNTRADE0U, r'[! {Hmm..., What...} "I actually dont think that the" $favSysPlayer $favSysPlayerRationale "badly. Hes actually really clutch in games!"'
                                                                 r' ". Lets go back to the teams for now though. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_BAD5, State.TURNTRADE0U, r'[! {Hmm..., What...} "No I completely disagree with you when you say that" $favSysPlayer "is not" $favSysPlayerAdj ". Hes actually super clutch in games!"'
                                                                 r' ". Lets go back to the teams for now though. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_BAD6, State.TURNTRADE0U, r'[! {Hmm..., What...} "No I completely disagree with you when you say that" $favSysPlayer "always" $favSysPlayerRationale ". Hes actually really clutch in games!"'
                                                                 r' ". Lets go back to the teams for now though. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_system_transition(State.TURNPF6S_OP_BAD7, State.TURNTRADE0U, r'[! {Hmm..., What...} "No I completely disagree with you when you say that" $favSysPlayer "is a bad" $favSysPlayerRationale ". Hes actually really clutch in games too!"'
                                                                 r' ". Lets go back to the teams for now though. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
# generic opinion response
df.add_system_transition(State.TURNPF6S_OP_GEN, State.TURNTRADE0U, r'[! #sentiAnalyserFavSysPlayer() '
                                                                   r'". Lets go back to the teams for now though. Earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')



# PF6S: System makes a claim why it thinks favSysPlayer is integral to team
df.add_system_transition(State.TURNPF6S, State.TURNPF6U, r'[! "Mostly because" $favSysPlayer "is really" {integral to the,important to the, key to the} $favSysTeam ". He"'
                                                         r'{is super clutch,is always making ridiculous shots,is such a great team player}{especially at important moments in the game,especially at the end of games}. "Do you think there is someone on the " $favSysTeam "who is better?"]')

# PF6U takes a disagreement or any statement, then goes to PF7
df.add_user_transition(State.TURNPF6U, State.TURNPF7S1, '[#ONT(agree)]')
df.add_user_transition(State.TURNPF6U, State.TURNPF7BS, dont_know)
df.add_user_transition(State.TURNPF6U, State.TURNPF7S, '[#ONT(disagree)]')
df.add_user_transition(State.TURNPF6U, State.TURNPF7AS, '[#ONT(teams)]') #case where user inputs another player
df.set_error_successor(State.TURNPF6U, State.TURNTRADE0AS)


# Error succ for PF6U
# PF7S transitions into trade turns
df.add_system_transition(State.TURNPF7AS, State.TURNTRADE0U, r'[! #nicknameToPlayer #teamPlayerCheck #GATE(sameTeam:yes) "Oh, he is pretty good too. Hopefully he and " $favSysPlayer " will lead the "$favSysTeam " to a victory. earlier in the season" #tradeNewsByTeam() " What do you think about" $player "?"]')
df.add_system_transition(State.TURNPF7AS, State.TURNTRADE0AU, r'[! #nicknameToPlayer #teamPlayerCheck #GATE(sameTeam:no) "Huh, I dont think thats a player on the" $favSysTeam'
                                                          r'". Going back to the teams, earlier in the season" #tradeNewsByTeam() " What do you think about" $player "?"]')
df.add_system_transition(State.TURNPF7S, State.TURNTRADE0U, r'[! "Glad to see you agree with me. Going back to the teams, earlier in the season" #tradeNewsByTeam() " What do you think about" $player "?"]')
df.add_system_transition(State.TURNPF7S1, State.TURNTRADE0U, r'[! "Hmm okay, lets agree to disagree for now and wait until the playoffs actually start! '
                                                             r'Focusing back on the teams though, earlier in the season" #tradeNewsByTeam() " What do you think about" $player "?"]')
df.add_system_transition(State.TURNPF7BS, State.TURNTRADE0U, r'[! "There certainly are many good players on " $favSysTeam ". But back to the teams, earlier in the season" #tradeNewsByTeam() " What do you think about" $player "?"]')

"""trades turns"""
#turn 0
#TURNPF5S comes from the idk scenario. will probably need to add in some things to engage more with user response, this is generic catcher
df.add_system_transition(State.TURNTRADE0AS, State.TURNTRADE0U, r'[! "I see. Speaking about the teams, earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]') #I heard that" $receivingTeam "had traded for " $player ". Do you think that trade had repercussions for playoffs?"]')
df.add_system_transition(State.TURNTRADE0S, State.TURNTRADE0U, r'[! "I have also heard my robot uncle say that about his " $playerRationale ". Speaking about the teams, earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about "$player "?"]')
df.add_system_transition(State.TURNTRADE0BS, State.TURNTRADE0U, r'[! "Great minds think alike!. Speaking about the teams, earlier in the season I heard that" {#tradeNewsByTeam()} ". What do you think about " $player "?"]')
df.add_user_transition(State.TURNTRADE0U, State.TURNTRADE1S, "[$userTradePlayerOpinion=#ONT(adjPositive)]") #todo insert rationale here
df.add_user_transition(State.TURNTRADE0U, State.TURNTRADE1S1, "[$userTradePlayerOpinion=#ONT(adjNegative)]") #todo insert rationale here
df.add_user_transition(State.TURNTRADE0U, State.TURN0DK1S, dont_know)
#have these duplicate TRADE0AU so the Gate macro in 6PF can function properly - Anthony
df.add_user_transition(State.TURNTRADE0AU, State.TURNTRADE1S, "[$userTradePlayerOpinion=#ONT(adjPositive)]") #todo insert rationale here
df.add_user_transition(State.TURNTRADE0AU, State.TURNTRADE1S1, "[$userTradePlayerOpinion=#ONT(adjNegative)]") #todo insert rationale here
df.add_user_transition(State.TURNTRADE0AU, State.TURN0DK1S, dont_know)

df.add_user_transition(State.TURNTRADE0U, State.TURNTRADE1S_GEN, '[$userOpinionTradePlayerGen=[/.*/] #NOT(#ONT(adjPositive),#ONT(adjNegative))]')
df.add_user_transition(State.TURNTRADE0AU, State.TURNTRADE1S_GEN, '[$userOpinionTradePlayerGen=[/.*/] #NOT(#ONT(adjPositive),#ONT(adjNegative))]')
df.add_system_transition(State.TURNTRADE1S_GEN, State.TURNTRADE2U, r'[! #sentiAnalyserTradePlayer "." #playerRating() " Do you think that trade influenced how the " $receivingTeam " performed this season?"]')
# Error succ for 0U
df.set_error_successor(State.TURNTRADE0U, State.TURNTRADE0ERR)
df.add_system_transition(State.TURNTRADE0ERR, State.TURNTRADE2U, r'[! "I have heard that from my robot uncle too. Do you think that trade influenced how the " $receivingTeam " performed this season?"]')

# transitions from 1S-esque
df.add_system_transition(State.TURNTRADE1S, State.TURNTRADE2U, r'[! "So you think " $player " is aight. " #playerRating() " Do you think that trade influenced how the " $receivingTeam " performed this season?"]') #todo add onto Macro to indicate the bot agrees/disagrees
df.add_system_transition(State.TURNTRADE1S1, State.TURNTRADE2U, r'[! "So you think " $player " is bad. " #playerRating() " Do you think that trade influenced how the " $receivingTeam " performed this season?"]')
df.add_system_transition(State.TURN0DK1S, State.TURNTRADE2U, r'[! "No worries, if you are not sure I can" {just talk about,give,talk to you about} "my opinions! I think " #playerRating() ". Do you think that trade affected how the " $receivingTeam " seeded into playoffs?"]')
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE3BS, '[$playerImpact=#ONT(disagree)]')
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE3AS, '[$playerImpact=#ONT(agree)]')
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE3CS, dont_know)

# Error Succ for 2U
df.set_error_successor(State.TURNTRADE2U, State.TURNTRADE2ERR)
df.add_system_transition(State.TURNTRADE2ERR, State.TURNTRADE3U, r'[! "That is true too. I think it is hard to tell the impact of a trade because there are player intangibles such as personality which play a big role. Do you think the players would have let the trade impact their playoff mentality?"]')

df.add_system_transition(State.TURNTRADE3AS, State.TURNTRADE3U, r'[! #positiveSeedingImpact() ". Do you think he will play a big role in getting the " $receivingTeam "to playoffs next year?"]')
df.add_system_transition(State.TURNTRADE3BS, State.TURNTRADE3U, r'[! #negativeSeedingImpact() ". Do you think he will play a big role in getting the " $receivingTeam "to playoffs next year?"]')
df.add_system_transition(State.TURNTRADE3CS, State.TURNTRADE3U, r'[! Yeah I am a little uncertain myself too because I feel like player personality plays a big role in how they influence a team. Do you think he will have a big role on the team next year?"]')

df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE5AS, '[#ONT(agree)]')
df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE5BS, '[#ONT(disagree)]')
df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE5CS, dont_know) #dont_know
df.set_error_successor(State.TURNTRADE3U, State.TURNTRADE3UERR)
df.add_system_transition(State.TURNTRADE3UERR, State.TURNTRADE5U, r'[! "I guess thats a possibility. But we wouldn’t know for sure since this is just our speculations haha.'
                                                       ' While youre here," {do you want to chat about another trade,would you like to chat about another trade}"?"]')

df.add_system_transition(State.TURNTRADE5AS, State.TURNTRADE5U, r'[! "So you are excited to see him play next year. "#nextYearPlayoffImpact() {Do you want to chat about another trade,would you like to chat about another trade}"?"]')
df.add_system_transition(State.TURNTRADE5BS, State.TURNTRADE5U, r'[! "So you do not have high hopes " #nextYearPlayoffImpact() {Do you want to chat about another trade,would you like to chat about another trade}"?"]')
df.add_system_transition(State.TURNTRADE5CS, State.TURNTRADE5U, r'[! #nextYearPlayoffImpact() "I am a little uncertain too. You can never account for randomness like injuries sidelining players. " {do you want to chat about another trade,would you like to chat about another trade}"?"]')

df.add_user_transition(State.TURNTRADE5U, State.TURNTRADE6AS, "[#ONT(agree)]")
df.add_system_transition(State.TURNTRADE6AS, State.TURNTRADE1U, r'[! "Okay! I found" {another,this other,a new} {trade news, article} "that says that" #tradeNews() "Does that sound interesting?"]')

df.add_user_transition(State.TURNTRADE5U, State.TURNTRADE6BS, "[#ONT(disagree)]")
df.add_system_transition(State.TURNTRADE6BS, State.END, r'[! "Okay, well in that case we can talk again later. Bye!"]')

# Error Succ 5U
df.set_error_successor(State.TURNTRADE5U, State.TURNTRADE5U_ERR)
df.add_system_transition(State.TURNTRADE5U_ERR, State.END, r'[! "Okay, since I didnt get an explicit affirmation, Ill take my leave for now. See you next time!"]')

df.add_user_transition(State.TURNTRADE1U, State.TURNTRADE2S, '[#ONT(agree)]')
df.add_system_transition(State.TURNTRADE2S, State.TURNTRADE0U, r'[! "Okay, then what do you think about" $player "?"]')
df.add_user_transition(State.TURNTRADE1U, State.TURNTRADE1AS, '[#ONT(disagree)]') #goes to talk about a different trade
df.add_system_transition(State.TURNTRADE1AS, State.TURNTRADE1U , r'[! {[! "How about this:"],I found this other trade article.,[! "What about this trade? I heard that"]} {#tradeNews()}]')

# Errpr Succ 1U
df.set_error_successor(State.TURNTRADE1U, State.TURNTRADE1U_ERR)
df.add_system_transition(State.TURNTRADE1U_ERR, State.TURNTRADE0U, r'[! "Okay, I think this trade should be interesting to talk about! What do you think about" $player "?"]')

# TODO: work on errors and more macros, and idks

"""
#turn 1
df.add_system_transition(State.TURNTRADE1S, State.TURNTRADE1U, r'[! "Here is my thought. " #playerRating() " Would you say you can agree?]')
df.add_user_transition(State.TURNTRADE1U, State.TURNTRADE2S, '[#ONT(agree)]')
df.add_user_transition(State.TURNTRADE1U, State.TURNTRADE1BS, '[#ONT(disagree)]')
df.set_error_successor(State.TURNTRADE1U, State.TURNTRADE1ERR)
df.add_system_transition(State.TURNTRADE1ERR, State.TURNTRADE2U, r'[! "so i guess the big question is how do you think this trade will make difference in playoff performance for $receivingTeam ?"]' )

#turn 2
df.add_system_transition(State.TURNTRADE2S, State.TURNTRADE2U, r'[! "how do you think this will impact $receivingTeam and ultimately, would you think they could become a threat to $favUserTeam ?"]') #edge case when the news covers same team as userfavteam
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE3S2, "[$response2=#ONT(badimpact)]")
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE2DK1S, dont_know) # dont knows
df.add_system_transition(State.TURNTRADE2DK1S, State.TURNTRADE3U, r'[! "Its okay if youre not sure! I actually think that " #goodBadTrade() ". Do you agree?"]') #TODO: need to edit
df.set_error_successor(State.TURNTRADE2U, State.TURNTRADE2ERR)
df.add_system_transition(State.TURNTRADE2ERR, State.TURNTRADE3U, r'[! "I dont know why you made that comment about " $player ". I still think that " ' #TODO: need to edit
                                                                 r'#goodBadTrade() ". Do you agree?"]')
#TODO: next transition would be just responding to users opinion and concluding with "you wouldn't know until the playoff starts
#turn 3
df.add_system_transition(State.TURNTRADE3S1, State.TURNTRADE3U, r'[! "My robot uncle thinks " $player " is " $response2 "too. But we cant forget about the teams" #teamStats() ", and I think that " #goodBadTrade() ". Do you agree?"]')
df.add_system_transition(State.TURNTRADE3S2, State.TURNTRADE3U, r'[! "Ultimately, " #goodBadTrade() ". Do you agree?"]')
df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE4S, '[#ONT(agree)]')
df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE4S1, '[#ONT(disagree)]')

df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE3DK1S,ate.TURNTRADE3S1, "[$response2=#ONT(goodimpact)]") # TODO: more variation needed
df.add_user_transition(State.TURNTRADE2U, St dont_know) # dont knows
df.add_system_transition(State.TURNTRADE3DK1S, State.TURNTRADE4U, r'[! "Youre not sure? Thats okay, since its hard to tell. How do you think this trade will affect the playoffs?"]')
df.set_error_successor(State.TURNTRADE3U, State.TURNTRADE3ERR)
df.add_system_transition(State.TURNTRADE3ERR, State.TURNTRADE4U, r'[! "That is certainly an opinion haha. Playoffs are happening soon though! How do you think this trade affects the playoff?"]')

#turn 4
df.add_system_transition(State.TURNTRADE4S1, State.TURNTRADE4U, r'[! "Interesting perspective. Anyway, how do you think this affects the playoff?"]')
df.add_system_transition(State.TURNTRADE4S, State.TURNTRADE4U, r'[! "How do you think this trade will affect the playoffs? "]')
df.add_user_transition(State.TURNTRADE4U, State.TURNTRADE5S, possible_results)

df.add_user_transition(State.TURNTRADE4U, State.TURNTRADE4DK1S, dont_know)
df.add_system_transition(State.TURNTRADE4DK1S, State.TURNTRADE5U, r'[! "Honestly, youre probably right to bunsure as we wont know until playoffs actually start. Do you want to chat about playoffs or another topic?"]')
df.set_error_successor(State.TURNTRADE4U, State.TURNTRADE4ERR)
df.add_system_transition(State.TURNTRADE4ERR, State.TURNTRADE5S, r'[! "Haha, youre funny, but ultimately I guess we wont know until later when playoffs start."]')

df.add_system_transition(State.TURNTRADE5S, State.TURNTRADE5U, r'[! "I guess that is a possibility. We will not know until playoffs actually start. Do you want to chat about playoffs or another topic?"]')
df.add_user_transition(State.TURNTRADE5U, State.END, '[$watching={#ONT(agree)}]')
"""
if __name__ == '__main__':
    df.run(debugging=args.debug)
