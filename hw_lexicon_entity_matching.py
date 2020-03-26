from emora_stdm import KnowledgeBase, DialogueFlow, Macro
from enum import Enum, auto
import requests
import json
from sportsreference.nba.schedule import Schedule
from sportsreference.nba.roster import Player


# TODO: Update the State enum as needed
class State(Enum):
    START = auto()
    TURN0 = auto()
    TURN0ERR = auto()
    TURNTRADE1S = auto()
    TURNTRADE1U = auto()
    TURNTRADE1ERR = auto()
    TURNTRADE1BS = auto()
    TURNTRADE1BU = auto()
    TURNTRADE2S = auto()
    TURNTRADE2U = auto()
    TURNTRADE2AS = auto()
    TURNTRADE2AU = auto()
    TURNTRADE2ERR = auto()
    TURNTRADE3S = auto()
    TURNTRADE3U = auto()
    TURNTRADE3ERR = auto()
    TURNTRADE4S = auto()
    TURNTRADE4U = auto()
    TURNTRADE4ERR = auto()
    TURNTRADE5U = auto()
    TURNTRADE5S = auto()
    END = auto()
    EARLYEND = auto()


# ONTOLOGY IS LOADED FROM teams.json
ontology = {
    "ontology": {

        }
}

#GLOBAL VARS????
receivingTeam = str()
givingTeam = str()
player = str()

class news(Macro):
    def run (self, ngrams, vars, args):
        #andrew- im just gonna assume that the input is the team name and only the team name, eg "Atlanta Hawks"

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
        #andrew- im just gonna assume that the input is the team name and only the team name, eg "Atlanta Hawks"

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

        if vars['receivingTeam'] == "Atlanta Hawks" or "Atlanta" or "Hawks":
            team = 'ATL'
        elif vars['receivingTeam'] == "Boston Celtics" or "Boston" or "Celtics":
            team = 'BOS'
        elif vars['receivingTeam'] == "Brooklyn Nets" or "Brooklyn" or "Nets":
            team = 'BKN'
        elif vars['receivingTeam'] =="Charlotte Hornets" or "Charlotte" or "Hornets":
            team = 'CHA'
        elif vars['receivingTeam'] =="Chicago Bulls" or "Chicago" or "Bulls":
            team = 'CHI'
        elif vars['receivingTeam'] =="Cleveland Cavaliers" or "Cleveland" or "Cavaliers":
            team = 'CLE'
        elif vars['receivingTeam'] =="Dallas Mavericks" or "Dallas" or "Mavericks":
            team = 'DAL'
        elif vars['receivingTeam'] =="Denver Nuggets" or "Denver" or "Nuggets":
            team = 'DEN'
        elif vars['receivingTeam'] =="Detroit Pistons" or "Detroit" or "Pistons":
            team = 'DET'
        elif vars['receivingTeam'] =="Golden State Warriors" or "GSW" or "Warriors":
            team = 'GSW'
        elif vars['receivingTeam'] =="Houston Rockets" or "Houston" or "Rockets":
            team = 'HOU'
        elif vars['receivingTeam'] =="Indiana Pacers" or "Indiana" or "Pacers":
            team = 'IND'
        elif vars['receivingTeam'] =="LA Clippers" or "Clippers":
            team = 'LAC'
        elif vars['receivingTeam'] =="Los Angeles Lakers" or "Lakers":
            team = 'LAL'
        elif vars['receivingTeam'] =="Memphis Grizzlies" or "Memphis" or "Grizzlies":
            team = 'MEM'
        elif vars['receivingTeam'] =="Miami Heat" or "Miami":
            team = 'MIA'
        elif vars['receivingTeam'] =="Milwaukee Bucks" or "Milwaukee" or "Bucks":
            team = 'MIL'
        elif vars['receivingTeam'] =="Minnesota Timberwolves" or "Minnesota" or "Timberwolves":
            team = 'MIN'
        elif vars['receivingTeam'] =="New Orleans Pelicans" or "Pelicans" or "NoLa":
            team = 'NOP'
        elif vars['receivingTeam'] =="New York Knicks" or "Knicks" or "NY":
            team = 'NYK'
        elif vars['receivingTeam'] =="Oklahoma City Thunder" or "Thunder" or "OKC":
            team = 'OKC'
        elif vars['receivingTeam'] =="Orlando Magic" or "Orlando" or "Magic":
            team = 'ORL'
        elif vars['receivingTeam'] =="Philadelphia SeventySixers" or "Philly" or "SeventySixers" or "76ers":
            team = 'PHI'
        elif vars['receivingTeam'] =="Phoenix Suns" or "Phoenix" or "Suns":
            team = 'PHX'
        elif vars['receivingTeam'] =="Portland Trail Blazers" or "Portland" or "Trail Blazers":
            team = 'POR'
        elif vars['receivingTeam'] =="Sacramento Kings" or "Sacramento" or "Kings":
            team = 'SAC'
        elif vars['receivingTeam'] =="San Antonio Spurs" or "San Antonio" or "Spurs":
            team = 'SAS'
        elif vars['receivingTeam'] =="Toronto Raptors" or "Toronto" or "Raptors":
            team = 'TOR'
        elif vars['receivingTeam'] =="Utah Jazz" or "Utah" or "Jazz":
            team = 'UTA'
        elif vars['receivingTeam'] =="Washington Wizards" or "Washington" or "Wizards":
            team = 'WAS'
        else:
            #error handling? idk if needed
            return "I didn't get that"

        wins = 0
        losses = 0
        teamSchedule = Schedule(team)
        for game in teamSchedule:
            if game.result == 'Win':
                wins += 1
            else:
                losses += 1

        return "The {} have a total of {} wins and {} losses".format(vars['worseTeam'], wins, losses)

