from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.cache import cache
from Photo.models import *
from django.utils import simplejson

def index(request):
	pass
def board(request):
	pass
def move(request):
	pass
def poll(request):
	pass
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
