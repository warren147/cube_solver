from tkinter import *
import solver

if __name__ == "__main__":
    gui = Tk()
    gui.title("Rubik Cube")
    gui.geometry("1056x700")
    uiFrame = Frame(gui)
    uiFrame.pack(fill="both", expand=True)
    solver.main(uiFrame)
    gui.mainloop()