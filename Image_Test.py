import tkinter as tk

LARGE_FONT = ("Verdana", 20)


class ImageApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ImagePage):

            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(ImagePage)

        self.show_frame(ImagePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class ImagePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Hello!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


app = ImageApp()
app.geometry("500x500")
app.resizable(width=False, height=False)
app.mainloop()
