from bot.lib.functions import generate_string


class Email:

    def __init__(self, db, logger, random=True):
        self.db = db
        self.logger = logger
        self.random = random

        self.id = id
        self.address = None
        self.password = None
        self.imap_address = None
        self.imap_port = None


    def get(self, where=None, id=None):
        if self.random is True:
            self.set("%s@gmail.com" % generate_string().lower())
        else:
            where_s = ""
            if where:
                where_s = (" AND %s " % where)

            if id is None:
                sql = "SELECT e.* FROM emails e " \
                      "LEFT JOIN profiles pr ON pr.email_id = e.id " \
                      "WHERE e.is_active=1 AND e.blacklist=0 AND profile_id IS NULL %s ORDER BY RAND() LIMIT 1" % (
                          where_s)

            else:
                sql = "SELECT * FROM emails WHERE id = %s" % (id)

            finalSql = sql

            try:
                result = self.db.fetchOne(finalSql)
                self.set(result['email_address'], result['id'], result['password'], result['imap_address'], result['imap_port'])

            except Exception as err:
                self.logger.error('error on getting email : ', err)

        return self


    def set(self, address, id=None, password=None, imap_address=None, imap_port=None ):
        self.id = id
        self.address = address
        self.password = password
        self.imap_address = imap_address
        self.imap_port = imap_port

        return self


    def __repr__(self):
        return {
            "id": self.id,
            "address": self.address,
            "imap_addr": self.imap_address,
            "imap_port": self.imap_port,
            "password": self.password
        }

    def __str__(self):
        return str(self.__repr__())