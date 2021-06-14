import sqlite3

class DB:

	def __init__ (self, dbpath=None):
		self.dbpath = dbpath
		self.connection = None
		self.cursor = None
		self._connect()

	def dict_factory(self,cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	def _connect (self):
		dbname = self.dbpath
		self.connection = sqlite3.connect(dbname)
		self.connection.row_factory = self.dict_factory

		self.cursor = self.connection.cursor()

	def query(self,sql) :
		result = self.cursor.execute(sql)
		return result


	def execQuery(self,sql) :
		result = self.cursor.execute(sql)
		self.connection.commit()
		return result

	def fetchAll(self, sql):
		records  = self.cursor.execute(sql)
		result = records.fetchall()
		return result

	def fetchOne(self,sql):
		rows = self.cursor.execute(sql)
		result = rows.fetchone()
		return result
	
	def last_id (self):
		return self.cursor.lastrowid


	

