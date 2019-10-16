import tkinter as tk
import Utilities
from tkinter import messagebox
 
 #initialize utilities and get json data
json_data = Utilities.GetJsonData()

##Setup fonts for the GUI
LARGE_FONT= ("Verdana", 25)
BUTTON_FONT= ("Arial", 15)

##GUI Entry point
class PayrollApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        ##setup container for widgets
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #setup all frames for the application
        self.frames = {}
        for F in (MenuPage, PayslipPage, ExpensePage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #select default screen
        self.show_frame(MenuPage)

    #show's specified frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        


  #menu page of the application, can access either payslip screen or expense screen
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        #title
        label = tk.Label(self, text="Payroll Application!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #nav button 1
        button = tk.Button(self, text="Payslip",
                            command=lambda: controller.show_frame(PayslipPage),
                            font=BUTTON_FONT)
        button.pack()

        #nav button 2
        button2 = tk.Button(self, text="Expenses",
                            command=lambda: controller.show_frame(ExpensePage),
                            font=BUTTON_FONT)
        button2.pack()


#Page that handles generating a payslip for the given employee number
class PayslipPage(tk.Frame):
    #initialization of the page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #object setup
        titleLabel = tk.Label(self, text="Payslip Management", font=LARGE_FONT)

        #button to return to menu page
        menuButton = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(MenuPage),
                            font=BUTTON_FONT)
        
        #button to search for employee data
        searchButton = tk.Button(self, text="Search", font=BUTTON_FONT,
                                  command=lambda: self.Search(forename, surname, yearlySalary, entryBox))
        
        #labels
        employeeLabel = tk.Label(self, text="Enter employee number", font=BUTTON_FONT)        
        entryBox = tk.Entry(self) 
        forename = tk.Label(self, text="Forename: ", font=BUTTON_FONT)
        surname = tk.Label(self, text="Surname: ", font=BUTTON_FONT)
        yearlySalary = tk.Label(self, text="Salary: ", font=BUTTON_FONT)
        
        #setup pointer to validation callback function
        validation = self.register(Utilities.ValidateInt)
        
        #Grid setup
        titleLabel.grid(row=0, columnspan=3, sticky="E", padx=10, pady=10)
        employeeLabel.grid(row=1, sticky="E")
        entryBox.grid(row=1, column=2, sticky="E")
        forename.grid(row=2, sticky="W", padx=(0, 115), columnspan=3)
        surname.grid(row=3, sticky="W", padx=(0, 115), columnspan=3)
        yearlySalary.grid(row=4, sticky="W", padx=(0, 115), columnspan=3)
        searchButton.grid(row=5, sticky="W")
        menuButton.grid(row=6, sticky="S",columnspan=3, pady=(30, 0), padx=(30, 0))
        
        ##enable validation on entry box
        entryBox.config(validate="key", validatecommand=(validation, '%S'))
        
    
    #searches for an employee. is bound to searchButton
    def Search(self, forename, surname, yearlySalary, entryBox):
        #read data from database
        tempEmployee = Utilities.GetEmployeeData(entryBox.get(), json_data); #recieve data
        
        #check for corrupted return
        if tempEmployee is None:
            print("Error: Unable to locate employee in database")
            messagebox.showerror("Error!", "Unable to locate employee in database,\n check the employee number or contact a system admin")
            return
        
        ##update gui
        forename.configure(text="Forename: " + tempEmployee.forename)
        surname.configure(text="Surname: " + tempEmployee.surname)
        yearlySalary.configure(text="Salary: " + str(tempEmployee.salary))
        
        Utilities.WriteEmployeePaylistToFile(tempEmployee, json_data['working_days_in_year'])
        

#Screen to add or remove expenses from a employee
class ExpensePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = tk.Label(self, text="Expense Management", font=LARGE_FONT)

        #button to return to the menu page
        menuButton = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(MenuPage),
                            font=BUTTON_FONT)
        
        #button to add expense
        expenseButton = tk.Button(self, text="Update Expenses",
                                  command=lambda: self.UpdateExpenses(int(expenseValueEntry.get()), employeeNumberEntry.get()), font=BUTTON_FONT)
        
        #labels
        lblEmployeeNumber = tk.Label(self, text="Employee Num: ", font=BUTTON_FONT)
        lblExpenseValue = tk.Label(self, text="Expense Value: ", font=BUTTON_FONT)
        
        #Entry boxes
        employeeNumberEntry = tk.Entry(self)
        expenseValueEntry = tk.Entry(self)
        
        #setup pointer to validation callback function
        validationInt = self.register(Utilities.ValidateInt)
        validationPosInt = self.register(Utilities.ValidatePositiveInt)
        
        #configure grid
        titleLabel.grid(row=0, columnspan=3, sticky="E", padx=10, pady=10)
        lblEmployeeNumber.grid(row=1, sticky="W")
        lblExpenseValue.grid(row=2, sticky="W")
        employeeNumberEntry.grid(row=1, column=2, sticky="W")
        expenseValueEntry.grid(row=2, column=2, sticky="W")
        menuButton.grid(row=3, column=0, sticky="NESW")
        expenseButton.grid(row=3, column=2, sticky="NESW")
        
        #setup validation
        employeeNumberEntry.config(validate="key", validatecommand=(validationInt, '%S'))
        expenseValueEntry.config(validate="key", validatecommand=(validationPosInt, '%S'))
    
    #output method for expense button
    def UpdateExpenses(self, employeeNum, expenses):
        #run update method and show error if employee not found or another error occurs, more detailed log will be shown in terminal
        if not Utilities.UpdateMonthlyExpenses(employeeNum, expenses, json_data):
            messagebox.showerror("Error!", "Unable to locate employee in database,\n check the employee number or contact a system admin")

#app config and loop run
app = PayrollApp()
app.geometry("400x300")
app.resizable(width=False, height=False)
app.mainloop()