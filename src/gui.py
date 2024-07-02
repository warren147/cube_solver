import tkinter as tk
from tkinter import messagebox
from cube import RubiksCube
from solver import RubiksCubeSolver

class RubiksCubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube Solver")
        self.cube = RubiksCube()

        self.create_widgets()

    def create_widgets(self):
        # Create widgets for color input
        # Example: Add buttons or entry fields for each face of the cube
        self.entries = {}
        faces = ['F', 'B', 'U', 'D', 'L', 'R']
        for face in faces:
            frame = tk.Frame(self.root)
            frame.pack()
            for i in range(9):
                entry = tk.Entry(frame, width=2)
                entry.grid(row=i//3, column=i%3)
                self.entries[(face, i)] = entry

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_cube)
        solve_button.pack()

    def solve_cube(self):
        for (face, index), entry in self.entries.items():
            self.cube.cube[face][index] = entry.get().upper()

        solver = RubiksCubeSolver(self.cube)
        solver.solve()

        # Display the solution
        messagebox.showinfo("Solution", "The cube has been solved!")

if __name__ == "__main__":
    root = tk.Tk()
    app = RubiksCubeGUI(root)
    root.mainloop()