import pymysql as mdb
import traceback

class MyDB():
	def __init__(self):
			self.connection = None
			self.cursor = None

	def connect(self):
		self.connection = mdb.connect('192.168.100.93', 'username', 'password', 'gestioip')
		self.cursor = self.connection.cursor(mdb.cursors.DictCursor)
		return self

	def execute(self, sql, *args):
		# self.cursor = self.connection.cursor(mdb.cursors.DictCursor)
		try:
			self.connect()
			e = self.cursor.execute(sql, *args)
			self.connection.commit()
			self.cursor.close()
		except (mdb.Error, e):
			print(traceback.format_exc())
			self.connection.rollback()
		self.cursor.close()
		return e

	def queryone(self, sql, *args):
		try:
			self.connect()
			d = self.cursor
			d.execute(sql, *args)
			tmp = d.fetchone()
			d.close()
			return tmp

		# Reopen database connection
		except (AttributeError, mdb.OperationalError ):
			self.connect()
			self.cursor.execute(sql, *args)
			return self.cursor.fetchone()

	def queryall(self, sql, *args):
		try:
			self.connect()
			d = self.cursor
			d.execute(sql, *args)
			tmp = d.fetchall()
			d.close()
			return tmp

		# Reopen database connection
		except  (AttributeError, mdb.OperationalError ):
			self.connect()
			self.cursor.execute(sql, *args)
			return self.cursor.fetchall()

	def lastrowid(self, sql, *args):
		try:
			self.cursor.execute(sql, *args)
			return self.cursor.lastrowid
		# Reopen database connection
		except  (AttributeError, mdb.OperationalError ):
			self.connect()
			self.cursor.execute(sql, *args)
			return self.cursor.lastrowid

	def disconnect(self):
		self.connection.close()
