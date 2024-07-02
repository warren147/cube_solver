from src.gui import RubiksCubeGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = RubiksCubeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()