class tradeNews(Macro):
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
        
        #print(trade)
        #print('recieving team', receivingTeam)
        #print('givingTeam', givingTeam)
        #print(player)
        #print(role)

        return "I found this most recent trade for {} between the {} and {}".format(player, givingTeam, receivingTeam)

class worseTeam(Macro):
    def run (self, ngrams, vars, args):

        response = requests.get("https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json")
        test = response.json()
        trades = [x for x in test['NBA_Player_Movement']['rows'] if x['Transaction_Type'] == 'Trade']
        trade = trades[0]['TRANSACTION_DESCRIPTION']
        receivingTeam = trade.split(' received')[0]
        givingTeam = trade.split('from ')[1]
        givingTeam = givingTeam[:-1]
        print('givingTeam', givingTeam)

        receiving_giving = [receivingTeam, givingTeam]
        receive_give_codes = []
        for team in receiving_giving:
            if team in ["Atlanta Hawks", "Atlanta", "Hawks"]:
                receive_give_codes.append('ATL')
            elif team in ["Boston Celtics", "Boston", "Celtics"]:
                receive_give_codes.append('BOS')
            elif team in ["Brooklyn Nets", "Brooklyn", "Nets"]:
                receive_give_codes.append('BKN')
            elif team in ["Charlotte Hornets", "Charlotte",  "Hornets"]:
                receive_give_codes.append('CHA')
            elif team in ["Chicago Bulls", "Chicago", "Bulls"]:
                receive_give_codes.append('CHI')
            elif team in ["Cleveland Cavaliers", "Cleveland", "Cavaliers"]:
                receive_give_codes.append('CLE')
            elif team in ["Dallas Mavericks", "Dallas", "Mavericks"]:
                receive_give_codes.append('DAL')
            elif team in ["Denver Nuggets", "Denver", "Nuggets"]:
                receive_give_codes.append('DEN')
            elif team in ["Detroit Pistons", "Detroit", "Pistons"]:
                receive_give_codes.append('DET')
            elif team in ["Golden State Warriors", "GSW", "Warriors"]:
                receive_give_codes.append('GSW')
            elif team in ["Houston Rockets", "Houston", "Rockets"]:
                receive_give_codes.append('HOU')
            elif team in ["Indiana Pacers", "Indiana", "Pacers"]:
                receive_give_codes.append('IND')
            elif team in ["LA Clippers", "Clippers"]:
                receive_give_codes.append('LAC')
            elif team in ["Los Angeles Lakers", "Lakers"]:
                receive_give_codes.append('LAL')
            elif team in ["Memphis Grizzlies", "Memphis", "Grizzlies"]:
                receive_give_codes.append('MEM')
            elif team in ["Miami Heat", "Miami"]:
                receive_give_codes.append('MIA')
            elif team in ["Milwaukee Bucks", "Milwaukee", "Bucks"]:
                receive_give_codes.append('MIL')
            elif team in ["Minnesota Timberwolves", "Minnesota", "Timberwolves"]:
                receive_give_codes.append('MIN')
            elif team in ["New Orleans Pelicans", "Pelicans", "NoLa"]:
                receive_give_codes.append('NOP')
            elif team in ["New York Knicks", "Knicks", "NY"]:
                receive_give_codes.append('NYK')
            elif team in ["Oklahoma City Thunder", "Thunder", "OKC"]:
                receive_give_codes.append('OKC')
            elif team in ["Orlando Magic", "Orlando", "Magic"]:
                receive_give_codes.append('ORL')
            elif team in ["Philadelphia SeventySixers", "Philly", "SeventySixers", "76ers"]:
                receive_give_codes.append('PHI')
            elif team in ["Phoenix Suns", "Phoenix", "Suns"]:
                receive_give_codes.append('PHX')
            elif team in ["Portland Trail Blazers", "Portland", "Trail Blazers"]:
                receive_give_codes.append('POR')
            elif team in ["Sacramento Kings", "Sacramento", "Kings"]:
                receive_give_codes.append('SAC')
            elif team in ["San Antonio Spurs", "San Antonio", "Spurs"]:
                receive_give_codes.append('SAS')
            elif team in ["Toronto Raptors", "Toronto", "Raptors"]:
                receive_give_codes.append('TOR')
            elif team in ["Utah Jazz", "Utah", "Jazz"]:
                receive_give_codes.append('UTA')
            elif team in ["Washington Wizards", "Washington", "Wizards"]:
                receive_give_codes.append('WAS')
            else:
                receive_give_codes.append('')

        win_loss = list()

        print('recieve_give_codes', receive_give_codes)
        for team in receive_give_codes:
            wins = 0
            losses = 0
            teamSchedule = Schedule(team)
            for game in teamSchedule:
                if game.result == 'Win':
                    wins += 1
                else:
                    losses += 1
            win_loss.append(wins/losses)

        # x is the receiving team
        # y is the giving team
        for x,y in zip(win_loss, win_loss[1:]):
            if x >= y: # if receiving team has the better W-L ratio, then the giving team is the worse team
                vars['worseTeam'] = givingTeam
                return "{}".format(givingTeam)
            else:
                vars['worseTeam'] = receivingTeam
                return "{}".format(receivingTeam)


