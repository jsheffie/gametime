#!/usr/bin/env python

import requests
import requests.packages.urllib3
import json
import time

game_type="training"
#game_type="championship"
server_url="https://umbelmania.umbel.com/%s/" % game_type

moves=["A", "B", "C", 
	   "D", "E", "F", 
	   "G", "H", "I",
	   "J", "K" ]

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

my_game_results = {}
my_game_results['opponent']='na'
my_game_results['moves']={}

#-------------------------------------------
def make_my_move(current_move, last_run_moves, opponent_move=False):
	#for move in cheat_sheet.keys():
	print "current_move: %d" % ( current_move )
	if str(current_move) in last_run_moves:
		if last_run_moves[str(current_move)]["score"] > 0:
			# it was a good move 
			print "!!! it was a good move... use it !!! "
			return last_run_moves[str(current_move)]['move']

	print "!!! calculating a better move !!!"
	for move in sorted(cheat_sheet.keys(), reverse=True):
		#print "--> move: %s opponent_move: %s" % ( move, opponent_move )
		if opponent_move:
			if str(current_move) in last_run_moves:
				if opponent_move in cheat_sheet[move]["beats"] and last_run_moves[str(current_move)]['move'] != move:
					#print "!!! move: %s" % ( move )
					return move
			else:
				if opponent_move in cheat_sheet[move]["beats"]:
					#print "!!! move: %s" % ( move )
					return move


	return "A"


#-------------------------------------------
# make the first request
requests.packages.urllib3.disable_warnings()

opponent= "el-rey-muy-dante"
pdata={"moves":{}}
try:
	fh = open('game_results.txt', 'r')
	previous_data=fh.read()
	#import pdb; pdb.set_trace();
	pdata = json.loads(previous_data)
	opponent = pdata['opponent']
	#pdata['moves']
	fh.close()
except:
	pass
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
#while moves_remaining > 990:
while moves_remaining > 0:
	print "Moves Remaining: %d" % ( moves_remaining )
	r = requests.post(server_url, data =json.dumps(data), headers=headers) 
	#time.sleep(1)
	print "Server Status Code: %d" % ( r.status_code ) 
	print r.content
	data = json.loads(r.content)
	
	if current_move > 0: 
		my_game_results["moves"][current_move-1]["score"]=data['gamestate']['score']
		
	data["move"]="K"
	try:
		moves_remaining=data['gamestate']['moves_remaining']
		if 'opponent_move' in data['gamestate']:
			data["move"]=make_my_move(current_move, pdata['moves'], data['gamestate']['opponent_move'])
		else:
			data["move"]=make_my_move(current_move, pdata['moves'])

		my_game_results["moves"][current_move]={}
		my_game_results["moves"][current_move]["move"]=data["move"]

		if 'score' in data['gamestate'] and 'total_score' in data['gamestate']:
			print "Score: %d" % ( data['gamestate']['score']) 
			print "Total Score: %d" % ( data['gamestate']['total_score']) 
	except Exception, e:
		raise
	current_move=current_move + 1

f = open('game_results.txt', 'w')
my_game_results['opponent']=initial_data['opponent']
f.write(json.dumps(my_game_results))
f.close()
