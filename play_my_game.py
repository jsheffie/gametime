#!/usr/bin/env python

import requests
import requests.packages.urllib3
import json
import time
import sys

#game_type="training"
game_type="championship"
server_url="https://umbelmania.umbel.com/%s/" % game_type

moves=["A", "B", "C", 
       "D", "E", "F", 
       "G", "H", "I",
       "J", "K" ]

# 165 char repeating sequence
my_unique_sequence=[ "A","B","F","D","G","F","G","H","F","G","K","F","B","C","I","E","F","F","H","G","F","K","A","F","G",
                     "D","F","F","G","I","I","J","F","A","G","F","D","E","F","G","H","F","J","K","I","B","C","F","E","G",
                     "F","H","I","F","G","A","F","C","D","I","F","G","F","I","G","F","A","B","F","G","E","F","G","H","I",
                     "J","K","F","B","G","F","E","F","F","G","I","F","K","A","I","C","D","F","F","G","F","I","J","F","G",
                     "B","F","D","E","I","G","H","F","J","G","F","B","C","F","G","F","F","H","I","I","K","A","F","C","G",
                     "F","F","G","F","G","J","F","A","B","I","D","E","F","G","G","F","J","K","F","G","C","F","E","F","I",
                     "H","I","F","K","G","F","C","D","F","G","G","F","I","J","I"]
playing_my_game=["A","B","F"]


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
def make_my_move(current_move):
    print "Current Move: %s" % ( current_move )
    for move in cheat_sheet.keys():
        if current_move in cheat_sheet[move]["beats"]:
            print "!!! move: %s" % ( move )
            return move


#-------------------------------------------
# make the first request

# I nee over 1k moves ( there are 165 moves in my_unique_sequence)
my_game_moves = my_unique_sequence * 10
opponent_actual_moves = []

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

moves_remaining=1111 # magic number over 1000

data=initial_data
current_move=0

while moves_remaining > 0:
    print "Moves Remaining: %d" % ( moves_remaining )
    r = requests.post(server_url, data =json.dumps(data), headers=headers) 
    #time.sleep(1)
    print "Server Status Code: %d" % ( r.status_code ) 

    if moves_remaining < 2:
        print r.content

    data = json.loads(r.content)
    moves_remaining=data['gamestate']['moves_remaining']
    data["move"]=make_my_move(my_game_moves[current_move])

    #import pdb; pdb.set_trace()
    try:
        opponent_move = data['gamestate']['opponent_move']
        opponent_actual_moves.append(opponent_move)
        if current_move == 3: 
            # are we playing my game?
            if not opponent_actual_moves == playing_my_game:
                print opponent_actual_moves
                print playing_my_game
                print "We are not playing my game, lets play again sometime"
                sys.exit(1)
            

        if 'score' in data['gamestate'] and 'total_score' in data['gamestate']:
            print "Score: %d" % ( data['gamestate']['score']) 
            print "Total Score: %d" % ( data['gamestate']['total_score']) 
    except KeyError:
        pass
    except Exception, e:
        raise

    current_move=current_move + 1
