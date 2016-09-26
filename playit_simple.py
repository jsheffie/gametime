#!/usr/bin/env python

import requests
import requests.packages.urllib3
import json
import time

#game_type="training"
game_type="championship"
server_url="https://umbelmania.umbel.com/%s/" % game_type

moves=["A", "B", "C", 
     "D", "E", "F", 
     "G", "H", "I",
     "J", "K" ]

# You can fetch the cheat sheet from here: 
#     https://umbelmania.umbel.com/moves/
# however: I like having it here for reference.
cheat_sheet = {
  "A": {
    "beats": [
      "B",
      "C",
      "D",
      "E",
      "F"
    ],
    "name": "Diamond Dust"
  },
  "C": {
    "beats": [
      "D",
      "E",
      "F",
      "G",
      "H"
    ],
    "name": "Mushroom Stomp"
  },
  "B": {
    "beats": [
      "C",
      "D",
      "E",
      "F",
      "G"
    ],
    "name": "Shooting Star"
  },
  "E": {
    "beats": [
      "F",
      "G",
      "H",
      "I",
      "J"
    ],
    "name": "Gorilla"
  },
  "D": {
    "beats": [
      "E",
      "F",
      "G",
      "H",
      "I"
    ],
    "name": "Belly Flop"
  },
  "G": {
    "beats": [
      "H",
      "I",
      "J",
      "K",
      "A"
    ],
    "name": "Death Valley"
  },
  "F": {
    "beats": [
      "G",
      "H",
      "I",
      "J",
      "K"
    ],
    "name": "Flapjack"
  },
  "I": {
    "beats": [
      "J",
      "K",
      "A",
      "B",
      "C"
    ],
    "name": "Atomic Drop"
  },
  "H": {
    "beats": [
      "I",
      "J",
      "K",
      "A",
      "B"
    ],
    "name": "Catapult"
  },
  "K": {
    "beats": [
      "A",
      "B",
      "C",
      "D",
      "E"
    ],
    "name": "Bulldog"
  },
  "J": {
    "beats": [
      "K",
      "A",
      "B",
      "C",
      "D"
    ],
    "name": "Rollercoaster"
  }
}


#-------------------------------------------
def make_my_move(current_move, last_run_moves, opponent_move=False):
    return "A"


#-------------------------------------------
# make the first request
requests.packages.urllib3.disable_warnings()

opponent= "pato-bajo-jr"
initial_data = {
  # Potential opponent's
  # "pato-bajo-jr", "princesa-comico", "el-rey-muy-dante", "senor-amistoso"
  "opponent": opponent,
  "player_name": "Jeff Sheffield",
  "email": "jeff.sheffield@gmail.com"
}
headers = {'content-type': 'application/json'}

moves_remaining=2000

data=initial_data
current_move=0
while moves_remaining > 0:
    print "Moves Remaining: %d" % ( moves_remaining )
    r = requests.post(server_url, data =json.dumps(data), headers=headers) 
    print "Server Status Code: %d" % ( r.status_code ) 
    
    if moves_remaining < 2:
        print r.content

    data = json.loads(r.content)

    data["move"]="A"

    moves_remaining=data['gamestate']['moves_remaining']

    if 'score' in data['gamestate'] and 'total_score' in data['gamestate']:
        print "Score: %d" % ( data['gamestate']['score']) 
        print "Total Score: %d" % ( data['gamestate']['total_score']) 

    current_move=current_move + 1

