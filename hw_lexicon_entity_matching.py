from emora_stdm import KnowledgeBase, DialogueFlow, Macro
from enum import Enum, auto
import requests
from sportsreference.nba.schedule import Schedule
from sportsreference.nba.roster import Player
import json
from random import randrange

# TODO: Update the State enum as needed
class State(Enum):
  #states for trade conversation
    START = auto()
    TURN0 = auto()
    TURNTRADE0S = auto()
    TURNTRADE0U = auto()
    TURN0DK1S = auto()
    TURN0DK1U = auto()
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
    TURNTRADE2DK1S = auto()
    TURNTRADE2ERR = auto()
    TURNTRADE3S1 = auto()
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
    
    #states for playoff conversation
    TURNPF1S = auto()
    TURNPF1U = auto()
    TURNPF1ERR = auto()
    TURNPF2AS = auto()
    TURNPF2AU = auto()
    TURNPF2BS = auto()
    TURNPF2BS1 = auto()
    TURNPF2BU1 = auto()
    TURNPF2BU = auto()
    TURNPF2CS = auto()
    TURNPF2ERR = auto()
    TURNPF2AERR = auto()
    TURNPF2BU_ERR1 = auto()
    TURNPF2BU_ERR2= auto()
    TURNPF3AS = auto()
    TURNPF3AERR = auto()
    TURNPF3BS = auto()
    TURNPF3CS = auto()
    TURNPF3DS = auto()
    TURNPF3AU = auto()
    TURNPF3U = auto()
    TURNPF3ERR = auto()
    TURNPF4S = auto()
    TURNPF5S = auto()
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
        
        #print(trade)
        #print('recieving team', receivingTeam)
        #print('givingTeam', givingTeam)
        #print(player)
        #print(role)

        return "I found this most recent trade news that {} from {} is going to {}".format(player, givingTeam, receivingTeam)

class tradeNews(Macro):
    def run (self, ngrams, vars, args):
        with open('trades.json') as f:
            data = json.load(f)
        trades = data['trades']
        trade = trades[randrange(55)]['TRANSACTION_DESCRIPTION']
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

        return "I found this most recent trade news that {} from {} is going to {}".format(player, givingTeam, receivingTeam)


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
                vars['favSysTeam'] = 'Bucks'
                vars['favSysPlayer'] = 'Giannis Antetokounmpo'
                vars['favSysPlayerPER'] = 31.71
                vars['favSysPlayerPTS'] = 29.6
                vars['favSysPlayerREB'] = 13.7
                vars['favSysPlayerAST'] = 5.8
                return

        if 'favUserTeam' in vars:
            if vars['favUserTeam'] in 'milwaukee bucks' or vars['favUserTeam'] in 'bucks' or vars['favUserTeam'] in 'milwaukee':
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
        if (PER > 18):
            vars['goodBadPlayer'] = 'good'
            return "I get the impression that he is efficient and good player. With more opportunities, he may be even better. I think this trade will go great."
        else:
            vars['goodBadPlayer'] = 'bad'
            return "I don't get the impression that he is good. This could just be me, but he doesn't seem too efficient."

class comparePlayers(Macro):
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
        PER = player.player_efficiency_rating
        PTS = player.points/player.games_played
        REB = player.total_rebounds/player.games_played
        AST = player.assists/player.games_played
        ## COMPARE WITH HARDCODED STATS OF SYSTEM's FAV PLAYER- still not sure how much of this should be generated by the turns and how much of this should be generated by the macro
        
        ##PER was not mentioned so idk if its something we want to add
        if PTS > 20 or AST > 8 or REB > 10:
            return "I see {} is having an exceptional season. Personally, I think {} will win because of {}".format(vars['favUserPlayer'], vars['favSysTeam'], vars['favSysPlayer'])
        return "Interesting you like {} because he is not that great satistically. Personally, I think {} will win because of {}".format(vars['favUserPlayer'], vars['favSysTeam'], vars['favSysPlayer'])

knowledge = KnowledgeBase()
knowledge.load_json_file("teams.json")
df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.SYSTEM, kb=knowledge, macros={'news': news(), 'newsPlayer': newsPlayer(), 'newsTeam': newsTeam(),
                                                                                                  'teamStats': teamStats(), 'playerRating' : playerRating(),
                                                                                                  'goodBadTrade' : goodBadTrade(), 'tradeNews':tradeNews(),
                                                                                                  'botFavTeam': botFavTeam()})

