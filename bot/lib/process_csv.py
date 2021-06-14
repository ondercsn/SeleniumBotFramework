# -*- coding: utf-8 -*-

import csv
from bot.db._mysql import DB

db = DB()


def add_proxy_list_to_db(file_path, version=6, project_id=1, description=""):
	with open(file_path, newline='') as cfile:
		sreader = csv.reader(cfile, delimiter=',', quotechar='|')

		for row in sreader:
			data1 = row[0]
			
			datax = data1.split(":")
			ip = datax[0]
			port = datax[1]
			#userdata = datax[2].split("@")
			username = '' #userdata[0]
			password = '' #userdata[1]

			countSql = "SELECT COUNT(*) as ccount FROM proxies WHERE v4addr='%s' and port='%s' " % (ip, port)
			currCount = db.fetchOne(countSql)

			if currCount['ccount'] == 0:
				
				query = ("INSERT INTO proxies (project_id, version, v4addr, port, description) VALUES ("\
					"%s, '%s', '%s', '%s', '%s' )"
					% (project_id,version, ip, port, description))

				db.execQuery(query)
				
			
	return True


def add_email_list_to_db(filename, host, imap, port):
	with open(filename, newline='') as cfile:
		sreader = csv.reader(cfile, delimiter=',', quotechar='|')
		for row in sreader:
			data1 = row[0]
			data2 = row[1]
			
			countSql = "SELECT COUNT(*) as ccount FROM emails WHERE email_address = '%s' " % data1
			currCount = db.fetchOne(countSql)
			
			if currCount['ccount'] is 0:
				query = ("INSERT INTO emails (email_address,password,host,imap_address,imap_port,add_date) VALUES ("\
					"'%s','%s','%s','%s','%s',NOW())" % (data1, data2, host, imap, port))

				db.execQuery(query)



def add_names_to_db(file_path, country='DE', gender=1):
	with open(file_path, newline='', encoding="utf8") as cfile:
		sreader = csv.reader(cfile, delimiter=',', quotechar='|')
		for row in sreader:
			
			name = row[0]
			surname = row[1]
			word = ""

			if len(row) >= 3:
				word = row[2]
			print(row)
			countSql = "SELECT COUNT(*) as cc FROM names WHERE\
			 			name='%s' AND surname='%s' AND country='%s' " % (name,surname,country)

			currCount = db.fetchOne(countSql)
			
			if currCount['cc'] == 0 and (name != "" or surname != "" or word != ""):
				query = ("INSERT INTO names (name,surname,word,country,gender) VALUES ("\
					" '%s', '%s', '%s','%s', %s)" % (name, surname, word, country, gender))
				db.execQuery(query)

def add_hashtag_to_db(file_path, country):

	with open(file_path, encoding="utf8") as cfile:
		for row in cfile:
			tag = row.strip()
			
			countSql = "SELECT COUNT(*) as cc FROM hashtags WHERE hashtag='%s' AND country='%s' " % (tag,country)
			currCount = db.fetchOne(countSql)
			
			if currCount['cc'] == 0 and tag != "":
				query = ("INSERT INTO hashtags (hashtag,country) VALUES ("\
					" '%s', '%s')" % (tag, country))
				db.execQuery(query)

def add_bios_to_db(file_path, country):

	with open(file_path, encoding="utf8") as cfile:
		for row in cfile:
			text = row.strip()
			
			try:
				print(text)
				countSql = "SELECT COUNT(*) as cc FROM bio WHERE bio_text='%s' AND country='%s' " % (text,country)
				currCount = db.fetchOne(countSql)
				
				if currCount['cc'] == 0 and tag != "":
					query = ("INSERT INTO bio (bio_text, country) VALUES ('%s', '%s')" % (tag, country))
					db.execQuery(query)
			except:
				pass

def add_accounts_to_db(filepath, project):
	#profile = Profile()

	with open(filepath, encoding="utf8") as cfile:
		sreader = csv.reader(cfile, delimiter=':', quotechar='|')
		for row in sreader:
			username = row[0]
			passw = row[1]
			email = row[2] 
			email_pass = row[3]

			currCountQ = db.fetchOne("SELECT COUNT(*) as cc FROM profiles WHERE email='%s' " % email)
			currCount = currCountQ['cc']
			print(email,currCount)
			

			if currCount <= 0 :
				pr = GetProxy(" p.project_id = 1 ")
				ua = GetUserAgent()
				
				print(pr)
				print(ua)
				
				sqlEmail = db.execQuery("INSERT INTO emails (email_address,password,add_date) VALUES ('%s','%s',NOW())" % (email, email_pass ) )
				email_id = db.last_id()
				#email_id = 10000

				sql = "INSERT INTO profiles \
				(proxy_id, useragent_id, useragent, screensize, password, email_id, email,login_with, project, add_date) \
				VALUES (%s, %s, '%s', '%s', '%s', %s, '%s', 2, 2,NOW()) " % (
					pr['proxy_id'],ua['useragent_id'],ua['agent_string'],ua['screen_size'],passw,email_id,email
				)
				db.execQuery(sql)
				print('%s yok' % username)

def FindDuplicates(file1, file2):
	f1 = open(file1,"r")
	f2 = open(file2,"r")

	r1 = set(f1.readlines())
	r2 = set(f2.readlines())

	print(r1)
	print(r2)
	#print(r1-r2)
	datas = (list(set(r1).intersection(r2)))
	print(datas)

	for data in datas:
		data = data.strip('\n')
		dataR = data.split(":")
		print(dataR)

		#db.execQuery("INSERT INTO proxies (project_id,v4addr,port,add_date,description) VALUES (2,'%s',%s,NOW(),'%s')" % (
		#	dataR[0],dataR[1],'shared_DE319015_DE319016'
		#))




if __name__ == "__main__" :
	#FindDuplicates("..\\files\\a\\proxies_http_ip_2.txt", "..\\files\\a\\proxies_http_ip_1.txt")
	#add_accounts_to_db(filepath="..\\files\\aged_profiles_100.txt", project=1)

	#add_hashtag_to_db("..\\files\\popular_hashtags_en.txt", "en")
	#add_bios_to_db("..\\files\\german_bio_new.txt", "de")

	#add_names_to_db('..\\files\\german_female_usernames.csv')

	#add_proxy_list_to_db('..\\files\\a\\proxies_http_ip_1.txt',version=4, project_id=2, description='proxy_check_list_2')
	#add_proxy_list_to_db('..\\files\\a\\proxies_http_ip_2.txt',version=4, project_id=2, description='proxy_check_list_1')
	#add_proxy_list_to_db('..\\files\\german_dedicated_proxy.txt', 4 , 'blazing_german_dedicated')

	#add_email_list_to_db('C:/Users/dell/Desktop/mails/500_O2PL_email.csv','o2.pl','poczta.o2.pl', 993)
	#add_email_list_to_db('C:/Users/dell/Desktop/mails/500outlook_email.csv','outlook.com','outlook.office365.com', 993)
	#add_email_list_to_db('C:/Users/dell/Desktop/mails/500hotmail_emails.csv','hotmail.com','imap-mail.outlook.com', 993)
	add_email_list_to_db('C:/Users/dell/Desktop/1k_email.csv', 'outlook.com', 'outlook.office365.com', 993)
	#AddNamesToDb()
