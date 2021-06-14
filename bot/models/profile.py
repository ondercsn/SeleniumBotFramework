from bot.lib.functions import *
from bot.db._mysql import DB
from bot.models.email import Email
from bot.models.proxy import Proxy
from bot.models.useragent import UserAgent

from faker import Faker

class Profile:

	def __init__(self,db, logger, proxy=None,email=None,useragent=None):
		self.db = db
		self.logger = logger
		self.proxy = proxy
		self.email = email
		self.useragent = useragent

		self.id = None
		self.status = None
		self.profile = None
		self.project = 0
		self.email_verified = False
		self.is_active = True

		self.username = None
		self.password = None
		self.firstname = None
		self.lastname = None
		self.fullname = None


	def generateIdentity(self, profile_id=None, fake_data=True, country=None, gender=1):

		if not profile_id:
			if fake_data:
				fake = Faker()
				self.firstname = fake.pystr(min_chars=12, max_chars=15).lower()
				self.lastname = fake.pystr(min_chars=12, max_chars=15).lower()
				self.username = fake.pystr(min_chars=12, max_chars=15).lower()
				self.password = generate_password(size=10)

		else:
			profileSql = 'SELECT * FROM profiles WHERE id = %s' % profile_id
			profileDatas = self.db.fetchOne(profileSql)
			self.firstname = profileDatas['name']
			self.lastname = profileDatas['surname']
			self.username = profileDatas['username']
			self.password = profileDatas['password']

		return self


	def create(self):
		self.user_identity = self.generateIdentity(country='DE')
		return self


	def __repr__(self):
		return {
			'profile' : self.profile,
			'user_identity': self.user_identity,
			'proxy': self.proxy,
			'email': self.email,
			'useragent': self.useragent
		}

	def __str__(self):
		return str(self.__repr__())


	def get(self, profile_id):
		if profile_id is not None:
			userSql = "SELECT * FROM profiles WHERE profile_id = %s and status>=0" % profile_id
			sqlResult = self.db.fetchOne(userSql)

			self.id = profile_id
			self.email_verified = sqlResult['email_verified']
			self.id = profile_id
			self.status = sqlResult['status']

			self.email = Email(self.db, self.logger,random=False).get(id=sqlResult['email_id'])
			self.proxy = Proxy(self.db, self.logger).get()
			self.useragent = UserAgent(self.db, self.logger).from_string(sqlResult['useragent'])
			self.user_identity = self.generateIdentity(profile_id=profile_id)

		return self


	def delete(self,id):
		return self.db.execQuery('update profiles set status=-1 where id=%s' % id)


	def set_status(self,id, status):
		return self.db.execQuery('update profiles set status=%s where id=%s' % (status, id))
