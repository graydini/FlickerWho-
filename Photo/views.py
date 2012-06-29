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
	myGame = Game.objects.get(id=request.GET['game_id'])
	
def poll(request):
	messages = cache.get('u_messages_%s' % request.user.id)
	if messages:
		return HttpResponse(messages)
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
