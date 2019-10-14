#imports
import mysql.connector
import json
import os.path

#struct to hold employee data for the GUI
class Employee:
	def __init__(self, forename, surname, email_address, salery):
		self.forename = forename
		self.surname = surname
		self.email_address = email_address
		self.salery = salery