import smtplib

from email.mime.text import MIMEText

def send_message(email_receiving, organization, location, descirption):
	'''
		(string, string, string, string) -> (none)
		
		@returns a value of 'None' no matter what, there is no indication of whether the email was
				 sent sucesfully to the organization though we will still have the records in our db
				
		*** THIS SHOULD ONLY BE USED FOR VALID-EMAILS THAT HAVE BEEN HARVESTED OR ARE FOR DEBUGGING***
	'''
	#Setup a template which can be used for every email made to companies that have been reported
	#online by a user, the attempt is to make a friendly but informative greeting
	formated_message = f'''
		
		Greetings {organization},
		
		This is an automated message notifiying your organization that a report was recently filed on
		our platform relating to an issue around {location}.
		
		The description of the issue was found described as:
			
		{descirption}
		
		GeoStatus is an online platform dedicated to providing a user-friendly and reliable platform
		for reporting local issues related to specific companies. We are not responsible for the reports
		made by users, this platform is an atempt to amplify the voice of the good-citizen.
	'''

	#The following modifies the msg dictionary that will be used within the email sent by the mailgun
	#platform
	msg = MIMEText(formated_message)
	msg['Subject'] = "GeoStatus | {organization}, we're reporting a known issue."
	msg['From']    = "postmaster@automated.geostatus.online"
	msg['To']      = "gabecofficial@gmail.com"

	s = smtplib.SMTP('smtp.mailgun.org', 587)

	#sign-in to the credentials of the mailgun account that is connected to the dns of the website, failure
	#to do this will result in an inability to send the email to the company
	s.login('postmaster@automated.geostatus.online', '34de62e8e3c5ce9a08465a18f12f2dc9-713d4f73-15cd22c3')
	s.sendmail(msg['From'], msg['To'], msg.as_string()) #finally send the mail using the templates and credentials
	s.quit()