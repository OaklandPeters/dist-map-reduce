
# Setup web server
# Web server ~ Index

# Correspondence:
# config_file <--> Index
# 	entries = [...
#		FilePath: to config file, or to record file
#		URL: to another Web-index



class IndexABC(object):
	pass

class IndexDispatcher(IndexABC):
	"""Dispatches to other indexes.
	"""

class IndexTerminal(IndexABC):
	"""
	Consists of a number of RecordChunks
	"""

class RecordChunk():
	"""
	Can be .live (in memory) or .dormant (on hard-drive)
	Can be told to 'wake' (become live), or, if read from, wakes before responding
	"""