class playerRating(Macro):
    def run (self, ngrams, vars, args):
        n = vars['player'].split()
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
        PER = player.player_efficiency_rating
        if (PER > 18): return "good player. I think this trade will go great"
        else: return "bad player. I don't have high hopes for this trade"


#returns name of team which has better W/L ratio
class betterTeam(Macro):
    def run (self, ngrams, vars, args):

        response = requests.get("https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json")
        test = response.json()
        trades = [x for x in test['NBA_Player_Movement']['rows'] if x['Transaction_Type'] == 'Trade']
        trade = trades[0]['TRANSACTION_DESCRIPTION']
        receivingTeam = trade.split(' received')[0]
        givingTeam = trade.split('from ')[1]
        givingTeam = givingTeam[:-1]
        print('givingTeam', givingTeam)

        receiving_giving = [receivingTeam, givingTeam]
        receive_give_codes = []
        for team in receiving_giving:
            if team in ["Atlanta Hawks", "Atlanta", "Hawks"]:
                receive_give_codes.append('ATL')
            elif team in ["Boston Celtics", "Boston", "Celtics"]:
                receive_give_codes.append('BOS')
            elif team in ["Brooklyn Nets", "Brooklyn", "Nets"]:
                receive_give_codes.append('BKN')
            elif team in ["Charlotte Hornets", "Charlotte",  "Hornets"]:
                receive_give_codes.append('CHA')
            elif team in ["Chicago Bulls", "Chicago", "Bulls"]:
                receive_give_codes.append('CHI')
            elif team in ["Cleveland Cavaliers", "Cleveland", "Cavaliers"]:
                receive_give_codes.append('CLE')
            elif team in ["Dallas Mavericks", "Dallas", "Mavericks"]:
                receive_give_codes.append('DAL')
            elif team in ["Denver Nuggets", "Denver", "Nuggets"]:
                receive_give_codes.append('DEN')
            elif team in ["Detroit Pistons", "Detroit", "Pistons"]:
                receive_give_codes.append('DET')
            elif team in ["Golden State Warriors", "GSW", "Warriors"]:
                receive_give_codes.append('GSW')
            elif team in ["Houston Rockets", "Houston", "Rockets"]:
                receive_give_codes.append('HOU')
            elif team in ["Indiana Pacers", "Indiana", "Pacers"]:
                receive_give_codes.append('IND')
            elif team in ["LA Clippers", "Clippers"]:
                receive_give_codes.append('LAC')
            elif team in ["Los Angeles Lakers", "Lakers"]:
                receive_give_codes.append('LAL')
            elif team in ["Memphis Grizzlies", "Memphis", "Grizzlies"]:
                receive_give_codes.append('MEM')
            elif team in ["Miami Heat", "Miami"]:
                receive_give_codes.append('MIA')
            elif team in ["Milwaukee Bucks", "Milwaukee", "Bucks"]:
                receive_give_codes.append('MIL')
            elif team in ["Minnesota Timberwolves", "Minnesota", "Timberwolves"]:
                receive_give_codes.append('MIN')
            elif team in ["New Orleans Pelicans", "Pelicans", "NoLa"]:
                receive_give_codes.append('NOP')
            elif team in ["New York Knicks", "Knicks", "NY"]:
                receive_give_codes.append('NYK')
            elif team in ["Oklahoma City Thunder", "Thunder", "OKC"]:
                receive_give_codes.append('OKC')
            elif team in ["Orlando Magic", "Orlando", "Magic"]:
                receive_give_codes.append('ORL')
            elif team in ["Philadelphia SeventySixers", "Philly", "SeventySixers", "76ers"]:
                receive_give_codes.append('PHI')
            elif team in ["Phoenix Suns", "Phoenix", "Suns"]:
                receive_give_codes.append('PHX')
            elif team in ["Portland Trail Blazers", "Portland", "Trail Blazers"]:
                receive_give_codes.append('POR')
            elif team in ["Sacramento Kings", "Sacramento", "Kings"]:
                receive_give_codes.append('SAC')
            elif team in ["San Antonio Spurs", "San Antonio", "Spurs"]:
                receive_give_codes.append('SAS')
            elif team in ["Toronto Raptors", "Toronto", "Raptors"]:
                receive_give_codes.append('TOR')
            elif team in ["Utah Jazz", "Utah", "Jazz"]:
                receive_give_codes.append('UTA')
            elif team in ["Washington Wizards", "Washington", "Wizards"]:
                receive_give_codes.append('WAS')
            else:
                receive_give_codes.append('')

        win_loss = list()

        print('recieve_give_codes', receive_give_codes)
        for team in receive_give_codes:
            wins = 0
            losses = 0
            teamSchedule = Schedule(team)
            for game in teamSchedule:
                if game.result == 'Win':
                    wins += 1
                else:
                    losses += 1
            win_loss.append(wins/losses)

        # x is the receiving team
        # y is the giving team
        for x,y in zip(win_loss, win_loss[1:]):
            if x <= y: # if receiving team has a worse win loss ratio, then they are the worse team and giving team is the better team
                return "{}".format(givingTeam)
            else:
                return "{}".format(receivingTeam)

