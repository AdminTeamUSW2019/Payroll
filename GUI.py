import tkinter as tk
import Utilities
from tkinter import messagebox
 
 #initialize utilities and get json data
json_data = Utilities.GetDbData()


LARGE_FONT= ("Verdana", 25)
BUTTON_FONT= ("Arial", 15)


class PayrollApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Payroll Application!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Payslip",
                            command=lambda: controller.show_frame(PageOne),
                            font=BUTTON_FONT)
        button.pack()

        button2 = tk.Button(self, text="Expenses",
                            command=lambda: controller.show_frame(PageTwo),
                            font=BUTTON_FONT)
        button2.pack()


class PageOne(tk.Frame):

    #initialization of the page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #object setup
        titleLabel = tk.Label(self, text="Payslip Management", font=LARGE_FONT)

        menuButton = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(StartPage),
                            font=BUTTON_FONT)
        
        searchButton = tk.Button(self, text="Search", font=BUTTON_FONT,
                                  command=lambda: self.Search(forename, surname, yearlySalery, entryBox))
        
        employeeLabel = tk.Label(self, text="Enter employee number", font=BUTTON_FONT)        
        entryBox = tk.Entry(self, text="test") 
        forename = tk.Label(self, text="Forename: ", font=BUTTON_FONT)
        surname = tk.Label(self, text="Surname: ", font=BUTTON_FONT)
        yearlySalery = tk.Label(self, text="Salery: ", font=BUTTON_FONT)
        
        #Grid setup
        titleLabel.grid(row=0, columnspan=3, sticky="E", padx=10, pady=10)
        employeeLabel.grid(row=1, sticky="E")
        entryBox.grid(row=1, column=2, sticky="E")
        forename.grid(row=2, sticky="W", padx=(0, 115), columnspan=3)
        surname.grid(row=3, sticky="W", padx=(0, 115), columnspan=3)
        yearlySalery.grid(row=4, sticky="W", padx=(0, 115), columnspan=3)
        searchButton.grid(row=5, sticky="W")
        menuButton.grid(row=6, sticky="S",columnspan=3, pady=(30, 0), padx=(30, 0))
        
        
    def Search(self, forename, surname, yearlySalery, entryBox):
        #read data from database
        tempEmployee = Utilities.GetEmployeeData(entryBox.get(), json_data);
        
        if tempEmployee is None:
            print("Error: Unable to locate employee in database")
            messagebox.showerror("Error!", "Unable to locate employee in database,\n check the employee number or contact a system admin")
            return
        
        ##update gui
        forename.configure(text="Forename: " + tempEmployee.forename)
        surname.configure(text="Surname: " + tempEmployee.surname)
        yearlySalery.configure(text="Salery: " + str(tempEmployee.salery))
        

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Expense Management", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(StartPage),
                            font=BUTTON_FONT)
        button1.pack(side="left")
        


app = PayrollApp()
app.geometry("400x300")
app.resizable(width=False, height=False)
app.mainloop()