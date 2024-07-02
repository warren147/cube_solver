# src/gui.py

import tkinter as tk
from tkinter import messagebox
from cube import RubiksCube
from solver import RubiksCubeSolver

class RubiksCubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube Solver")
        self.cube = RubiksCube()
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for each face of the cube
        faces = ['U', 'L', 'F', 'R', 'B', 'D']
        face_positions = {
            'U': (0, 1),
            'L': (1, 0),
            'F': (1, 1),
            'R': (1, 2),
            'B': (1, 3),
            'D': (2, 1)
        }
        for face in faces:
            frame = tk.Frame(self.root)
            frame.grid(row=face_positions[face][0], column=face_positions[face][1], padx=10, pady=10)
            tk.Label(frame, text=face).grid(row=0, column=1)
            for i in range(9):
                entry = tk.Entry(frame, width=2, justify='center')
                entry.grid(row=(i // 3) + 1, column=(i % 3))
                self.entries[(face, i)] = entry

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_cube)
        solve_button.grid(row=3, column=1, pady=10)

    def solve_cube(self):
        # Read the colors entered by the user into the cube
        for (face, index), entry in self.entries.items():
            color = entry.get().upper()
            if color not in ['W', 'Y', 'R', 'G', 'B', 'O']:
                messagebox.showerror("Error", f"Invalid color {color} at {face}{index}. Please use W, Y, R, G, B, or O.")
                return
            self.cube.cube[face][index] = color

        solver = RubiksCubeSolver(self.cube)
        solver.solve()

        # Display the solved cube state (just printing for simplicity)
        solved_state = self.cube.cube
        for face in solved_state:
            print(f"{face}: {solved_state[face]}")

        messagebox.showinfo("Solved", "The cube has been solved! Check the console for the solved state.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RubiksCubeGUI(root)
    root.mainloop()