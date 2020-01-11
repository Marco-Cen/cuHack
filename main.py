########################################################################
# Impoorts Required for Flask Server Functionality
########################################################################
from flask import Flask, render_template, url_for, abort, redirect

########################################################################
# Primative and non-Primitve user-data imports for text/database
########################################################################
from data import GenericData

########################################################################
# Server Settup / Socket Address Initilization and Referects
########################################################################

app = Flask(__name__)

#route a new port for connection to the general domain in the case a connection
#has been made without an intended html file
@app.route('/')
def index():
	return render_template('report.html', title='GeoMap | Report an Issue')

#route a new port for connection to the main page containing the general report
#bar as well as questions and about-us on a paralax style page
@app.route('/report')
def home():
	#we are directing them to the main page so call the function made to handle
	#generic requests made to the server
	return index()

#route a new port for connection to the secondary page which displays a live view
#of all the ongoing reports made to the server by anonymous individuals
@app.route('/display')
def about():
	return render_template('display.html', title='GeoMap | Current Reports Around You')

#in the case the user has typed a sub-address that does not exist direct them to a
#cannot be found page | once again we start by routing a new port for connection
@app.errorhandler(404)
def handle(error):
	return render_template('error.html', title='404 Error')
	
#we only want to run this server from this file, only during the build-phase should we have
#debugging turned on which will automaticly update the page on commit
if __name__ == "__main__":
	app.run(debug=True)