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

@app.route('/')
def index():
	return render_template('report.html', title='GeoMap | Report an Issue')

@app.route('/report')
def home():
	return redirect(url_for('/'))

@app.route('/display')
def about():
	return render_template('display.html', title='GeoMap | Current Reports Around You')

@app.errorhandler(404)
def handle(error):
	return render_template('handler.html', title='404 Error')
	
if __name__ == "__main__":
	app.run(debug=True)