knowledge = KnowledgeBase()
knowledge.load_json_file("teams.json")
df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.SYSTEM, kb=knowledge, macros={'news': news(), 'newsPlayer': newsPlayer(), 'newsTeam': newsTeam(), 'teamStats': teamStats(), 'playerRating' : playerRating(), 'worseTeam' : worseTeam(), 'tradeNews':tradeNews()})

#########################
# THIS DOCUMENT IS THE SOURCE OF TRUTH FOR WHAT WE ARE DOING: https://docs.google.com/document/d/15N6Xo60IipqOknUGHxXt-A17JFOXOhMCZSMcOAyUEzo/edit
##########################

#turn 0
df.add_system_transition(State.START, State.TURN0, '"Hi I’m NBA chatbot. I can talk to you about trades, injuries, drafts, or all-stars. Which of these would you like to talk about?"')
df.add_user_transition(State.TURN0, State.TURNTRADE1S, '[#ONT(trades)]')
df.set_error_successor(State.TURN0, State.TURN0ERR) #todo test if we want category which is NOT trades
df.add_system_transition(State.TURN0ERR, State.TURN0, r'[! "I do not know how to talk about that yet"]')
#df.add_system_transition(State.TURNTRADE1S2, State.EARLYEND, r'[! "Oh, thats a shame. I cant really talk about other news right now unfortunately. Maybe next time we can talk some more"]')


