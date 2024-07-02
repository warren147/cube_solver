class RubiksCube:
    def __init__(self):
        # Initialize a solved Rubik's Cube
        self.cube = {
            'F': ['F'] * 9,  # Front face
            'B': ['B'] * 9,  # Back face
            'U': ['U'] * 9,  # Up face
            'D': ['D'] * 9,  # Down face
            'L': ['L'] * 9,  # Left face
            'R': ['R'] * 9   # Right face
        }

    def rotate_face(self, face):
        # Rotate the face 90 degrees clockwise
        face[0], face[1], face[2], face[5], face[8], face[7], face[6], face[3] = \
        face[6], face[3], face[0], face[1], face[2], face[5], face[8], face[7]

    def rotate(self, move):
        # Rotate the appropriate face and adjust adjacent edges
        if move == 'F':
            self.rotate_face(self.cube['F'])
            self.rotate_F_adjacent()
        elif move == 'F\'':
            self.rotate_face(self.cube['F'])
            self.rotate_face(self.cube['F'])
            self.rotate_face(self.cube['F'])
            self.rotate_F_adjacent(reverse=True)
        elif move == 'B':
            self.rotate_face(self.cube['B'])
            self.rotate_B_adjacent()
        elif move == 'B\'':
            self.rotate_face(self.cube['B'])
            self.rotate_face(self.cube['B'])
            self.rotate_face(self.cube['B'])
            self.rotate_B_adjacent(reverse=True)
        elif move == 'U':
            self.rotate_face(self.cube['U'])
            self.rotate_U_adjacent()
        elif move == 'U\'':
            self.rotate_face(self.cube['U'])
            self.rotate_face(self.cube['U'])
            self.rotate_face(self.cube['U'])
            self.rotate_U_adjacent(reverse=True)
        elif move == 'D':
            self.rotate_face(self.cube['D'])
            self.rotate_D_adjacent()
        elif move == 'D\'':
            self.rotate_face(self.cube['D'])
            self.rotate_face(self.cube['D'])
            self.rotate_face(self.cube['D'])
            self.rotate_D_adjacent(reverse=True)
        elif move == 'L':
            self.rotate_face(self.cube['L'])
            self.rotate_L_adjacent()
        elif move == 'L\'':
            self.rotate_face(self.cube['L'])
            self.rotate_face(self.cube['L'])
            self.rotate_face(self.cube['L'])
            self.rotate_L_adjacent(reverse=True)
        elif move == 'R':
            self.rotate_face(self.cube['R'])
            self.rotate_R_adjacent()
        elif move == 'R\'':
            self.rotate_face(self.cube['R'])
            self.rotate_face(self.cube['R'])
            self.rotate_face(self.cube['R'])
            self.rotate_R_adjacent(reverse=True)

    def rotate_F_adjacent(self, reverse=False):
        if reverse:
            # Counterclockwise
            self.cube['U'][6], self.cube['U'][7], self.cube['U'][8], \
            self.cube['R'][0], self.cube['R'][3], self.cube['R'][6], \
            self.cube['D'][2], self.cube['D'][1], self.cube['D'][0], \
            self.cube['L'][8], self.cube['L'][5], self.cube['L'][2] = \
            self.cube['L'][8], self.cube['L'][5], self.cube['L'][2], \
            self.cube['U'][6], self.cube['U'][7], self.cube['U'][8], \
            self.cube['R'][0], self.cube['R'][3], self.cube['R'][6], \
            self.cube['D'][2], self.cube['D'][1], self.cube['D'][0]
        else:
            # Clockwise
            self.cube['U'][6], self.cube['U'][7], self.cube['U'][8], \
            self.cube['R'][0], self.cube['R'][3], self.cube['R'][6], \
            self.cube['D'][2], self.cube['D'][1], self.cube['D'][0], \
            self.cube['L'][8], self.cube['L'][5], self.cube['L'][2] = \
            self.cube['R'][0], self.cube['R'][3], self.cube['R'][6], \
            self.cube['D'][2], self.cube['D'][1], self.cube['D'][0], \
            self.cube['L'][8], self.cube['L'][5], self.cube['L'][2], \
            self.cube['U'][6], self.cube['U'][7], self.cube['U'][8]

    def rotate_B_adjacent(self, reverse=False):
        if reverse:
            # Counterclockwise
            self.cube['U'][0], self.cube['U'][1], self.cube['U'][2], \
            self.cube['L'][0], self.cube['L'][3], self.cube['L'][6], \
            self.cube['D'][8], self.cube['D'][7], self.cube['D'][6], \
            self.cube['R'][8], self.cube['R'][5], self.cube['R'][2] = \
            self.cube['R'][8], self.cube['R'][5], self.cube['R'][2], \
            self.cube['U'][0], self.cube['U'][1], self.cube['U'][2], \
            self.cube['L'][0], self.cube['L'][3], self.cube['L'][6], \
            self.cube['D'][8], self.cube['D'][7], self.cube['D'][6]
        else:
            # Clockwise
            self.cube['U'][0], self.cube['U'][1], self.cube['U'][2], \
            self.cube['L'][0], self.cube['L'][3], self.cube['L'][6], \
            self.cube['D'][8], self.cube['D'][7], self.cube['D'][6], \
            self.cube['R'][8], self.cube['R'][5], self.cube['R'][2] = \
            self.cube['L'][0], self.cube['L'][3], self.cube['L'][6], \
            self.cube['D'][8], self.cube['D'][7], self.cube['D'][6], \
            self.cube['R'][8], self.cube['R'][5], self.cube['R'][2], \
            self.cube['U'][0], self.cube['U'][1], self.cube['U'][2]

    def rotate_U_adjacent(self, reverse=False):
        if reverse:
            # Counterclockwise
            self.cube['F'][0], self.cube['F'][1], self.cube['F'][2], \
            self.cube['R'][0], self.cube['R'][1], self.cube['R'][2], \
            self.cube['B'][0], self.cube['B'][1], self.cube['B'][2], \
            self.cube['L'][0], self.cube['L'][1], self.cube['L'][2] = \
            self.cube['L'][0], self.cube['L'][1], self.cube['L'][2], \
            self.cube['F'][0], self.cube['F'][1], self.cube['F'][2], \
            self.cube['R'][0], self.cube['R'][1], self.cube['R'][2], \
            self.cube['B'][0], self.cube['B'][1], self.cube['B'][2]
        else:
            # Clockwise
            self.cube['F'][0], self.cube['F'][1], self.cube['F'][2], \
            self.cube['R'][0], self.cube['R'][1], self.cube['R'][2], \
            self.cube['B'][0], self.cube['B'][1], self.cube['B'][2], \
            self.cube['L'][0], self.cube['L'][1], self.cube['L'][2] = \
            self.cube['R'][0], self.cube['R'][1], self.cube['R'][2], \
            self.cube['B'][0], self.cube['B'][1], self.cube['B'][2], \
            self.cube['L'][0], self.cube['L'][1], self.cube['L'][2], \
            self.cube['F'][0], self.cube['F'][1], self.cube['F'][2]