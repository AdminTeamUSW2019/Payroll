import tkinter as tk
from tkinter import messagebox
import Utilities

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
        for F in (LoginPage,MenuPage, PayslipPage, ExpensePage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #select default screen
        self.show_frame(LoginPage)

    #show's specified frame
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


 #menu page of the application, can access either payslip screen or expense screen


    #member function thats pops up a quit message
    def quit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


    #tk.protocol("WM_DELETE_WINDOW", quit()) had to use a function to call this method, if you know how; try and get this to work
    
# Login Page of the application, can access to mainpage if username and password is correct
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._controller = controller


        global username_verify
        global password_verify

        username_verify = tk.StringVar()
        password_verify = tk.StringVar()


        # title label
        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # labels
        label1 = tk.Label(self, text="Username:")
        label1.config(font=("Arial", 15))
        label1.place(x=50, y=120)

        label2 = tk.Label(self, text="Password:")
        label2.config(font=("Arial", 15))
        label2.place(x=50, y=175)

        # Entry Box
        login_box = tk.Entry(self)
        login_box.place(x=170, y=125)
        password_box = tk.Entry(self)
        password_box.place(x=170, y=180)
        
        #image setup
        self.image1 = tk.PhotoImage(file="./Button_Texture2.png")
        
        # button
        self.login_entry = tk.Entry(self)
        self.login_entry.place(x=170, y=125)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.place(x=170, y=180)

        btn_login = tk.Button(self, text="Login", font=BUTTON_FONT, image.self=image1, compound=tk.CENTER, command=self.login_Button)
        btn_login.place(x=200, y=220)

    def login_Button(self):
        # login validation
        if Utilities.login_verification(self.login_entry.get(), self.password_entry.get()):
            self._controller.show_frame(MenuPage)
        else: messagebox.showerror("Error", "Incorrect username or password")
    
  #menu page of the application, can access either payslip screen or expense screen
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #image setup
        self.image1 = tk.PhotoImage(file="./Button_Texture2.png")

        #title
        label = tk.Label(self, text="Payroll Application!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        #nav button 1
        payslipButton = tk.Button(self, text="Payslip",
                            command=lambda: controller.show_frame(PayslipPage),
                            font=BUTTON_FONT, image=self.image1, compound=tk.CENTER)
        payslipButton.pack()

        #nav button 2
        expensesButton = tk.Button(self, text="Expenses",
                            command=lambda: controller.show_frame(ExpensePage),
                            font=BUTTON_FONT, image=self.image1, compound=tk.CENTER)
        expensesButton.pack()

        #exit button
        exitButton = tk.Button(self, text="Quit",

                               command = lambda: controller.quit(),
                               font=BUTTON_FONT, image=self.image1, compound=tk.CENTER)


        exitButton.pack()

#Page that handles generating a payslip for the given employee number
class PayslipPage(tk.Frame):
    #initialization of the page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #object setup
        titleLabel = tk.Label(self, text="Payslip Management", font=LARGE_FONT)

        #image setup
        self.image1 = tk.PhotoImage(file="./Button_Texture2.png")

        #button to return to menu page
        menuButton = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(MenuPage),
                            font=BUTTON_FONT, image=self.image1, compound=tk.CENTER)

        #button to search for employee data
        generateButton = tk.Button(self, text="Generate", font=BUTTON_FONT,
                                   image=self.image1, compound=tk.CENTER,
                                  command=lambda: self.Search(forename, surname, yearlySalary,
                                                               entryBox, expensesText))

        #labels
        employeeLabel = tk.Label(self, text="Enter employee number", font=BUTTON_FONT)
        entryBox = tk.Entry(self)
        forename = tk.Label(self, text="Forename: ", font=BUTTON_FONT)
        surname = tk.Label(self, text="Surname: ", font=BUTTON_FONT)
        yearlySalary = tk.Label(self, text="Salary: ", font=BUTTON_FONT)
        expensesText = tk.Label(self, text="Expenses due: ", font=BUTTON_FONT)
        #setup pointer to validation callback function
        validation = self.register(Utilities.ValidateInt)

        #Grid setup
        titleLabel.grid(row=0, columnspan=3, sticky="E", padx=10, pady=10)
        employeeLabel.grid(row=1, sticky="E")
        entryBox.grid(row=1, column=2, sticky="E")
        forename.grid(row=2, sticky="W", padx=(0, 115), columnspan=3)
        surname.grid(row=3, sticky="W", padx=(0, 115), columnspan=3)
        yearlySalary.grid(row=4, sticky="W", padx=(0, 115), columnspan=3)
        expensesText.grid(row=5, sticky="W")
        generateButton.grid(row=6, sticky="W")
        menuButton.grid(row=6, sticky="S",columnspan=3, pady=(0, 0), padx=(30, 0))

        ##enable validation on entry box
        entryBox.config(validate="key", validatecommand=(validation, '%S'))

    #searches for an employee. is bound to searchButton
    def Search(self, forename, surname, yearlySalary, entryBox, expensesText):
        #read data from database
        tempEmployee = Utilities.GetEmployeeData(entryBox.get(), json_data) #recieve data

        #check for corrupted return
        if tempEmployee is None:
            print("Error: Unable to locate employee in database")
            messagebox.showerror("Error!", "Unable to locate employee in database,\n check the employee number or contact a system admin")
            return

        ##update gui
        forename.configure(text="Forename: " + tempEmployee.forename)
        surname.configure(text="Surname: " + tempEmployee.surname)
        yearlySalary.configure(text="Salary: " + str(tempEmployee.salary))
        expensesText.configure(text="Expenses due: " + str(Utilities.GetMonthlyExpenses(tempEmployee.employeeNumber, json_data)))

        Utilities.WriteEmployeePaylistToFile(tempEmployee, json_data)

#Screen to add or remove expenses from a employee
class ExpensePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        titleLabel = tk.Label(self, text="Expense Management", font=LARGE_FONT)

        #image setup
        self.image1 = tk.PhotoImage(file="./Button_Texture3.png")

        #button to return to the menu page
        menuButton = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(MenuPage),
                            font=BUTTON_FONT, image=self.image1, compound=tk.CENTER)

        #button to add expense
        expenseButton = tk.Button(self, text="Update Expenses",
                                  command=lambda: self.UpdateExpenses(int(expenseValueEntry.get()), employeeNumberEntry.get()), font=BUTTON_FONT,
                                  image=self.image1, compound=tk.CENTER)

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


def close():
    PayrollApp.quit(app)

#app config and loop run
app = PayrollApp()

app.geometry("400x300")

app.resizable(width=False, height=False)

app.protocol("WM_DELETE_WINDOW", close)
app.title("Payrol")

app.mainloop()
