from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.cache import cache
from Photo.models import *
from django.utils import simplejson
from copy import copy

def index(request):
	pass
def board(request):
	player = Player.objects.get(user=request.user)
	"""Find esisting game else start a new one"""
	game_id = request.GET.get('game_id',False)
	if game_id:
		try:
			myGame = Game.objects.get(id=game_id)
			opponent_username = myGame.players.all()[0].user.username
			choice = request.GET.get('choice')
			if choice:
				game_info = cache.get('game_id_%s' % game_id)
				if game_info[player.user.username][2] == 1:
					myGame.player1_choice = choice
				else:
					myGame.player2_choice = choice
				myGame.save()
		except:
			return HttpResponse('failed')
	else:
		"""Find opponent"""
		try:
			opponent_username = request.GET['opponent']
		except:
			opponent_username = cache.get('waiting_player')
			if opponent_username:
				cache.delete('waiting_player')
			else:
				cache.set('waiting_player',player.user.username,200)
				return HttpResponse("waiting")
		opponent = Player.objects.get(user__username=opponent_username)
		myGame = Game()
		myGame.save()
		myGame.players.add(player)
		myGame.players.add(opponent)
		cache.set('game_id_%s' % game_id,{player.user.username:[0,0,1],opponent_username:[0,0,2]})
		photos = Photo.objects.filter(has_face=True).order_by('?')[:20]
		row = 0
		col = 0
		for photo in photos:
			tile = Tile()
			tile.photo = photo
			tile.row = row
			tile.col = col
			if row < 3:
				if col < 4:
					col += 1
				else:
					col = 0
					row += 1
			tile2 = copy(tile)
			tile.belongs_to = player
			tile2.belongs_to = opponent
			tile.save()
			tile2.save()
			myGame.tiles.add(tile)
			myGame.tiles.add(tile2)
	tiles = []
	for tile in myGame.tiles.filter(belongs_to=player):
		tiles.append({'id':tile.id,'pic':tile.photo.pic,'row':tile.row,'col':tile.col})
	to_json = {
	'opponent':opponent_username,
	'tiles':tiles,
	'game_id':myGame.id
}
	return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')

def guess(request):
	to_json=""
	game_id = request.GET['game_id']
	myScores = cache.get('game_id_%s' % game_id)
	myGame = Game.objects.get(id=game_id)
	opponent = request.GET['opponent']
	if myGame.players.all()[0] == opponent:
		im_player_1 = False
	else:
		im_player_1 = True
	guess = request.GET.get("guess")
	if guess:
		if im_player_1:
			opponent_choice = myGame.player2_choice
			myGame.player2_score = myScores[request.user.username][0]
			myGame.player2_guesses += 1
			myGame.player2_score -= (myGame.player2_guesses * 50)
			myScores[request.user.username][0] = myGame.player2_score
		else:
			opponent_choice = myGame.player1_choice
			myGame.player1_score = myScores[request.user.username][0]
			myGame.player1_guesses += 1
			myGame.player1_score -= (myGame.player1_guesses * 50)
			myScores[request.user.username][0] = myGame.player1_score
		cache.set('game_id_%s' % game_id, myScores)
		if solve == opponent_choice:
			send_message(opponent,{"guess":"solved","scores":myScores})
			to_json = {"solved":True,"scores":myScores}
		else:
			myGame.save()
			send_message(opponent,{"guess":guess,"scores":myScores})
			to_json = {"solved":False,"scores":myScores}
	else:
		send_message(opponent,request.GET['clue'])
	return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')

def send_message(recipeint,message):
	m_id = 'u_messages_%s' % recipeint
	messages = cache.get(m_id)
	if not messages:
		messages = []
	messages.append(message)
	cache.set(m_id,messages)

def respond(request):
	to_json=[]
	answer = request.GET.get('reply',False)
	opponent = request.GET['opponent']
	game_id = 'game_id_%s' % request.GET['game_id']
	if answer:
		send_message(opponent,answer)
		scores = cache.get(game_id)
		scores[opponent][1]+=1 # Incraments moves
		if answer == 'yes':
			scores[opponent][0]+= 50 * scores[opponent][1]
		else:
			scores[opponent][0]-= 20
		cache.set(game_id,scores)
		to_json={"scores":scores}
	else:
		send_message(request.GET['to'],request.GET['message'])
	return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
def poll(request):
	m_id = 'u_messages_%s' % request.user.username
	messages = cache.get(m_id)
	if messages:
		cache.delete(m_id)
		return HttpResponse(simplejson.dumps(messages))
	else:
		return HttpResponse()
def players(request):
	uid = request.user.id
	cache.set('u_%s' % uid, uid,300)
	players = cache.get('players')
	active_players = [uid]
	player_ids = []
	if players:
		print players
		for player in players:
			this_player = cache.get('u_%s' % player)
			if this_player and not this_player == uid:
				active_players.append(player)
				player_ids.append(this_player)
		cache.set('players',active_players,300)
	else:
		cache.set('players',[request.user.id],300)

	to_json = []
	if player_ids:
		for p_id in player_ids:
			to_json.append(User.objects.get(id=p_id).username)
	return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
