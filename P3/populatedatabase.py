from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Director, Base, Movie

engine = create_engine('sqlite:///directors.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Movies for Martin Scorsese
director1 = Director(	name = "Martin Scorsese",
						bio = "Martin Charles Scorsese is an American director, producer, screenwriter, actor, and film historian. Part of the New Hollywood wave of filmmaking, he is widely regarded as one of the most significant and influential filmmakers in cinema history.",
						image = "http://ia.media-imdb.com/images/M/MV5BMTcyNDA4Nzk3N15BMl5BanBnXkFtZTcwNDYzMjMxMw@@._V1._SX140_CR0,0,140,209_.jpg")

session.add(director1)
session.commit()

movie1 = Movie(	name = "The Wolf of Wall Street",
				image = "http://ia.media-imdb.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_SX214_AL_.jpg",
				trailer = "iszwuX1AK6A",
				description ="In 1987, Jordan Belfort (Leonardo DiCaprio) takes an entry-level job at a Wall Street brokerage firm. By the early 1990s, while still in his 20s, Belfort founds his own firm, Stratton Oakmont. Together with his trusted lieutenant (Jonah Hill) and a merry band of brokers, Belfort makes a huge fortune by defrauding wealthy investors out of millions. However, while Belfort and his cronies partake in a hedonistic brew of sex, drugs and thrills, the SEC and the FBI close in on his empire of excess.",
				director = director1)
session.add(movie1)
session.commit()

movie2 = Movie(	name = "Hugo",
				image = "http://ia.media-imdb.com/images/M/MV5BMjAzNzk5MzgyNF5BMl5BanBnXkFtZTcwOTE4NDU5Ng@@._V1_SX214_AL_.jpg",
				trailer = "hR-kP-olcpM",
				description ="Orphaned and alone except for an uncle, Hugo Cabret (Asa Butterfield) lives in the walls of a train station in 1930s Paris. Hugo's job is to oil and maintain the station's clocks, but to him, his more important task is to protect a broken automaton and notebook left to him by his late father (Jude Law). Accompanied by the goddaughter (Chloe Grace Moretz) of an embittered toy merchant (Ben Kingsley), Hugo embarks on a quest to solve the mystery of the automaton and find a place he can call home.",
				director = director1)
session.add(movie2)
session.commit()

movie3 = Movie(	name = "Shutter Island",
				image = "http://ia.media-imdb.com/images/M/MV5BMTMxMTIyNzMxMV5BMl5BanBnXkFtZTcwOTc4OTI3Mg@@._V1_SX214_AL_.jpg",
				trailer = "5iaYLCiq5RM",
				description = "The implausible escape of a brilliant murderess brings U.S. Marshal Teddy Daniels (Leonardo DiCaprio) and his new partner (Mark Ruffalo) to Ashecliffe Hospital, a fortress-like insane asylum located on a remote, windswept island. The woman appears to have vanished from a locked room, and there are hints of terrible deeds committed within the hospital walls. As the investigation deepens, Teddy realizes he will have to confront his own dark fears if he hopes to make it off the island alive.",
				director = director1)
session.add(movie3)
session.commit()

#Movies for George Lucas
director1 = Director(	name = "George Lucas",
						bio = "George Walton Lucas, Jr. is an American film director, screenwriter, producer, and entrepreneur. He founded Lucasfilm and led the company as chairman and chief executive before selling it to The Walt Disney Company on October 30, 2012.",
						image = "http://ia.media-imdb.com/images/M/MV5BMTA0Mjc0NzExNzBeQTJeQWpwZ15BbWU3MDEzMzQ3MDI@._V1._SY209_CR1,0,140,209_.jpg")

session.add(director1)
session.commit()

movie1 = Movie(	name = "Star Wars: Episode IV - A New Hope",
				image = "http://ia.media-imdb.com/images/M/MV5BMTU4NTczODkwM15BMl5BanBnXkFtZTcwMzEyMTIyMw@@._V1_SX214_AL_.jpg",
				trailer = "vZ734NWnAHA",
				description = "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a wookiee and two droids to save the universe from the Empire's world-destroying battle-station, while also attempting to rescue Princess Leia from the evil Darth Vader.",
				director = director1)
session.add(movie1)
session.commit()