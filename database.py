import pymysql as sql

class database:
	def __init__(self):
		'''
			(self) -> (None)
			
			*** established the class variables that are required
			 by the database connection to be established by the
			 program upon request by the flask server		   ***
		'''
		#we have no required class variables hence we pass the function
		pass
	def connection_data_push(self, organization, description, location, img, status):
		'''
			(string, string, string, string, string) -> (boolean)
			
			@paramaters the inputed data must be scanned for malicious data, etc.
			 
			*** established a connection with the mysql database to
			 store information inputed by the the website visitor ***
		'''
		#settup the generic paramaters required to make a connection to the mysql database hosted by digital
		#ocean servers, autocommit is True to ensure that all changes, additions, and deletions are made after
		#the queries have been placed on the server, other data is generic login requirments
		connection = sql.connect(
			host = 'db-mysql-tor1-25463-do-user-1518724-0.db.ondigitalocean.com',
			port = 25060,
			user = 'doadmin',
			passwd = 'e9gyc0vtu66g1emn',
			autocommit = True,
			db = 'defaultdb' #the database the table for the reports can be found on
		)
		try:
			with connection.cursor() as cursor:
				#insert into the reports table data that coresponds to the columns of originization, location, 
				#descirption, image coresponding to the report and the status of the report (most likely by default
				#'reported') 
				s = f"INSERT INTO reports (organization, location, description, image, status) VALUES (\'{organization}\', \'{location}\', \'{description}\', \'{img}\', \'{status}\');"
				#execute the string mysql syntatical request to the database/table in order to add the report data to the
				#server so that it can be requested by the user-application later on for map-population, etc.
				cursor.execute(s)
				#close the connection to avoid future problems being encountered when attempting to re-submit another query
				cursor.close()
		except:
			#in acordance to the docstrings, we can return to the main business logic side of the program that an error has been
			#encountered and that whatever query atempting to be made didn't suceed
			return False
		#assume that at this point the query has sucessfuly been commited and changed had been made though acknowledge the
		#docstrings in that a false positive is not out of the question
		return True
	def connection_data_collect_from_org(self, organization):
			'''
				(string) -> (list of strings)
				
				@paramaters the inputed data must be scanned for malicious data, etc. AND the orginization
							should be valid in order to receive useful data
				@returns a multidimentional list of strings represting all the rows of data associated with
						 a specific originization requesting to see all the requests pertaining to them
				@exception returns an empty list if the originization did not exist OR there was an error/bug
						 encountered along the way such as a connection being dropped while attempting to connect
				
				*** established a connection with the mysql database to return all information ***
			'''
			#settup the generic paramaters required to make a connection to the mysql database hosted by digital
			#ocean servers, autocommit is True to ensure that all changes, additions, and deletions are made after
			#the queries have been placed on the server, other data is generic login requirments
			connection = sql.connect(
				host = 'db-mysql-tor1-25463-do-user-1518724-0.db.ondigitalocean.com',
				port = 25060,
				user = 'doadmin',
				passwd = 'e9gyc0vtu66g1emn',
				autocommit = True,
				db = 'defaultdb' #the database the table for the reports can be found on
			)
			try:
				with connection.cursor() as cursor:
					#select all rows where the originization inputed into the function coresponds to the collumn
					#for population on a visual data table on the website
					s = f"SELECT * FROM reports WHERE organization = \'{organization}\';"
					cursor.execute(s)
					#retreive the row associated with the selected originization, will be useful in populating a table of data that
					#can be displayed to the user so that they can acknowledge all the requests in progress
					data = cursor.fetchone()
					#close the connection to avoid future problems being encountered when attempting to re-submit another query
					cursor.close()
			except:
				#if an error was encountered we will return an empty string inidcating this error, we do this isntead of a boolean false
				#to respect the docstrings so this will become the deafult failure value
				return ''
			finally:
				#assume that at this point the query has sucessfuly been commited and changed had been made though acknowledge the
				#docstrings in that a false positive is not out of the question
				return data
	def connection_data_remove_from_db(self, organization, location, description):
		'''
			(string, string, string) -> (boolean)
			
			@paramaters the inputed data must be scanned for malicious data, etc. AND the orginization
						should be valid in order to receive useful data
						
			@returns 'True' if the connection to the database in order to remove a request data set was
					 successful meaning that it was removed from the database entirly and cannot be redone
			@exception returns 'False' if the mysql connection has failed during the attempt remove the
					   request from the database this is possibly because of a failure to connect (server
					   is down) or there was some other bug encountered along the way
			
			*** REMEMBER : A FALSE POSITIVE CAN BE ENCOUNTERED MEANING THAT THE CONTENT WAS ONLY REMOVED
				IF A VALID COLUMN DATA WAS GIVEN (DATA THAT IS KNOWN TO EXIST IN THE SERVER)		 ***
		'''
		#settup the generic paramaters required to make a connection to the mysql database hosted by digital
		#ocean servers, autocommit is True to ensure that all changes, additions, and deletions are made after
		#the queries have been placed on the server, other data is generic login requirments
		connection = sql.connect(
			host = 'db-mysql-tor1-25463-do-user-1518724-0.db.ondigitalocean.com',
			port = 25060,
			user = 'doadmin',
			passwd = 'e9gyc0vtu66g1emn',
			autocommit = True,
			db = 'defaultdb' #the database the table for the reports can be found on
		)
		try:
			with connection.cursor() as cursor:
				#from the database 'defaultdb' and table 'reports' which hold the data for all the reports on the website, find the columns
				#that specifically have the arguments for the org. , location, and descirption and delete it from the table entirly
				s = f"DELETE FROM reports WHERE (organization, location, description) = (\'{organization}\', \'{location}\', \'{description}\');"
				print(s)
				cursor.execute(s)
				#close the connection to avoid future problems being encountered when attempting to re-submit another query
				cursor.close()
		except:
			#in acordance to the docstrings, we can return to the main business logic side of the program that an error has been
			#encountered and that whatever query atempting to be made didn't suceed
			return False
		#assume that at this point the query has sucessfuly been commited and changed had been made though acknowledge the
		#docstrings in that a false positive is not out of the question
		return True
	def report_change_status(self, organization, location, description, new_status):
		'''
			(string, string, string) -> (boolean)
			
			@returns 'True' if the connection to the database in order to modify the status of a request data
					 was successful meaning that it was changed from the its original value (etc. pending->done)
			@exception returns 'False' if the mysql connection has failed during the attempt modify the
					   request from the database this is possibly because of a failure to connect (server
					   is down) or there was some other bug encountered along the way
			
			*** REMEMBER : A FALSE POSITIVE CAN BE ENCOUNTERED MEANING THAT THE CONTENT WAS ONLY REMOVED
				IF A VALID COLUMN DATA WAS GIVEN (DATA THAT IS KNOWN TO EXIST IN THE SERVER)		 ***
		'''
		#settup the generic paramaters required to make a connection to the mysql database hosted by digital
		#ocean servers, autocommit is True to ensure that all changes, additions, and deletions are made after
		#the queries have been placed on the server, other data is generic login requirments
		connection = sql.connect(
			host = 'db-mysql-tor1-25463-do-user-1518724-0.db.ondigitalocean.com',
			port = 25060,
			user = 'doadmin',
			passwd = 'e9gyc0vtu66g1emn',
			autocommit = True,
			db = 'defaultdb' #the database the table for the reports can be found on
		)
		try:
			with connection.cursor() as cursor:
				#using the database and table that stores all the vital report data on the server, where the originization, location, and descirption
				#function arguments match or are inclusivly apart of a specific row/column we need to change the status in order to indicated visually
				#the current status of any report ever submited to the database
				s = f"UPDATE reports SET status = \'{new_status}\' WHERE (organization, location, description) = (\'{organization}\', \'{location}\', \'{description}\');"
				cursor.execute(s)
				#close the connection to avoid future problems being encountered when attempting to re-submit another query
				cursor.close()
		except:
			#in acordance to the docstrings, we can return to the main business logic side of the program that an error has been
			#encountered and that whatever query atempting to be made didn't suceed
			return False
		#assume that at this point the query has sucessfuly been commited and changed had been made though acknowledge the
		#docstrings in that a false positive is not out of the question
		return True