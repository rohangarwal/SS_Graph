from __future__ import print_function
from Commons import *
from Spider import *
from Edge import *

def Printpaths(word, web):
	'''
	To print paths to a specific word in web
	'''
	if word in web:
		paths = web[word]
		print ('TO : ',word)
		for i, path in enumerate(paths):
			print ('PATH', i+1,' :',end='')
			score = 1
			for edge in path:
				score *= edge.weight
				print (' |',edge, end='')
			print  ()
			print ('PathScore : ',score)
	else:
		print ('Word',word,'is not reachable from Source')

def Score(word, web):
	'''
	To Compute score of word in web
	'''
	if word in web:
		paths = web[word]
		print ('TO : ',word)
		score = 0
		for i, path in enumerate(paths):
			path_score = 1
			for edge in path:
				path_score *= edge.weight
			score += path_score
		return score
	else:
		print ('Word',word,'is not reachable from Source')
		return 0

def Printweb(word, web):
	'''
	To Print entire web of mentioned word
	'''
	print ('FROM : ',word)
	for word, paths in web.items():
		print ('TO : ',word)
		for i, path in enumerate(paths):
			print ('PATH',i+1,' :',end='')
			score = 1
			for edge in path:
				score *= edge.weight
				print (' |',edge, end='')
			print ()
			print ('PathScore : ',score)

if __name__ == '__main__':
	word = 'lion'
	client = 'tiger'
	try:
		sp = Spider(word)
		web = sp.crawl()	# Web obtained back around mentioned word
		# Printweb(word, web)
		Printpaths(client, web)
		print ('Final Score : ',Score(client, web))
	except Exception as e:
		print ('Error Wordclient- ',e)