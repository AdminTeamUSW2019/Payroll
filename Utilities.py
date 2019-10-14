#imports
import mysql.connector
import json
import os.path
import math
from decimal import Decimal

#todo: put this in a config file
workingDaysInMonth = 20

#struct to hold employee data for the GUI
class Employee:
	def __init__(self, employeeNum, forename, surname, email_address, salary,dateStarted, daysWorked):
		self.forename = forename
		self.surname = surname
		self.email_address = email_address
		self.salary = salary
		self.dateStarted = dateStarted
		self.employeeNumber = employeeNum
		self.daysWorked = daysWorked
  
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
		query = ("SELECT employee_number, forename, surname, email_address, salary, dateStarted, days_worked_this_month FROM Employees WHERE employee_number = %s")
		cursor.execute(query, (employeeNum,));

        #debug output
		for (employee_number,forename, surname, email_address, salary, dateStarted, days_worked_this_month) in cursor:
			print("-------------------------------")
			print("Employee num: " + str(employee_number))
			print("Forename: " + forename)
			print("Surname: " + surname)
			print("email addr: " + email_address)
			print("salary: " + str(salary))
			print("Date Hired:" + str(dateStarted))
			print("Days worked this month: " + str(days_worked_this_month))

            #return employee data
			tempEmployee = Employee(employeeNum, forename, surname, email_address, salary,dateStarted, days_worked_this_month)
   
			cursor.close()
			cnx.close()
   
			return tempEmployee


		#catch error
	except mysql.connector.Error as err:
		cursor.close()
		cnx.close()
  
def CalculateMonthlyWage(yearlySalery, daysWorked):
	#TO-DO: magic conversion here 
	taxRate = 0.00
	monthlyWageBeforeTax = (yearlySalery*100 / 260.71) * daysWorked
 
	#todo: put these values into a config file
 
	#locate tax bracket
	if yearlySalery > 150000:
		taxRate = 0.45
	elif yearlySalery > 50000:
		taxRate = 0.4
	elif yearlySalery > 12500:
		taxRate = 0.2
	else:
 		taxRate = 0.00
   
	temp = math.floor(monthlyWageBeforeTax* (1.0-taxRate))

   
	#return correct amount
	return float(temp/100)

def WriteEmployeePaylistToFile(employee):
	outputString = ("Employee: "+ str(employee.employeeNumber) +
                 "\nForename: " + employee.forename +
                 "\nSurname: " + employee.surname +
                 "\nEmail Addr: " + employee.email_address +
                 "\nDate Hired: " + str(employee.dateStarted) +
                 "\n------------------------------------------" +
                 "\n\nYearly Salery: " + str(employee.salary) +
                 "\nDays worked (month): " + str(employee.daysWorked) +
                 "\nWage for current month: " + str(CalculateMonthlyWage(employee.salary, employee.daysWorked)))
	f = open("Employee" + employee.employeeNumber + "Payslip", "w")
	f.write(outputString)
	f.close()