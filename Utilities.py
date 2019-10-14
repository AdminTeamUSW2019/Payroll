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
  
def GetDbData():
    print("Loading...")

    #Check for database file, if not exist create file with correct formating
    if not os.path.exists("./dbConnectionData.json"):
        print("Database connection data file missing!\nCreating File...")

        #generate data
        data = {
		    'username': '',
		    'password': '',
		    'host': '',
			'database_name': ''
			}
        
        with open('dbConnectionData.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
		#exit program
        exit(0)


	#Open File
    with open("dbConnectionData.json") as json_file:
        data = json.load(json_file)
        return data