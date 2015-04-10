#!/usr/bin/env python
import webbrowser
class Movie(object):
	""" The class stores the information for a movie. """
	# class variable in ALL CAPS
	VALID_RATINGS = ["G","PG","PG-13","R"]
	def __init__(self, title, storyline, poster_image_url, trailer_url,main_cast,release_date):
		self.title = title
		self.storyline = storyline
		self.poster_image_url = poster_image_url
		self.trailer_youtube_url = trailer_url
		self.main_cast = main_cast
		self.release_date = release_date
	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)