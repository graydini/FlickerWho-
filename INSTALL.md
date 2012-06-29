fill out setting.py adding your api keys in the space provided, and tags to search for.
this project requires the following python librarys:
* flickr_api from https://github.com/alexis-mignon/python-flickr-api.git
* faceclient from https://github.com/Kami/python-face-client
currently you need to run Photo.models.gatherImages() from './manage.py shell' to populate the database, this will be made into a command suitable for cron soon.
