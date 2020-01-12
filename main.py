########################################################################
# Impoorts Required for Flask Server Functionality
########################################################################
from flask import Flask, render_template, url_for, abort, redirect, request

########################################################################
# Primative and non-Primitve user-data imports for text/database
########################################################################
from data import GenericData, OrganizationEmails
from database import database
from mailing import send_message

########################################################################
# Server Settup / Socket Address Initilization and Referects
########################################################################

app = Flask(__name__)
database = database()
emails = OrganizationEmails()

#route a new port for connection to the general domain in the case a connection
#has been made without an intended html file
@app.route('/', methods=['post', 'get'])
def index():
	if request.method == 'POST':
		#setup all the required pieces of data for transmition to the mysql server
		#so that the custom google maps can have the adresses added in the future
		organization = request.form.get('Organization')
		street_address = request.form.get('Street Address')
		postal_code = request.form.get('PostalCode')
		country = request.form.get('country')
		description = request.form.get('Description')
		#we need to format the data for street address, country, and postal code so that
		#it can fit within one element of the 'location' column on the database
		location = f"{street_address} {country} {postal_code}"
		#send a mysql query in order to store the request on the server
		database.connection_data_push(organization, description, location, "none", "reported")
		#send an email using mailgun so that the orignization selected can be informed about an
		#ongoing issue reported by an anonymous user
		send_message(emails['Demo Organization'], organization, location, description)
	
	return render_template('cuhacks.html', title='GeoMap | Report an Issue')

#route a new port for connection to the main page containing the general report
#bar as well as questions and about-us on a paralax style page
@app.route('/report', methods=['post', 'get'])
def home():
	#we are directing them to the main page so call the function made to handle
	#generic requests made to the server
	return index()

#route a new port for connection to the secondary page which displays a live view
#of all the ongoing reports made to the server by anonymous individuals
@app.route('/display')
def about():
	return render_template('pagetwo.html', title='GeoMap | Current Reports Around You')

#in the case the user has typed a sub-address that does not exist direct them to a
#cannot be found page | once again we start by routing a new port for connection
@app.errorhandler(404)
def handle(error):
	return index()
	
#we only want to run this server from this file, only during the build-phase should we have
#debugging turned on which will automaticly update the page on commit
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')