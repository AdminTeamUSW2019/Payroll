#imports
import mysql.connector
import json
import os.path
import math
from decimal import Decimal
import hashlib

import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst

#method to create a popup window with title <title> and message <msg>
def popupmsg(title, msg):
    win = tk.Tk()
    win.title(title);
    frame1 = tk.Frame(
    master = win,
    bg = '#bdbbb7')
    frame1.pack(fill='both', expand='yes')
    editArea = tkst.ScrolledText(
        master = frame1,
        wrap   = tk.WORD,
        width  = 80,
        height = 50
    )
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.insert(tk.INSERT, msg)
    win.mainloop()
    
    
def popupMessageFromFile(title, file):
    try:
        f = open(file, "r")
        popupmsg(title, f.read())
    except:
        popupmsg("Error", "Opening text file failed, contact a system enginner.")
#struct to hold employee data for the GUI
class Employee:
  def __init__(self, employeeNum, forename, surname, email_address, salary, daysWorked):
    self.forename = forename
    self.surname = surname
    self.email_address = email_address
    self.salary = salary
    self.employeeNumber = employeeNum
    self.daysWorked = daysWorked

def login_verification(username, password, data):

	#setup connection
	cnx = mysql.connector.connect(user=data['username'], database=data['database_name'], password=data['password'], host=data['host'])
	cursor = cnx.cursor()

	#set login rsult as false
	login_Result = False
	
	#query database
	query = ("SELECT user_number, username, password FROM login")
	cursor.execute(query)

	#fetch data result
	records = cursor.fetchall()

	for row in records:
		if username == row[1] and password == row[2]:
			login_Result = True
			
	cursor.close()
	cnx.close()
	return login_Result

#return user hashed password
def hash_password(username, password, data):

	#fetch user unique code
    salt = get_salt(username,data)[0]
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + salt

def get_salt(username, data):
	#setup connection
    cnx = mysql.connector.connect(user=data['username'], database=data['database_name'], password=data['password'], host=data['host'])
    cursor = cnx.cursor()

	#query database
    query = ("SELECT salt FROM login WHERE username = %s ")
    cursor.execute(query, (username,))

	#fetch one row of data
    myResult = cursor.fetchall()

    for row in myResult:
        return row

    return myResult