#########################
# THIS DOCUMENT IS THE SOURCE OF TRUTH FOR WHAT WE ARE DOING: https://docs.google.com/document/d/15N6Xo60IipqOknUGHxXt-A17JFOXOhMCZSMcOAyUEzo/edit
##########################

# natex expressions
dont_know = '[{' \
            'dont know,do not know,unsure,maybe,[not,{sure,certain}],hard to say,no idea,uncertain,i guess,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[{dont,do not}, have, {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[!{cant,cannot,dont} {think,remember,recall}]' \
            '}]'

possible_results = '[{' \
                   'better,worse,obliterate,crush,destroy,change,effect,difference,improve,adjust,adapt,implications,good,bad,weird' \
                   '}]'

"""playoffs turns"""
#turn 1
df.add_system_transition(State.START, State.TURNPF1U, r'[! "Hi I am NB chatbot. The NBA season has been shutdown because of COVID. If we played playoffs based off the current standings, which team do you think would win?"]')
df.add_user_transition(State.TURNPF1U, State.TURNPF2AS, dont_know)
df.add_user_transition(State.TURNPF1U, State.TURNPF2CS, '[#ONT(nonplayoffteams)]')
df.add_user_transition(State.TURNPF1U, State.TURNPF2BS, '[$favUserTeam=#ONT(playoffteams)]')
df.set_error_successor(State.TURNPF1U, State.TURNPF1ERR)
df.add_system_transition(State.TURNPF1ERR, State.TURNPF2AS, 'Picking userTeam')


#idk scenario 
df.add_system_transition(State.TURNPF2CS, State.TURNPF2AU, r'[! #botFavTeam "I dont think that team will be in the playoffs. But you know, I think that " $favSysTeam " can win. Do you agree?"]')
df.add_system_transition(State.TURNPF2AS, State.TURNPF2AU, r'[! #botFavTeam "It is okay to be unsure because predictability of playoffs is difficult without more data. I think that " $favSysTeam " can win. Do you agree?"]')
df.add_user_transition(State.TURNPF2AU, State.TURNPF3AS, '[#ONT(agree)]')
df.add_user_transition(State.TURNPF2AU, State.TURNPF3BS, '[#ONT(disagree)]')
df.set_error_successor(State.TURNPF2AU, State.TURNPF2AERR)
df.add_system_transition(State.TURNPF2AERR, State.TURNPF3AS, 'uncertain about playoff team')

df.add_system_transition(State.TURNPF3AS, State.TURNPF3AU, r'[! "I always love meeting other fans of " $favSysTeam " Why do you think " $favSysTeam " is going to win?"]')
df.add_system_transition(State.TURNPF3BS, State.TURNPF3AU, r'[! "Why do you think " $favSysTeam " will not win?"]')
df.add_user_transition(State.TURNPF3AU, State.TURNPF4S, '[/[a-z A-Z]+/]') #pull any response here
df.add_system_transition(State.TURNPF4S, State.TURNPF5S, r'[! "That is a good opinion. Personally, I think " $favSysTeam "will win because of " $favSysPlayer ". What do you think of " #comparePlayer]') #todo modify comparePlayer to work with either sysplayer or userplayer
#df.set_error_successor(State.TURNPF3AU, State.TURNPF3AERR)
#df.add_system_transition(State.TURNPF3AERR, State.TURN)

# Playoff Turn 2 (not idk scenario)
df.add_system_transition(State.TURNPF2BS, State.TURNPF2BU, r'[! #botFavTeam "Why do you think" $favUserTeam "will win?"]')
df.add_user_transition(State.TURNPF2BU, State.TURNPF2BS1, '[$rationale=[#ONT(rationale)]]') # hopefully we can pick up rationales
df.set_error_successor(State.TURNPF2BU, State.TURNPF2BU_ERR2)
df.add_system_transition(State.TURNPF2BU_ERR2, State.TURNPF3U, r'[! "Thats fair. Personally, I think that" $favSysTeam "has the best chance of winning because of" $favSysPlayer]') #todo make sure this transition goes into the correct user transition

df.add_system_transition(State.TURNPF2BS1, State.TURNPF2BU1, r'[! "Do you think theres a player that is integral to their team?"]')
df.add_user_transition(State.TURNPF2BU1, State.TURNPF3CS, "[$favUserPlayer=[#ONT(playoffteams)]]") #todo make ontology for players who are in and not in playoffs
df.set_error_successor(State.TURNPF2BU1, State.TURNPF2BU_ERR2)

