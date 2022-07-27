import sys
try:
	import requests
	from bs4 import BeautifulSoup
except ModuleNotFoundError:
	print('To use this program, please install the required modules (requests and bs4)')
	sys.exit()

class InvalidArgumentError(Exception): pass
class Player:
	"""It is the principal class of the module to spy the players."""
	def __init__(self, tag: str) -> None:
		if type(tag) != str: raise InvalidArgumentError("Argument type must be string")
		self.tag = tag
	
	def spy(self):
		"""Can be used to create subclasses for the player."""
		response = requests.get(f'https://deckshop.pro/spy/player/{self.tag}')
		while response==None: pass
		if response.status_code == 200:
			data = response.text
			soup = BeautifulSoup(data, 'html.parser')
			tablesSection = soup.find("section", {"class": "grid"})
			cells = tablesSection.find_all("td")
			heads = tablesSection.find_all("th")
			titles = []
			for head in heads:
				if head.string != None and head.string != '0':
					titles.append(head.string.strip())
			del titles[0]
			del titles[4]
			del titles[8]
			del titles[5]
			titles = titles[:8]+titles[20:23]
			try: 
				titles.remove('Cards Won')
				if titles[8] == 'Battle Count': titles.pop(8)
				del titles[8]
				titles.append('Total donations')
				titles.append('Donations')
				titles.append('Donations received')
			except ValueError: pass
			current = 0
			cells = cells[:10]+cells[-3:]
			for cell in cells:
				if cell.string != None:
					exec(f'self.{titles[current].lower().replace(" ", "_").replace("losses", "loses")} = "{cell.string.strip().replace(" ", "")}"')
					current += 1
			self.days_spent_playing = soup.find("div", {"class": "spoiler-reveal"}).string.strip()[1:]
			self.clan = soup.find("h4", {'class': 'mb-0'}).findChild('a')['href'][10:-10]
			self.username = soup.find('h1', {'class': 'mb-0'}).string
			if self.username == None: self.username = '**special characters**'
			else: self.username = self.username.strip()
			if int(self.current_trophies) >= 4000:
				self.arena = self.league
				self.league = None
		else: return 'Error 404.'
class Clan:
	def __init__(self, id) -> None:
		self.tag = id
	def spy(self, rtype: type = list):
		rlist = rtype == list
		rdict = rtype == dict
		response = requests.get(f'https://www.deckshop.pro/spy/clan/{self.tag}')
		while response == None: pass
		if response.status_code == 200:
			data = response.text
			soup = BeautifulSoup(data, 'html.parser')
			tags = soup.find_all('small', {'class': 'text-gray-muted'})
			notreqtags = soup.find_all('small', {'class': 'timestamp text-gray-muted'})
			names = soup.find_all('a', {'class': 'text-blue-link text-lg'})
			if rlist: usersdict = []
			elif rdict: usersdict = {}
			iterator = 0
			for tag in tags:
				try: name = names[iterator].string
				except: break
				if notreqtags.__contains__(tag): continue
				else:
					tag = tag.string.replace('🍊', '').strip()[1:]
					iterator += 1
					if name == None: name = '**special characters**'
					if rlist: usersdict.append((name, tag))
					elif rdict: usersdict[name.strip()] = tag
			return usersdict
		else:
			return 'Error 404.'
