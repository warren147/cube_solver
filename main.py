from tkinter import *
from tkinter import ttk
import solver

if __name__ == "__main__":
    gui = Tk()
    gui.title("Rubik Cube")
    gui.geometry("1366x768")
    ui = ttk.Notebook(gui)
    uiLeft = ttk.Frame(ui)
    uiRight  = ttk.Frame(ui)
    solver.main(uiLeft)
    frame = Frame(uiRight ,width = 950, height = 670)
    frame.place(relx=0.5, rely=0.5,anchor = "center")
    ui.add(uiLeft,text = "Solver")
    ui.pack()
    gui.mainloop()