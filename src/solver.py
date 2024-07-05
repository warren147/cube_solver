from tkinter import *
import moves
import cube
import kociemba         #Install this package "pip install kociemba"


#Display the cube face
def show(side):
    #Gets surrounding faces
    surr = {
        0:"2435",
        1:"2534",
        2:"1405",
        3:"0415",
        4:"2130",
        5:"2031",
    }.get(side,dispcube)

    side = cols[side]

    #Decides which face is to be shown
    face = {
        cols[0]:cube.green,
        cols[1]:cube.blue,
        cols[2]:cube.white,
        cols[3]:cube.yellow,
        cols[4]:cube.red,
        cols[5]:cube.orange,
    }.get(side)
    
    #Place the cubies
    n=0
    for i in range(9):
        colour = {
            "g":cols[0],
            "b":cols[1],
            "w":cols[2],
            "y":cols[3],
            "r":cols[4],
            "o":cols[5],
        }.get(face[int(n/3)][int(n%3)])
        
        buts[i].config(bg=colour,state="disabled")
        buts[i].grid(row=int(n/3),column=int(n%3),padx=2,pady=2)
        n+=1

    #Place the surrounding faces' centers
    Button(dispcube,width=6,height=3,bg=cols[int(surr[0])],state=DISABLED).grid(row=0,column=2,pady = 40)  #top
    Button(dispcube,width=6,height=3,bg=cols[int(surr[1])],state=DISABLED).grid(row=2,column=4,padx = 40)  #right
    Button(dispcube,width=6,height=3,bg=cols[int(surr[2])],state=DISABLED).grid(row=4,column=2,pady = 40)  #bottom
    Button(dispcube,width=6,height=3,bg=cols[int(surr[3])],state=DISABLED).grid(row=2,column=0,padx = 40)  #left

#Solves the current state of cube
def solve(opt):
    opt.config(state = "normal")
    solved = "R L U2 R L' B2 U2 R2 F2 L2 D2 L2 F2"
    try:
        solution = kociemba.solve(current_state())
        opt.delete(0,END)
        if solution == solved:
            opt.insert(0,"Cube already solved")
        else:
            opt.insert(0,solution)
    except:
        opt.delete(0,END)
        opt.insert(0,"INVALID CUBE INPUT")
    opt.config(state = "readonly")

#Resets the cube
def reset(opt,mode):
    opt.config(state = "normal")
    opt.delete(0,END)
    opt.config(state = "readonly")
    for i in range(3):
        for j in range(3):
            cube.green[i][j] = Cols[0]
    for i in range(3):
        for j in range(3):
            cube.blue[i][j] = Cols[1]
    for i in range(3):
        for j in range(3):
            cube.white[i][j] = Cols[2]
    for i in range(3):
        for j in range(3):
            cube.yellow[i][j] = Cols[3]
    for i in range(3):
        for j in range(3):
            cube.red[i][j] = Cols[4]
    for i in range(3):
        for j in range(3):
            cube.orange[i][j] = Cols[5]
    if not mode.get():
        show(0)
    else:
        show(0)
        edit()

#Browse mode
def browse(mode):
    if not mode.get():
        for i in buts:
            i.config(state="disabled")
    for i in selectors:
        i.config(text = "")

#Activates the selected colour
def selected_colour(mode,c):
    browse(mode)
    global selected
    selected = c
    if not mode.get():
        show(selected)
    else:
        selectors[c].config(text = "~")


#Edit mode for a face
def edit():
    buts[0].config(state="normal",command=lambda:edit_colour(0))
    buts[1].config(state="normal",command=lambda:edit_colour(1))
    buts[2].config(state="normal",command=lambda:edit_colour(2))
    buts[3].config(state="normal",command=lambda:edit_colour(3))
    buts[5].config(state="normal",command=lambda:edit_colour(5))
    buts[6].config(state="normal",command=lambda:edit_colour(6))
    buts[7].config(state="normal",command=lambda:edit_colour(7))
    buts[8].config(state="normal",command=lambda:edit_colour(8))
    

#Change the colour of the clicked cubie
def edit_colour(i):
    cur = buts[4].cget('bg')
    face = {
        cols[0]:cube.green,
        cols[1]:cube.blue,
        cols[2]:cube.white,
        cols[3]:cube.yellow,
        cols[4]:cube.red,
        cols[5]:cube.orange,
    }.get(cur)
    face[int(i/3)][int(i%3)] = Cols[selected]
    buts[i].config(bg=cols[selected])


#Read current state of the cube
def current_state():
    state = ""
    for i in cube.white:
        for j in i:
            state+=selecttext(j)
    for i in cube.red:
        for j in i:
            state+=selecttext(j)
    for i in cube.green:
        for j in i:
            state+=selecttext(j)
    for i in cube.yellow:
        for j in i:
            state+=selecttext(j)
    for i in cube.orange:
        for j in i:
            state+=selecttext(j)
    for i in cube.blue:
        for j in i:
            state+=selecttext(j)
    return state

#Convert to kociemba format      
def selecttext(c):
    f = {
        "w":"U",
        "r":"R",
        "y":"D",
        "o":"L",
        "g":"F",
        "b":"B",
    }.get(c)
    return f

