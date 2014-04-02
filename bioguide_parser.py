# with open("scripts/exec") as rtyaml
import json 
from jsoncomment import JsonComment
import MySQLdb
import rtyaml
import yaml


string = "[]"
parser = JsonComment(json)

# open DB connection
DB_PARAMS = ["localhost","capitolwords","capitolwords","capitolwords"]

conn=MySQLdb.Connection(*DB_PARAMS, use_unicode=True)
cursor = conn.cursor()

#get files
historical_legislators_file = open("yaml/legislators-historical.yaml","r")
current_legilslators_file = open("yaml/legislators-current.yaml","r")

current_yaml = yaml.load(historical_legislators_file)
for congressperson in current_yaml:
	bioguide = congressperson['id'].get('bioguide')
	firstname =congressperson['name'].get('first',"")
	lastname = congressperson['name'].get('last',"")
	bio = congressperson.get('bio')
	if bio:
		birthday = bio.get('birthday',"")
	party = congressperson['terms'][0].get('party',"")
	state = congressperson['terms'][0].get('state',"")
	
	if birthday and (birthday > "1900"):
		print str(bioguide) + " " + firstname + " " + lastname  + " " +party +" " + state

		try:
			insert = "INSERT INTO bioguide_legislator (bioguide_id,first,last, party) VALUES (%s,%s,%s,%s);" 
			data = (bioguide, firstname, lastname, party)
			cursor.execute(insert, data)
		except MySQLdb.IntegrityError:
			print "dupicate record"

conn.commit()
	# insert = "INSERT INTO bioguide_legislator (bioguide_id,first,last, party) VALUES (%s,%s,%s,%s);" 
	# data = (bioguide, firstname, lastname, party)
	# cursor.execute(insert, data)

historical_legislators_file.close()
current_legilslators_file.close()