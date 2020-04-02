import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from api import *


class TestingCursorIterator:
	__test__ = False

	def __init__(self, cursor):
		self._cursor = cursor
		self._index = 0

	def __next__(self):
		if self._index < len(self._cursor.results):
			result = self._cursor.results[self._index]
			self._index += 1
			return result
		raise StopIteration

class TestingCursor:
	__test__ = False

	data = {
		'text#foo' : [ {'id':123} ],
		'text#bar' : [],
		'container#foo' : [ {'id':456} ],
		'container#bar' : [] ,
		'executable#111/foo' : [ {'id':112} ] ,
		'executable#111/bar' : [] ,
	}

	def __init__(self,db):
		self._db = db
		self._rows = []

	def __iter__(self):
		return TestingCursorIterator(self)

	def execute(self,query,args):
		self.results = []
		self.lastrowid = 0
		if query=="""SELECT `id` FROM `text` WHERE `text`=%s""":
			self.results = self.data['text#'+args[0]]
		elif query=="""SELECT `id` FROM `container` WHERE `image`=%s""":
			self.results = self.data['container#'+args[0]]
		elif query=="""SELECT `id` FROM `executable` WHERE `container_id`=%s AND `name`=%s""":
			self.results = self.data['executable#'+str(args[0])+'/'+args[1]]

		elif query=="""INSERT IGNORE INTO `text` (`text`) VALUES (%s)""":
			self.lastrowid = 789
			self.data['text#'+args[0]] = {'id':self.lastrowid}
		elif query=="""INSERT IGNORE INTO `container` (`image`) VALUES (%s)""":
			self.lastrowid = 135
			self.data['container#'+args[0]] = {'id':self.lastrowid}
		elif query=="""INSERT IGNORE INTO `executable` (`container_id`,`name`) VALUES (%s,%s)""":
			self.lastrowid = 113
			self.data['executable#'+str(args[0])+'/'+args[1]] = {'id':self.lastrowid}
		elif query=="""INSERT IGNORE INTO `logging_event` (`user`,`timestamp`,`image`,`executable`,`path`,`parameters`) VALUES (%s,%s,%s,%s,%s,%s)""":
			if args == ('xyz9', '2020-03-02 11:22:33', 'the_image.sif', 'run_me', '/nfs/foo/bar', 'the_first "the last" \'eternity\''):
				self.lastrowid = 12345
			else:
				self.lastrowid = 0

		else:
			print ("TestingCursor::execute UNRECOGNIZED")
			print (query)
			print (args)

class TestingDB:
	__test__ = False

	def __init__(self):
		return

	def cursor(self,buffered=False,dictionary=False):
		return TestingCursor(self)

	def commit(self):
		return


@pytest.fixture
def client():
    global app
    app.config['TESTING'] = True
    app.test_db = TestingDB()
    return app.test_client()
