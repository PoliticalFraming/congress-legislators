# with open("scripts/exec") as rtyaml
import rtyaml
import yaml
import logging
import datetime
import codecs
import dateutil.relativedelta

def get_string(date_variable):
	# Can't use strftime because it doesn't work for dates older than 1900
	date, time = date_variable.isoformat().split('T')
	return date


def get_date(date_string):
	return datetime.datetime.strptime(date_string, "%Y-%m-%d")

def make_terms_csv(yaml_file, output_file):
	"""
	Writes to the output_rile in CSV format a list of terms with the following feilds

	Fields:
	- bioguide 
	- firstname
	- lastname
	- birthday
	- start_date
	- end_date
	- party
	- state
	- incumbancy - "No" if this win was not a result of re-election immediately after serving a term in congress

	Input: 
	- yaml_file - yaml file to read from
	- output_file - csv file to write to
	"""

	# logging.basicConfig(level=logging.DEBUG)

	logging.debug("Creating CSV file of Terms")

	#Write Headers
	output_file.write("bioguide,firstname,lastname,birthday,state,party,start_date,end_date\n")

	current_yaml = yaml.load(yaml_file)
	for congressperson in current_yaml:

		#Congressperson specific variables
		bioguide = str(congressperson['id'].get('bioguide'))
		firstname = unicode(congressperson['name'].get('first',""))
		lastname = unicode(congressperson['name'].get('last',""))
		bio = congressperson.get('bio')
		birthday = bio.get('birthday',"") if bio else "Not Found"

		for i, term in enumerate(congressperson['terms']):
			#term specific variables
			start_date = get_date(term.get('start',""))
			end_date = get_date(term.get('end',""))
			party = term.get('party',"")
			state = term.get('state',"")

			incumbancy = True #True only if re-elected immediately after serving a term in congress
			if i==0:
				incumbancy = False
			else:
				previous_term = congressperson['terms'][i-1]
				previous_end_date = get_date(previous_term.get("end",""))
				if not previous_end_date > start_date -	dateutil.relativedelta.relativedelta(months=6):
					incumbancy = False

			to_write = [
				bioguide,
				firstname,
				lastname,
				birthday,
				state,
				party,
				get_string(start_date),
				get_string(end_date),
				"Yes" if incumbancy else "No"]

			output_file.write(",".join(to_write)+"\n")
			logging.debug("Processed Term %d for %s %s (%s)", i, firstname, lastname, bioguide)

# Make CSV of current legislators' terms
with open("yaml/legislators-current.yaml","r") as current_legilslators_file:
	with codecs.open("current-legislators-terms.csv", mode= "w", encoding="utf-8") as csvfile:
		make_terms_csv(current_legilslators_file, csvfile)

# Make CSV of historical legislators' terms
with open("yaml/legislators-historical.yaml","r") as historical_legislators_file:
	with codecs.open("historical-legislators-terms.csv", mode="w", encoding="utf-8") as csvfile:
		make_terms_csv(historical_legislators_file, csvfile)





