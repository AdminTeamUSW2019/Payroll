#imports
import mysql.connector
import json
import os.path

#struct to hold employee data for the GUI
class Employee:
	def __init__(self, forename, surname, email_address, salery, employeeNum):
		self.forename = forename
		self.surname = surname
		self.email_address = email_address
		self.salery = salery
		self.employeeNumber = employeeNum
  
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
        
        with open('./dbConnectionData.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
		#exit program
        exit(0)


	#Open File
    with open("./dbConnectionData.json") as json_file:
        data = json.load(json_file)
        return data
    
def GetEmployeeData(employeeNum, data):
    	#setup mysql connection
	try:
        #setup connection
		cnx = mysql.connector.connect(user=data['username'], database=data['database_name'], password=data['password'], host=data['host'], auth_plugin='mysql_native_password')
		cursor = cnx.cursor()

        #query database
		query = ("SELECT employee_number, forename, surname, email_address, salery FROM Employees WHERE employee_number = %s")
		cursor.execute(query, (employeeNum,));

        #debug output
		for (employee_number,forename, surname, email_address, salery) in cursor:
			print("-------------------------------")
			print("Forename: " + forename)
			print("Surname: " + surname)
			print("email addr: " + email_address)
			print("salery: " + str(salery))

            #return employee data
			tempEmployee = Employee(forename, surname, email_address, salery, employeeNum)
   
			cursor.close()
			cnx.close()
   
			return tempEmployee


		#catch error
	except mysql.connector.Error as err:
		cursor.close()
		cnx.close()