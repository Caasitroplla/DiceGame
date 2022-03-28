import json
import random
import sys

class Player():
	def __init__(self):
		self._name = None
		self._score = 0
		self._highscore = 0
		self._password_hash = None
		self._authenticated = False
	
	# getters for attributes
	@property
	def name(self):
		return self._name
		
	@property
	def score(self):
		return self._score
		
	@property
	def highscore(self):
		return self._highscore
		
	# loading to an from json 
	def load_player(self, jsondata: dict):
		self._name = jsondata['name']
		self._highscore = jsondata['score']
		self._password_hash = jsondata['password']
		
	def dict_format(self) -> dict:
		return {
			"name" : self._name,
			"score" : self._highscore,
			"password" : self._highscore
		}
		
	# setters for attributes
	def set_name(self, name):
		self._name = name
		
	def reset(self):
		self._score = 0
		self._authenticated = False
		
	def increment_score(self, val : int):
		self._score += val
		if self._score > self._highscore:
			self._highscore = self._score
			
	# login function
	def login(self):
		count = 0
		while (self._authenticated == False) and (count > 3):
			attempt = str(input('Enter you password'))
			self._authenticated = hash(attempt) == self._password_hash
			count += 1
			
		if count > 3:
			OSError("Hackerman Detected")
			sys.exit()
			
	# login bypass
	def authenticate(self):
		self._authenticated = True
			
	# player turn
	def turn(self):
		roll1 = random.randint(1, 6)
		roll2 = random.randint(1, 6)
		total = roll1 + roll2
		# bonuses points
		if total % 2 == 0:
			total += 10
		else:
			total -= 5
		
		if roll1 == roll2:
			# bonus roll
			total += random.randint(1, 6)
			
		# adjusting = overall score
		self._score += total
		if self._score < 0:
			self._score = 0
			
		print(f'{self.name} rolled a {roll1} and a {roll2} for a total including bonuses of {total} making your over score {self.score} \n')
		
	def end_game(self):
		if self._score > self._highscore:
			self._highscore = self._score
			
	def new_password(self, text):
		self._password_hash = hash(text)


class Game:
	def __init__(self):
		self._players = []
		self.json_file_name = "players.json"
		
		
	# properties
	@property
	def players(self):
		return self._players
		
	# loads all the players in json so people can login
	def load_players(self):
		with open("players.json", "r") as file:
			data = json.load(file)
			for player in data['players']:
				new_player = Player()
				new_player.load_player(player)
				self._players.append(new_player)
	
	# saves players to json
	def save_players(self):
		with open("players.json", "w") as file:
			# generate json data
			dictionary = {"players" : []}
			for player in self._players:
				dictionary["players"].append(player.dict_format()) 
				
			json.dump(dictionary)
			
	# login or new players function
	def create_player(self):
		choice = int(input("Create new player [1] or Sign in [2]"))
		
		if choice == 1:
			# Create new player
			new_player = Player()
			new_player.set_name(input("Enter player name"))
			new_player.new_password(input("Enter your password"))
			self._players.append(new_player)
			new_player.authenticate()
			return new_player
			
		if choice == 2:
			# Sign in by entering name then authenticating sign in	
			search_name = input("Please enter your username")
			for player in self.players:
				if self.player.name.lower() == search_name.lower():
					player.login()
					return player
					
		SyntaxError("Inavlid Input")
		
	def sort_players(self):
		self._players.sort(key=lambda x: x.highscore, reverse=True)
		
	# main game loop
	def play(self):
		# login or create new player for both players
		player1 = self.create_player()
		player2 = self.create_player()
		
		count = 0
		while count > 5 and player1.score != player2.score:
			player1.turn()
			player2.turn()
			
		# show winner
		if player1.score > player2.score:
			# player one won
			print(f"{player1.name} won with a score of {player1.score}")
		
		else:
			# player two score
			print(f"{player2.name} won with a score of {player2.score}")
			
		player1.reset()
		player2.reset()
		
		# show top five scores
		self.sort_players()
		print("\nThe top five players are:")
		for player in self._players:
			print(f'{player.name} with a score of {player.highscore}')


if __name__ == '__main__':
	game = Game()
	game.play()




