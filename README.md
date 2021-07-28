# NBAchatbot

NBAchatbot is a chatbot designed to talk about the 2019 NBA season. Checkout our [paper](final_paper.pdf)!

## Requirements

Python 3.4+ for the venv module, which comes baked in.

## Installation

Now with a [Makefile](Makefile)! 

Simply run 
```bash
make all
```
to get up and running quickly. `make all` is comprised of `make install`(installs a venv, activates it, and installs the requirements from [requirements.txt](requirements.txt)) and `make run`(runs [chatbotNba.py](chatbotNba.py)).

## Usage

After first install, `make run` will be sufficient to start the chatbot. Happy chatting!

`make clean` will delete the venv.

## Debugging

To enable debugging, manually run `chatbotNba.py` with the `--debug` flag set to `true`
```bash
python3 chatbotNba.py --debug true
```

## Features

1. Player specific rationale: Our bot has two favorite players. Kawhi Leonard and Jimmy Butler. The bot is able to respond to critiques which are specific to the two players. 
   * For Kawhi Leonard, that he is injury prone, for Jimmy Butler that he has bad chemistry with other players.
        
2. Nicknames: We can capture how people naturally talk about players which may include nicknames.  
   * Lbj for lebron james, aquaman for steven adams, or greek freak for Giannis Antetokounmpo.

3. Opinion on each different player changes (player rating macro): Our bot will have different opinions about different players. These are not hardcoded beforehand but pull from the dataset about players and formulates an opinion based on their stats. This also changes in relation to the context the opinion is being sought in.
   * Overall opinion vs opinion of how the player will perform in playoffs. 
   * In conversation #1 our bot has a different opinion for Giannis Antetokounmpo vs Jordan McRae.

4. Engagement with users’ emotions even if sentence isn’t caught by ontology (sentiment analyzer): Bot will indicate to the user that we understand the sentiment of their opinion even if the bot isn’t able to respond to their specific comment. 
   * In conversation #1 we see the user is neutral about Isaiah Thomas.

5. Variation: No two conversations will ever be identical because of variation of responses based on opinions and players mentioned by user throughout the conversation, and also individual changes in each utterance.

## Sample Conversation

```
S: Hi I am NBA chatbot. The NBA season has been put on hold because of COVID-19.  If we had playoffs based off the current standings , which team do you think would win?

U: the bucks will win

S:  Why do you think the bucks will win?

U: they have greek freak # nickname recognition

S:    I see giannis antetokounmpo is having an exceptional season. Personally, I think Clippers will win because Kawhi Leonard is more clutch . Whats your opinion of Kawhi Leonard ?
U: he is too fragile # specific rationale catch for Kawhi Leonard

S: Even though he is fragile  he always  overperforms  in playoffs. Anyways, I saw that Isaiah Thomas  from Washington Wizards went to LA Clippers . What are your thoughts about  Isaiah Thomas  ?

U: i dont have much thoughts

S: Okay, I can tell youre pretty neutral about Isaiah Thomas  . I dont think he is too terrible but he doesnt seem to have a huge impact to the game.  Do you think that trade influenced how the  LA Clippers  performed this season? #Sentiment analyser used as fail-safe error handler for opinions

U: hes probably not going to affect

S: I agree, the trade was early in the season and he has not shown he was worth it . Do you think he will play a big role in getting the  LA Clippers to playoffs next year?

U: maybe

S: I do not think he will play a big role. I think he is past his prime. I am a little uncertain too. You can never account for randomness like injuries sidelining players.  do you want to chat about another trade ?

U: yes

S: Okay! I found a new trade news that says that Willie Cauley-Stein  from Golden State Warriors is going to Dallas Mavericks Does that sound interesting?

U: no

S: I found this other trade article. Jordan McRae  from Washington Wizards is going to Denver Nuggets

U: yes

S: Okay, then what do you think about Jordan McRae  ?

U: hes pretty good

S: So you think  Jordan McRae   is aight.  As an unexperienced player, I think Jordan McRaeHe has been making stable contribution to the team even though his stats don't stand out.And I think his contribution can get even better if playoff was to start.  Do you think that trade influenced how the  Denver Nuggets  performed this season? 
```
