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
#def gather_images():
#	import flickr_api as flickr

def getFace(photo):
	"""Takes a response from face api and returns the face_area of the first face found in a picture."""
	nose = photo['tags'][0]['nose']['y']
	center = photo['tags'][0]['nose']['x']
	mouth = photo['tags'][0]['mouth_center']['y']
	height = photo['height']
	width = photo['width']
	ratio = mouth - nose
	scale_h = height / 100.0
	scale_w = width / 100.0
	c_width = int((ratio * 9) * scale_w)
	c_height = int((ratio * 9) * scale_h)
	c_left = int((center * scale_w) - ((ratio * 6) * scale_w))
	c_top = int((nose * scale_h) - ((ratio * 5) * scale_h))
	face_area = (c_left,c_top,c_left+c_width,c_top+c_height)
	return face_area



