#!/usr/bin/env python
import fresh_tomatoes
import media
""" Each movie instance has these 6 attributes in order
movie.title
movie.storyline
movie.poster_image_url
movie.trailer_youtube_url
movie.main_cast
movie.release_date
"""
ocean_11 = media.Movie("Ocean Eleven",\
	"Danny orchestrates the most sophisticated, elaborate casino heist in history.",\
	"http://iv1.lisimg.com/image/175447/600full-ocean%27s-eleven-poster.jpg",\
	"https://youtu.be/m7lrZK21AX4",\
	["George Clooney","Matt Damon","Andy Garc&#237a","Brad Pitt","Julia Roberts"],\
	"December 7, 2001")

edge_of_tomorrow = media.Movie("Edge of Tomorrow",\
	"When Earth falls under attack from invincible aliens, no military unit in the world is able to beat them. \
	Maj. William Cage (Tom Cruise), an officer who has never seen combat, is assigned to a suicide mission. Killed \
	within moments, Cage finds himself thrown into a time loop, in which he relives the same brutal fight -- and his \
	death -- over and over again. However, Cage's fighting skills improve with each encore, bringing him and a comrade \
	(Emily Blunt) ever closer to defeating the aliens.",\
	"http://www.joblo.com/timthumb.php?src=/posters/images/full/edge_of_tomorrow_np.jpg&w=654&zc=1&q=90",\
	"https://youtu.be/yUmSVcttXnI",\
	["Tom Cruise","Emily Blunt","Bill Paxton","Brendan Gleeson"],\
	"June 6, 2014"
	)

the_bourne_identity = media.Movie("The Bourne Identity",\
	"The story of a man (Matt Damon), salvaged, near death, from the ocean by an Italian fishing boat. \
	When he recuperates, the man suffers from total amnesia, without identity or background... except \
	for a range of extraordinary talents in fighting, linguistic skills and self-defense that speak of \
	a dangerous past. He sets out on a desperate search-assisted by the initially rebellious Marie \
	(Franka Potente) - to discover who he really is, and why he's being lethally pursued by assassins.",\
	"http://www.slantmagazine.com/assets/house/film/posterlabbournelegacy_5.jpg",\
	"https://youtu.be/FpKaB5dvQ4g",\
	["Matt Damon","Franka Potente","Chris Cooper","Clive Owen","Brian Cox","Adewale Akinnuoye-Agbaje"],\
	"June 14, 2002")

stardust = media.Movie("Stardust",\
	"To win the heart of his beloved (Sienna Miller), a young man named Tristan (Charlie Cox) ventures \
	into the realm of fairies to retrieve a fallen star. What Tristan finds, however, is not a chunk of \
	space rock, but a woman (Claire Danes) named Yvaine. Yvaine is in great danger, for the king's sons \
	need her powers to secure the throne, and an evil witch (Michelle Pfeiffer) wants to use her to \
	achieve eternal youth and beauty.",\
	"https://s-media-cache-ak0.pinimg.com/736x/d3/14/d4/d314d44f52b553192143cef2a2654c5f.jpg",\
	"https://youtu.be/VfYBKDyF-Dk",\
	["Claire Danes","Charlie Cox","Sienna Miller","Jason Flemyng","Mark Strong","Rupert Everett","Peter \
	O\'Toole","Michelle Pfeiffer","Robert De Niro"],\
	"10 August 2007")

cashback = media.Movie("Cashback",\
	"Would-be artist Ben (Sean Biggerstaff) realizes he has an extraordinary way of dealing with the \
	tedium of his dead-end job stocking shelves at a store -- he has acquired the ability to halt time \
	and explore the world while the rest of the earth's population remains frozen in place. Ben's unusual \
	talent helps him forget about a nasty breakup with his ex-girlfriend Suzy (Michelle Ryan), but he begins \
	to stop time so often that he may miss out on a new romance with his coworker Sharon (Emilia Fox).",\
	"https://s-media-cache-ak0.pinimg.com/originals/a9/0d/d9/a90dd93df6a88a7a2636559bd9f395fc.jpg",\
	"https://youtu.be/8qnQz8kxte0",\
	["Sean Biggerstaff","Emilia Fox","Shaun Evans","Michelle Ryan","Stuart Goodwin","Michael Dixon",\
	"Michael Lambourne","Marc Pickering"],\
	"10 September 2006")

training_day = media.Movie("Training Day",\
	'Police drama about a veteran officer who escorts a rookie on his first day with the LAPD\'s tough \
	inner-city narcotics unit. "Training Day" is a blistering action drama that asks the audience to \
	decide what is necessary, what is heroic and what crosses the line in the harrowing gray zone of \
	fighting urban crime. Does law-abiding law enforcement come at the expense of justice and public \
	safety? If so, do we demand safe streets at any cost?',\
	"http://image.tmdb.org/t/p/original/aD0JIpFkduApsVhj9G575VfJhiK.jpg",\
	"https://youtu.be/DXPJqRtkDP0",\
	["Denzel Washington","Ethan Hawke"],\
	"September 21, 2001")

toy_story = media.Movie("Toy Story",\
	"A story of a boy and his toys that come to life",\
	"http://i.imgur.com/NeB2R69.jpg",\
	"https://youtu.be/3Zuxjl1L6sA",\
	["Tom Hanks","Tim Allen","Don Rickles","Jim Varney","Wallace Shawn","John Ratzenberger","Annie \
	Potts","John Morris","Erik von Detten","Laurie Metcalf","R. Lee Ermey","Sarah Freeman"],\
	"November 22, 1995")

avatar = media.Movie("Avatar",\
	"A marine on an alien planet",\
	"http://www.comicbookmovie.com/images/users/gallerypictures/6660L.jpg",\
	"https://youtu.be/EgHI4YBXhxM",\
	["Sam Worthington","Zoe Saldana","Stephen Lang","Michelle Rodriguez","Sigourney Weaver"],\
	"December 18, 2009")

movies = [ocean_11,edge_of_tomorrow,the_bourne_identity,stardust,cashback,training_day,toy_story,avatar]
fresh_tomatoes.open_movies_page(movies)
#print media.Movie.VALID_RATINGS
#print media.Movie.__doc__
#print media.Movie.__name__
#print media.Movie.__module__