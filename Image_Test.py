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
        for F in (ImagePage, DummyPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ImagePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class ImagePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.image1 = tk.PhotoImage(file="./British_pound.png")
        label1 = tk.Label(self, image=self.image1)
        label1.pack()


        canv = tk.Canvas(self, width=500, height=500, bg='grey')
        canv.pack()

        canv.create_image(20, 20, anchor='w', image=self.image1)



class DummyPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


app = ImageApp()
app.geometry("500x500")
app.resizable(width=False, height=False)
app.mainloop()
