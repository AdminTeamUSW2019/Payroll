#imports
from enum import Enum
import Utilities
from tkinter import *
import tkinter.font as font

#scene enum
class Scene(Enum):
	MAIN_MENU = 0
	PAYSLIP_SCREEN = 1
	EXPENSES_SCREEN = 2
 
 #initialize utilities and get json data
json_data = Utilities.GetDbData()

#draw window
window = Tk()
window.title("Payroll App")
window.geometry('800x600')
window.resizable(width = False, height = False)
window.configure(background='black')

#setup font
mainFont = font.Font(family="Helvetica", size=40, weight="bold")




#event loop
window.mainloop()
