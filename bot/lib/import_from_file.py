import csv
from bot.db._mysql import DB


db = DB()


def AddProxyListToDb(file, proxy_type=4,):

	with open(file, newline='') as cfile:
		sreader = csv.reader(cfile, delimiter=',', quotechar='|')
		for row in sreader:
			data1 = row[0]
			
			datax = data1.split(":")
			ip = datax[0]
			port = datax[1]
			userdata = datax[2].split("@")
			username = userdata[0]
			password = userdata[1]

			countSql = "SELECT COUNT(*) as ccount FROM proxies WHERE v4addr='%s' and port='%s' " % (ip, port)
			currCount = db.fetchOne(countSql)

			if currCount['ccount'] == 0:
				query = ("INSERT INTO proxies (version, v4addr, port, user, pass) VALUES ("\
					" '%s', '%s', '%s', '%s', '%s' )"
					% (proxy_type, ip, port, username, password))

				db.execQuery(query)				

	return True


def AddProxyFromFile(file, project_id, proxy_type=4):
	with open(file) as cfile:
		lines = cfile.readlines()
		for line in lines:
			if (line):
				print(line)

				datax = line.split(":")
				ip = datax[0]
				port = datax[1]
				username = datax[2]
				password = datax[3]
	
				countSql = "SELECT COUNT(*) as ccount FROM proxies WHERE v4addr='%s' and port='%s' and project_id=%s " % (ip, port, project_id)
				currCount = db.fetchOne(countSql)
	
				if currCount['ccount'] == 0:
					query = ("INSERT INTO proxies (project_id, version, v4addr, port, user, pass) VALUES (" \
					         " %s, '%s', '%s', '%s', '%s', '%s' )"
					         % (project_id,proxy_type, ip, port, username, password))
	
					db.execQuery(query)

	return True


def AddEmailListToDb():

	with open('..\\files\\500mail.csv', newline='') as cfile:
		sreader = csv.reader(cfile, delimiter=',', quotechar='|')
		for row in sreader:
			data1 = row[0]
			data2 = row[1]
			
			host = "onet.pl"
			imap = "imap.poczta.onet.pl"
			port = 993

			countSql = "SELECT COUNT(*) as ccount FROM emails WHERE email_address = '%s' " % data1
			currCount = db.fetchOne(countSql)
			
			if currCount['ccount'] == 0:
				query = ("INSERT INTO emails (email_address, password, host, imap_address, imap_port) VALUES ("\
					" '%s', '%s', '%s', '%s', '%s' )"
					% (data1, data2, host, imap, port))
				#db.execQuery(query)
		

#AddProxyFromFile("../../tmp/webshare1000.txt",4)

