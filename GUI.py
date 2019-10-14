import tkinter as tk
import Utilities
 
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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #object setup
        titleLabel = tk.Label(self, text="Payslip Management", font=LARGE_FONT)

        menuButton = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(StartPage),
                            font=BUTTON_FONT)  
        employeeLabel = tk.Label(self, text="Enter employee number", font=BUTTON_FONT)        
        entryBox = tk.Entry(self) 
        forename = tk.Label(self, text="Forename: ", font=BUTTON_FONT)
        surname = tk.Label(self, text="Surname: ", font=BUTTON_FONT)
        
        #Grid setup
        titleLabel.grid(row=0, columnspan=3, sticky="E", padx=10, pady=10)
        employeeLabel.grid(row=1)
        entryBox.grid(row=1, column=2)
        forename.grid(row=2, sticky="E", padx=(0, 115))
        surname.grid(row=3, sticky="E", padx=(0, 115))
        

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
app.geometry("500x300")
app.resizable(width=False, height=False)
app.mainloop()