def GetJsonData():
    print("Loading...")

    #Check for database file, if not exist create file with correct formating
    if not os.path.exists("./appData.json"):
        print("App data file missing!\nCreating File...")

        #generate data
        data = {
		    'username': '',
		    'password': '',
		    'host': '',
			'database_name': '',
			'database_table': 'employees',
			'working_days_in_year': 260.71,
			'employee_contribution_percentage': 5
			}
        
        with open('./appData.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
		#exit program
        exit(0)

	
	#Open File
    with open("./appData.json") as json_file:
        data = json.load(json_file)
        return data
    
def GetEmployeeData(employeeNum, data):
    	#setup mysql connection
	try:
        #setup connection
		cnx = mysql.connector.connect(user=data['username'], database=data['database_name'], password=data['password'], host=data['host'])
		cursor = cnx.cursor()

        #query database

		query = ("SELECT employee_number, forename, surname, email_address, salary, days_worked_this_month FROM " +
            data['database_table'] + " WHERE employee_number = %s")
		cursor.execute(query, (employeeNum,));

        #debug output
		for (employee_number,forename, surname, email_address, salary, days_worked_this_month) in cursor:
			print("-------------------------------")
			print("Employee num: " + str(employee_number))
			print("Forename: " + forename)
			print("Surname: " + surname)
			print("email addr: " + email_address)
			print("salary: " + str(salary))
			print("Days worked this month: " + str(days_worked_this_month))

            #return employee data
			tempEmployee = Employee(employeeNum, forename, surname, email_address, salary, days_worked_this_month)
   
			cursor.close()
			cnx.close()
   
			return tempEmployee


		#catch error
	except mysql.connector.Error as err:
		cursor.close()
		cnx.close()
  
  ##returns an employee's monthly expenses to be paid back (-1 is error state)
def GetMonthlyExpenses(employeeNum, data):
	cnx = mysql.connector.connect(user=data['username'], database=data['database_name'], password=data['password'], host=data['host'], auth_plugin='mysql_native_password')
	cursor = cnx.cursor()
    
	#get current expenses
	expenses = -1
	try:
		#query database
		query = ("SELECT monthly_expenses FROM " + data['database_table'] + " WHERE employee_number = %s")
		cursor.execute(query, (employeeNum,));
	
		#fetch one row of data
		row = cursor.fetchone()
  
		##check for empty return
		if row is None:
			print("Unable to fetch monthly_expenses for employee: " + employeeNum)
			cursor.close()
			cnx.close()
			return -1
	
		expenses = row[0]
		print("Employee: " + str(employeeNum) + " current expense: " + str(expenses))
	   #error with query
	except mysql.connector.Error as err:
		print("Unable to fetch monthly_expenses for employee: " + employeeNum)
		cursor.close()
		cnx.close()
		return -1

	return expenses;
  
  
  
  #updates the database with new values for monthly expenses
def UpdateMonthlyExpenses(expenseValue, employeeNum, data):
    #setup connection
	cnx = mysql.connector.connect(user=data['username'], database=data['database_name'], password=data['password'], host=data['host'], auth_plugin='mysql_native_password')
	cursor = cnx.cursor()
 
	#get existing expenses and return false if an error occurs
	expenses = GetMonthlyExpenses(employeeNum, data);
	if expenses == -1:
		return False;


	#update value
	expenses += expenseValue
	
	try:
		query = ("UPDATE employees SET monthly_expenses = %s WHERE employee_number = %s")
		cursor.execute(query, (expenses, employeeNum))
		cnx.commit()
		print("Employee: " + str(employeeNum) + " expenses updated to: " + str(expenses))
		
    	#error updating value
	except mysql.connector.Error as err:
		print("Fetched monthly expenese but could not update. employee:  " + employeeNum)
		return False
  
  ##close connection and end
	cursor.close()
	cnx.close()
	return True

 
  #calculates an employee's montly wage
def CalculateMonthlyWage(yearlySalery, daysWorked, employeeNum, data):
	
	#calculate monthly wage before tax using number of days worked and working days in a year
	taxRate = 0.00
	monthlyWageBeforeTax = ((yearlySalery*100 / data['working_days_in_year']) * 
                         daysWorked) * ((100-data['employee_contribution_percentage'])/100)
	
 
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
	temp = temp/100 + GetMonthlyExpenses(employeeNum, data)
   
	#return correct amount
	return float(temp)

#writes an employee's payslip to a file
def WriteEmployeePaylistToFile(employee, data):
	outputString = ("Employee: "+ str(employee.employeeNumber) +
                 "\nForename: " + employee.forename +
                 "\nSurname: " + employee.surname +
                 "\nEmail Addr: " + employee.email_address +
                 "\n------------------------------------------" +
                 "\n\nYearly Salery: " + str(employee.salary) +
                 "\nDays worked (month): " + str(employee.daysWorked) +
                 "\nWage for current month: " + str(CalculateMonthlyWage(employee.salary, employee.daysWorked, employee.employeeNumber, data)))
	f = open("Employee" + employee.employeeNumber + "Payslip", "w")
	f.write(outputString)
	f.close()
 
 
 #validates that an input is an integer
def ValidateInt(input):
    if input.isdigit() or input is "":
        return True
    else:
        return False
 
 
 #validates that an input is a positive only integer   
def ValidatePositiveInt(input):
    #check for int
    if not ValidateInt(input):
        return False;
    
    ##check for positive
    if int(input) < 0:
        return False;
    
    return True;
    
    
