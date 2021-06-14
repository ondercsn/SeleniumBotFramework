import time
import requests

class Proxy:

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.id = id
        self.address = None
        self.port = None
        self.username = None
        self.password = None
        self.ipversion = 4
        self.protocol = None

    def get(self, version=4, where=None, id=None, project_id=None, order=None, limit=None):
        result = {}

        if id is None:
            where_s = ""

            if order is None:
                order = "ORDER BY RANDOM()"

            if limit is None:
                limit = "LIMIT 1"

            if where is not None:
                where_s = (" AND %s " % where)

            if project_id is not None:
                where_s = (" %s AND p.project_id=%s " % (where_s, project_id))

            sql = "SELECT p.* FROM proxies p " \
                  "LEFT JOIN profiles pr ON pr.proxy_id = p.id " \
                  "WHERE blacklist = 0 AND p.status=1 AND p.version=%s %s " \
                  "GROUP BY p.id " % (version, where_s)

            finalSql = ("%s %s %s" % (sql, order, limit))
        else:
            finalSql = "SELECT * FROM proxies WHERE id = %s " % id

        result = self.db.fetchOne(finalSql)

        if result:
            address = result["address"] if result["version"] == 4 else result["v6addr"]

            self.proxyModel = self.set(address=address,
                                       port=result["port"], username=result["user"], password=result["pass"],
                                       ipversion=result["version"], id=result['id'],
                                       protocol=result["protocol"])

            return self

    def set(self, address, port, username=None, password=None, ipversion=4, id=None, protocol=None):
        self.id = id
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.ipversion = ipversion
        self.protocol = protocol

    def check_proxies(proxy_model, testUrl="https://www.google.com/recaptcha/api2/demo"):
        t = 0
        headers = []
        proxyDict = {
            "http": 'http://%s:%s' % (proxy_model.address, proxy_model.port),
            "https": 'https://%s:%s' % (proxy_model.address, proxy_model.port)
        }
        try:
            r = requests.get(testUrl, headers=headers, proxies=proxyDict, timeout=10)
            if int(r.status_code) != 200:
                return False
        except:
            return False


    def __repr__(self):
        return {
            "id": self.id,
            "address": self.address.strip(),
            "port": self.port.strip(),
            "username": self.username.strip(),
            "password": self.password.strip(),
            "version": self.ipversion,
            "protocol": self.protocol
        }

    def __str__(self):
        return str(self.__repr__())
