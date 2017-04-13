from __future__ import print_function, division
from Spider import *
from Edge import *
import time
import copy
import math


# Needs words in lowercase, and if multiple words, join them using '_'

class Wordclient:
	def __init__(self, word):
		'''
		Constructor to crawl web for a word 
		'''
		self.alpha = 1 # To scale dimensions
		self.beta = 100 # To scale dimensions
		self.gamma = 100 # To scale dimensions
		self.delta = 100 # To scale dimensions

		self.word = word
		sp = Spider(word, spread=2, limit=0.01)
		self.web = sp.crawl('Graph.shelve')	# Crawled web
		self.graph = Shelveopen('Graph.shelve')

		self.paths = []	# To store all paths
		self.scores = []	# To store corresponding pathscores

		self.clientfeatures = []	# Feature vector for client
		self.standardfeatures = []	# To compare against

	# Reusable function for another client
	def init_client(self, client=None):
		'''
		To initialize diff. parameters related to client
		'''
		if client is None:
			client = self.client
		else:
			self.client = client

		self.paths, self.scores = self.calcmetric(client)

		#Initializing client features
		i = self.getpathnum() * self.alpha
		j = self.gethighestscore() * self.beta
		k = self.getmeanscore() * self.gamma
		l = self.gettotalscore() * self.delta
		self.clientfeatures = [i, j, k, l]

	def init_standard(self):
		'''
		To initialize diff. parameters to oneself
		'''
		paths, scores = self.calcmetric(self.word)

		#Initializing client features
		i = self.getpathnum(paths) * self.alpha	# To scale to other dimensions
		j = self.gethighestscore(scores) * self.beta
		k = self.getmeanscore(scores) * self.gamma
		l = self.gettotalscore(scores) * self.delta
		self.standardfeatures = [i, j, k, l]

	#Generic function for reuse
	def calcmetric(self, client):
		clientpaths = []
		clientscores = []
		total = []

		clientedges = self.graph[client]
		clientdests = []
		for edge in clientedges:
			clientdests.append(edge.dest)

		common_points = []
		for node in self.web:
			if node in clientdests:
				common_points.append(node)

		# Handles case when no common points exist
		extrapath = {}
		for node in common_points:
			edges = self.graph[node]
			for edge in edges:
				if edge.dest == client:
					extrapath[node] = edge
					break

		for node in common_points:
			paths = self.web[node]
			for path in paths:
				extraedge = extrapath[node]
				if extraedge:	# If path exists
					ls = copy.deepcopy(path)
					ls.append(extraedge)
					clientpaths.append(ls)

		# Score calculation
		for path in clientpaths:
			score = 1
			for edge in path:
				score *= edge.weight
			clientscores.append(score)

		total.append(clientpaths)
		total.append(clientscores)
		return total

	# Functions strictly for access only, no reuse
	def getscores(self):
		'''
		To access client scores
		'''
		return self.scores

	def getpaths(self):
		'''
		To access client paths
		'''
		return self.paths

	def getfeatures(self):
		'''
		To access client features
		'''
		return self.clientfeatures

	def getstandard(self):
		'''
		To access standard features to oneself
		'''
		if self.standardfeatures:
			return self.standardfeatures
		else:
			self.init_standard()	# Initialize Standard
			return self.standardfeatures

	def getmetric(self):
		'''
		To get semantic score between client and word
		'''
		if self.standardfeatures == []:
			self.init_standard()

		print ('Client',self.client,':',self.clientfeatures)
		print ('Standard',self.word,':',self.standardfeatures)
		return cosine_similarity(self.standardfeatures, self.clientfeatures)

	def printweb(self):
		'''
		To Print entire web
		'''
		print ('FROM : ',self.word)
		for dest, paths in self.web.items():
			print ('TO : ',dest)
			for i, path in enumerate(paths):
				print ('PATH',i+1,' :',end='')
				for edge in path:
					print (' |',edge, end='')
				print ()

	def printpaths(self, paths=None, scores=None):
		'''
		To print paths to a sclient
		'''
		if paths is None:
			paths = self.paths
		if scores is None:
			scores = self.scores
		if paths:
			for i, path in enumerate(paths):
				print ('PATH', i+1,' :',end='')
				for edge in path:
					print (' |',edge, end='')
				print  ()
				print ('PathScore : ',scores[i])
		else:
			print ('Word',dest,'is not reachable from Source')

	# Functions reused to create features for standard and client, also can be accessed directly for client
	def gettotalscore(self, scores=None):
		'''
		To compute total score
		'''
		if scores is None:
			scores = self.scores
		return sum(scores)

	def getmeanscore(self, scores=None):
		'''
		Get Mean of all scores
		'''
		if scores is None:
			scores = self.scores
		if len(scores) == 0:
			return 0	# To prevent division by zero
		else:
			return round(sum(scores)/len(scores),3)

	def gethighestscore(self, scores=None):
		'''
		To return highest score
		'''
		if scores is None:
			scores = self.scores
		if len(scores) == 0:
			return 0	# To prevent no arg. error
		else:
			return max(scores)

	def getpathnum(self, paths=None):
		'''
		To return no of paths obtained
		'''
		if paths is None:
			paths = self.paths
		return len(paths)

if __name__ == '__main__':
	start_time = time.time()
	word = 'puppy'
	client = 'dog'
	try:
		wc = Wordclient(word)
		wc.init_client(client)
		# wc.printweb()
		# wc.printpaths()
		print ('Final Score :',wc.getmetric())
		print ('Execution Time : ',time.time() - start_time)
	except Exception as e:
		print ('Error Wordclient- ',e)