import mysql.connector

class DB:
	def __init__(self, host=None, username=None, password=None, dbname=None):
		self.connection = None
		self.cursor = None

		self.host = host
		self.username = username
		self.password = password
		self.dbname = dbname
		self._connect()

	def _connect(self):
		try:
			self.connection = mysql.connector.connect(
			host=self.host,
			user=self.username,
			passwd=self.password,
			database=self.dbname,
			use_unicode=True,)

		except mysql.connector.Error as err:
			print('connection error')
			print (err)

		try:
			self.connection.set_charset_collation('utf8', 'utf8_unicode_ci')
			self.cursor = self.connection.cursor(dictionary=True, buffered=True)
		except Exception as err:
			print(err)

	def execQuery(self, sql):
		result = None
		try:
			result = self.cursor.execute(sql)
			self.connection.commit()
		except Exception as err:
			print("error on query : ",err)

		return result

	def fetchAll(self, sql):
		self.cursor.execute(sql)
		result = self.cursor.fetchall()

		return result

	def fetchOne(self, sql):
		result = None
		try:
			self.cursor.execute(sql)
			result = self.cursor.fetchone()
		except Exception as err:
			print('error : ',err)

		return result

	def last_id(self):
		self.cursor.execute("SELECT last_insert_id() as last_insert_id")
		sresult = self.cursor.fetchone()
		result = sresult['last_insert_id']
		return result
