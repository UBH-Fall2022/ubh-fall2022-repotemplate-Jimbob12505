from tkinter import *

class GUI:
    def create(self):
        customWindow = Tk()
        customWindow.geometry('500x450')
        customWindow.update_idletasks()

        my_label = Label(customWindow, text='Number of Planets:')
        my_label.pack(pady=20)
        my_text = Text(customWindow, width=30, height=10)
        my_text.pack(pady=20)
        

        customWindow.mainloop()

