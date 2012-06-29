from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Photo(models.Model):
	p_id = models.IntegerField()
	has_face = models.BooleanField()
#	name = models.CharField(max_length=50,blank=True,null=True)
#	face_x = models.IntegerField(blank=True,null=True)
#	face_y = models.IntegerField(blank=True,null=True)
#	face_width = models.IntegerField(blank=True,null=True)
	pic = models.FilePathField(blank=True,null=True)
	date_posted = models.IntegerField()
class Tile(models.Model):
	photo = models.ForeignKey('Photo')
	onboard = models.BooleanField(default=True)
	row = models.IntegerField()
	col = models.IntegerField()
	belongs_to = models.ForeignKey('Player')
class Player(models.Model):
	user = models.ForeignKey(User)
	games = models.ManyToManyField('Game')
	highest_game_score = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	friends = models.ManyToManyField('self')
	enemies = models.ManyToManyField('self')
class Game(models.Model):
	players = models.ManyToManyField('Player')
	player1_score = models.IntegerField(default=0)
	player2_score = models.IntegerField(default=0)
	player1_guesses = models.IntegerField(default=0)
	player2_guesses = models.IntegerField(default=0)
	tiles = models.ManyToManyField('Tile')
def gatherImages():
	import flickr_api as flickr
	import Image
	flickr.set_keys(settings.FLICKR_API,settings.FLICKR_SECRET)
	try:
		latest = Photo.objects.latest('id').date_posted 
	except:
		latest = 00000000
	w = flickr.Walker(flickr.Photo.search, tags=settings.FLICKR_TAGS, min_upload_date =latest, sort="date-posted-asc")
	for photo in w:
		face_pic = recognizeFace(photo.getPhotoFile())
		dbPhoto = Photo()
		dbPhoto.p_id = photo.id
		dbPhoto.date_posted = photo.dateuploaded
		if not face_pic == False:
			dbPhoto.has_face = True
			pic_filename = settings.MEDIA_ROOT+'raw_photos/'+photo.id+'.jpg'
			photo.save(pic_filename)
			local_image = Image.open(pic_filename)
			face_file = local_image.crop(face_pic)
			face_file.save(settings.MEDIA_ROOT+'faces/'+photo.id+'.jpg','jpeg')
			dbPhoto.pic = 'faces/'+photo.id+'.jpg'
		else:
			dbPhoto.has_face = False
		dbPhoto.save()
			
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
	c_height = int((ratio * 9) * scale_w)
	c_left = int((center * scale_w) - ((ratio * 6) * scale_w))
	c_top = int((nose * scale_h) - ((ratio * 5) * scale_h))
	face_area = (c_left,c_top,c_left+c_width,c_top+c_height)
	return face_area

def recognizeFace(photo_url):
	from face_client import FaceClient
	client = FaceClient(settings.FACES_API,settings.FACES_SECRET)
	try:
		photo = client.faces_detect(photo_url)['photos'][0]
	except:
		return False
	if len(photo['tags']) > 0:
		return getFace(photo)
	else:
		return False