#df.add_system_transition(State.TURNPF2BU_ERR2, State.TURNPFU, r'[! "Thats fair. Personally, I think that" $favSysTeam "has the best chance of winning because of" $favSysPlayer]')

# Playoff Turn 3
df.add_system_transition(State.TURNPF3CS, State.TURNPF3U, r'[! "I think that " #comparePlayers ". What is your opinion?]')
df.add_user_transition(State.TURNPF3U, State.TURNTRADE0S, "[#ONT(actions)]")



"""trades turns"""
#turn 0
#need to run trade macro up here to get the trades specific to teams
df.add_system_transition(State.TURNTRADE0S, State.TURNTRADE0U, r'[! "Earlier in the season I heard that" $receivingTeam "had traded for " $player ". Do you think that trade had repercussions for playoffs?"]')
df.add_user_transition(State.TURNTRADE0S, State.TURN0DK1S, dont_know) # dont knows section
df.add_system_transition(State.TURN0DK1S, State.TURN0DK1U, r'[! "No worries, if you dont know, I can just talk about trades! Is that okay?"]')
df.add_user_transition(State.TURN0DK1U, State.TURNTRADE1S, "[#ONT(agree)]")
df.set_error_successor(State.TURN0DK1U, State.TURN0ERR)

df.add_system_transition(State.TURN0ERR, State.TURN0, r'[! "I do not know how to talk about that yet"]')
df.set_error_successor(State.TURN0, State.TURN0ERR)
df.add_system_transition(State.TURN0ERR, State.TURNTRADE1U, r'[! "Honestly, Im only really good at talking about trades right now. If thats okay then listen to this! " #tradeNews() ". Doesnt that sound interesting?"]')
#df.add_system_transition(State.TURNTRADE1S2, State.EARLYEND, r'[! "Oh, thats a shame. I cant really talk about other news right now unfortunately. Maybe next time we can talk some more"]')


#turn 1
df.add_system_transition(State.TURNTRADE1S, State.TURNTRADE1U, r'[!{#tradeNews()} ". Do you want to talk about this trade?"]')
df.add_user_transition(State.TURNTRADE1U, State.TURNTRADE2S, '[#ONT(agree)]')
df.add_user_transition(State.TURNTRADE1U, State.TURNTRADE1BS, '[#ONT(disagree)]')
df.add_system_transition(State.TURNTRADE1BS, State.TURNTRADE1BU, r'[! "We can also talk about all-stars, injuries, the draft, or stop talking. Which would you prefer?"]')
df.add_user_transition(State.TURNTRADE1BU, State.END, '[/[a-z A-Z]+/]')
df.set_error_successor(State.TURNTRADE1U, State.TURNTRADE1ERR)
df.add_system_transition(State.TURNTRADE1ERR, State.TURNTRADE2U, r'[! "Okay, I mean " $player " is really interesting, and I really want to talk about him. " #playerRating() " What do you think about him?"]' )

#turn 2
df.add_system_transition(State.TURNTRADE2S, State.TURNTRADE2U, r'[! "When I watch " $player ", " #playerRating() " What do you think about " $player "?"]')
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE3S1, "[$response2=#POS(adj)]")
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE3S2, "[$response2=#POS(verb)]")
df.add_user_transition(State.TURNTRADE2U, State.TURNTRADE2DK1S, dont_know) # dont knows
df.add_system_transition(State.TURNTRADE2DK1S, State.TURNTRADE3U, r'[! "Its okay if youre not sure! I actually think that " #goodBadTrade() ". Do you agree?"]')
df.set_error_successor(State.TURNTRADE2U, State.TURNTRADE2ERR)
df.add_system_transition(State.TURNTRADE2ERR, State.TURNTRADE3U, r'[! "I dont know why you made that comment about " $player ". I still think that " '
                                                                 r'#goodBadTrade() ". Do you agree?"]')

#turn 3

df.add_system_transition(State.TURNTRADE3S1, State.TURNTRADE3U, r'[! "My robot uncle thinks " $player " is " $response2 "too. But we cant forget about the teams" #teamStats() ", and I think that " #goodBadTrade() ". Do you agree?"]')
df.add_system_transition(State.TURNTRADE3S2, State.TURNTRADE3U, r'[! "Ultimately, " #goodBadTrade() ". Do you agree?"]')
df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE4S, '[#ONT(agree)]')
df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE4S1, '[#ONT(disagree)]')

df.add_user_transition(State.TURNTRADE3U, State.TURNTRADE3DK1S, dont_know) # dont knows
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


if __name__ == '__main__':
    df.run(debugging=True)