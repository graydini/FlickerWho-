from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
	p_id = models.IntegerField()
	has_face = models.BooleanField()
	name = models.CharField(max_length=50,blank=True,null=True)
	face_x = models.IntegerField(blank=True,null=True)
	face_y = models.IntegerField(blank=True,null=True)
	face_width = models.IntegerField(blank=True,null=True)
	pic = models.FilePathField(blank=True,null=True)
	date_posted = models.IntegerField()
class Tile(models.Model):
	photo = models.ForeignKey('Photo')
	onboard = models.BooleanField()
	row = models.IntegerField()
	col = models.IntegerField()
	belongs_to = models.ForeignKey('Player')
class Player(models.Model):
	user = models.ForeignKey(User)
	games = models.ManyToManyField('Game')
	highest_game_score = models.IntegerField()
	score = models.IntegerField()
	friends = models.ManyToManyField('self')
	enemies = models.ManyToManyField('self')
class Game(models.Model):
	players = models.ManyToManyField('Player')
	player1_score = models.IntegerField()
	player2_score = models.IntegerField()
        player1_guesses = models.IntegerField()
        player2_guesses = models.IntegerField()
	tiles = models.ManyToManyField('Tile')
	