#turn 1
df.add_system_transition(State.TURNTRADE1S, State.TURNTRADE1U, r'[!{#tradeNews()} ". Do you want to talk aobut this trade?"]')
df.add_user_transition(State.TURNTRADE1U, State.TURNTRADE2S, '[#ONT(agree)]')
df.add_user_transition(State.TURNTRADE1U, State.TURNTRADE1BS, '[#ONT(disagree)]')
df.add_system_transition(State.TURNTRADE1BS, State.TURNTRADE1BU, r'[! "We can also talk about all-stars, injuries, the draft, or stop talking. Which would you prefer?"]')
df.add_user_transition(State.TURNTRADE1BU, State.END, '[/[a-z A-Z]+/]')
df.set_error_successor(State.TURNTRADE1U, State.TURNTRADE1ERR)
df.add_system_transition(State.TURNTRADE1ERR, State.TURNTRADE2U, r'[! "Do not know if I want to talk about trades or about something else"]' )

#turn 2

if player is good and receivingTeam is worseTeam:
    print('This helps the worseTeam')

if player is bad and receivingTeam is worseTeam:
    print('This helps the givingTeam')


df.add_system_transition(State.TURNTRADE2S, State.TURNTRADE2U, r'[! #teamStats() "Personally I think this will help" #worseTeam() ". Do you think it will?"]')
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE2AS, '[{#ONT(disagree)}]')
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE3S, '[{#ONT(agree)}]')
df.set_error_successor(State.TURNTRADE2U, State.TURNTRADE2ERR)
df.add_system_transition(State.TURNTRADE2ERR, State.TURNTRADE3U, r'[! "Do not know if it will help the worse team"]')

#turn 3
df.add_system_transition(State.TURNTRADE3S, State.TURNTRADE3U, r'[! ". When I watch " $player ", I feel like they are a " #playerRating() ". What do you think about " $player "?"]')
df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE4S, "[$response2=#POS(adj)]")
df.set_error_successor(State.TURNTRADE3U, State.TURNTRADE3ERR)
df.add_system_transition(State.TURNTRADE3ERR, State.TURNTRADE4U, "Do not know if it will boost win loss record.")

#turn 4
df.add_system_transition(State.TURNTRADE4S, State.TURNTRADE4U, r'[! "If this ends up being a good thing, it could change the playoff picture. Do you think it will? "]')
df.add_user_transition(State.TURNTRADE4U, State.TURNTRADE5S, "[$response3=/[a-z A-Z]+/]")
df.set_error_successor(State.TURNTRADE4U, State.TURNTRADE4ERR)
df.add_system_transition(State.TURNTRADE4ERR, State.TURNTRADE4S, "Do not have a playoff prediction")

df.add_system_transition(State.TURNTRADE5S, State.TURNTRADE5U, r'[! "I guess that is a possibility. We will not know until playoffs actually start. Do you want to chat about playoffs or another topic?"]')
df.add_user_transition(State.TURNTRADE5U, State.END, '[$watching={#ONT(agree)}]')




if __name__ == '__main__':
    df.run(debugging=True)