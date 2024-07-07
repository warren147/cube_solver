from tkinter import *
import moves
import cube
import kociemba         

def showSide(cubeSide):
    surrounding = {
        0:"2435",
        1:"2534",
        2:"1405",
        3:"0415",
        4:"2130",
        5:"2031",
    }.get(cubeSide, dispcube)

    cubeSide = columns[cubeSide]
    cubeFace = {
        columns[0]:cube.greenSide,
        columns[1]:cube.blueSide,
        columns[2]:cube.whiteSide,
        columns[3]:cube.yellowSide,
        columns[4]:cube.redSide,
        columns[5]:cube.orangeSide,
    }.get(cubeSide)
    
    n = 0
    for i in range(9):
        colors = {
            "g":columns[0],
            "b":columns[1],
            "w":columns[2],
            "y":columns[3],
            "r":columns[4],
            "o":columns[5],
        }.get(cubeFace[int(n/3)][int(n%3)])
        
        buttons[i].config(bg=colors,state="disabled")
        buttons[i].grid(row=int(n/3),column=int(n%3),padx=2,pady=2)
        n+=1

    Button(dispcube,width=3,height=3,bg=columns[int(surrounding[0])],state=DISABLED).grid(row=0,column=2,pady = 40)  #top
    Button(dispcube,width=3,height=3,bg=columns[int(surrounding[1])],state=DISABLED).grid(row=2,column=4,padx = 40)  #right
    Button(dispcube,width=3,height=3,bg=columns[int(surrounding[2])],state=DISABLED).grid(row=4,column=2,pady = 40)  #bottom
    Button(dispcube,width=3,height=3,bg=columns[int(surrounding[3])],state=DISABLED).grid(row=2,column=0,padx = 40)  #left

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

def reset(opt,mode):
    opt.config(state = "normal")
    opt.delete(0,END)
    opt.config(state = "readonly")
    for i in range(3):
        for j in range(3):
            cube.greenSide[i][j] = Cols[0]
    for i in range(3):
        for j in range(3):
            cube.blueSide[i][j] = Cols[1]
    for i in range(3):
        for j in range(3):
            cube.whiteSide[i][j] = Cols[2]
    for i in range(3):
        for j in range(3):
            cube.yellowSide[i][j] = Cols[3]
    for i in range(3):
        for j in range(3):
            cube.redSide[i][j] = Cols[4]
    for i in range(3):
        for j in range(3):
            cube.orangeSide[i][j] = Cols[5]
    if not mode.get():
        showSide(0)
    else:
        showSide(0)
        edit()

def browse(mode):
    if not mode.get():
        for i in buttons:
            i.config(state="disabled")
    for i in selectors:
        i.config(text = "")

def selected_colors(mode,c):
    browse(mode)
    global selected
    selected = c
    if not mode.get():
        showSide(selected)
    else:
        selectors[c].config(text = "~")

def edit():
    buttons[0].config(state="normal",command=lambda:edit_colors(0))
    buttons[1].config(state="normal",command=lambda:edit_colors(1))
    buttons[2].config(state="normal",command=lambda:edit_colors(2))
    buttons[3].config(state="normal",command=lambda:edit_colors(3))
    buttons[5].config(state="normal",command=lambda:edit_colors(5))
    buttons[6].config(state="normal",command=lambda:edit_colors(6))
    buttons[7].config(state="normal",command=lambda:edit_colors(7))
    buttons[8].config(state="normal",command=lambda:edit_colors(8))
    

def edit_colors(i):
    cur = buttons[4].cget('bg')
    cubeFace = {
        columns[0]:cube.greenSide,
        columns[1]:cube.blueSide,
        columns[2]:cube.whiteSide,
        columns[3]:cube.yellowSide,
        columns[4]:cube.redSide,
        columns[5]:cube.orangeSide,
    }.get(cur)
    cubeFace[int(i/3)][int(i%3)] = Cols[selected]
    buttons[i].config(bg=columns[selected])


def current_state():
    state = ""
    for i in cube.whiteSide:
        for j in i:
            state+=selecttext(j)
    for i in cube.redSide:
        for j in i:
            state+=selecttext(j)
    for i in cube.greenSide:
        for j in i:
            state+=selecttext(j)
    for i in cube.yellowSide:
        for j in i:
            state+=selecttext(j)
    for i in cube.orangeSide:
        for j in i:
            state+=selecttext(j)
    for i in cube.blueSide:
        for j in i:
            state+=selecttext(j)
    return state
     
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

def main(root):
    global columns,Cols,selected,buttons,selectors,dispcube
    columns = ["green","blue","white","yellow","red","orange"]
    Cols = ["g","b","w","y","r","o"]
    selected = 0

    title = LabelFrame(root,padx = 300)
    dispcube = LabelFrame(root,padx = 10,pady = 15,text = "State Of Cube")
    modeSel = LabelFrame(root,padx = 60, pady = 10, text = "Select Mode")
    colorsSel = LabelFrame(root,padx = 35,pady = 10,text = "Pick A Color")
    scramble = LabelFrame(root,text = "Scramble")
    options = LabelFrame(root,text = "Options",padx = 80,pady = 10)
    output = LabelFrame(root,padx = 2, pady = 2,text = "Solution")

    title.grid(row = 0, column = 0, columnspan=2,padx = 10,pady = 10)
    dispcube.grid(row = 1, column = 0, rowspan = 4,padx = 10)
    modeSel.grid(row = 1, column = 1,padx = 10)
    colorsSel.grid(row = 2, column = 1,padx = 10,pady = 5)
    scramble.grid(row = 3, column = 1)
    options.grid(row = 4, column = 1,padx = 10)
    output.grid(row = 5, column = 0,padx = 10,pady = 10)

    Label(title,text = "RUBIK CUBE SOLVER",pady = 3).grid(row = 0, column = 0)

    mode = IntVar()
    Radiobutton(modeSel, text = "Browse Sides", variable = mode, value = 0,command = lambda:browse(mode)).pack(anchor = W)
    Radiobutton(modeSel, text = "Edit Side", variable = mode, value = 1,command = edit).pack(anchor = W)

    selectors = [
        Button(colorsSel,width=3,height=3,bg=columns[0],command=lambda:selected_colors(mode,0)),
        Button(colorsSel,width=3,height=3,bg=columns[1],command=lambda:selected_colors(mode,1)),
        Button(colorsSel,width=3,height=3,bg=columns[2],command=lambda:selected_colors(mode,2)),
        Button(colorsSel,width=3,height=3,bg=columns[3],command=lambda:selected_colors(mode,3)),
        Button(colorsSel,width=3,height=3,bg=columns[4],command=lambda:selected_colors(mode,4)),
        Button(colorsSel,width=3,height=3,bg=columns[5],command=lambda:selected_colors(mode,5)),
    ]

    selectors[0].grid(row=0,column=0,padx=5,pady=2)
    selectors[1].grid(row=0,column=1,padx=5,pady=2)
    selectors[2].grid(row=1,column=0,padx=5,pady=2)
    selectors[3].grid(row=1,column=1,padx=5,pady=2)
    selectors[4].grid(row=2,column=0,padx=5,pady=2)
    selectors[5].grid(row=2,column=1,padx=5,pady=2)

    Button(scramble,width=2,text = "R",command=lambda: [moves.rotateRight(),showSide(selected)]).grid(row = 0, column = 0)
    Button(scramble,width=2,text = "L",command=lambda: [moves.rotateLeft(),showSide(selected)]).grid(row = 0, column = 1)
    Button(scramble,width=2,text = "F",command=lambda: [moves.rotateFront(),showSide(selected)]).grid(row = 0, column = 2)
    Button(scramble,width=2,text = "B",command=lambda: [moves.rotateBack(),showSide(selected)]).grid(row = 0, column = 3)
    Button(scramble,width=2,text = "U",command=lambda: [moves.rotateUp(),showSide(selected)]).grid(row = 0, column = 4)
    Button(scramble,width=2,text = "D",command=lambda: [moves.rotateDown(),showSide(selected)]).grid(row = 0, column = 5)
    Button(scramble,width=2,text = "R'",command=lambda: [moves.rotateRight3(),showSide(selected)]).grid(row = 1, column = 0)
    Button(scramble,width=2,text = "L'",command=lambda: [moves.rotateLeft3(),showSide(selected)]).grid(row = 1, column = 1)
    Button(scramble,width=2,text = "F'",command=lambda: [moves.rotateFront3(),showSide(selected)]).grid(row = 1, column = 2)
    Button(scramble,width=2,text = "B'",command=lambda: [moves.rotateBack3(),showSide(selected)]).grid(row = 1, column = 3)
    Button(scramble,width=2,text = "U'",command=lambda: [moves.rotateUp3(),showSide(selected)]).grid(row = 1, column = 4)
    Button(scramble,width=2,text = "D'",command=lambda: [moves.rotateDown3(),showSide(selected)]).grid(row = 1, column = 5)
    Button(scramble,width=2,text = "R2",command=lambda: [moves.rotateRight2(),showSide(selected)]).grid(row = 2, column = 0)
    Button(scramble,width=2,text = "L2",command=lambda: [moves.rotateLeft2(),showSide(selected)]).grid(row = 2, column = 1)
    Button(scramble,width=2,text = "F2",command=lambda: [moves.rotateFront2(),showSide(selected)]).grid(row = 2, column = 2)
    Button(scramble,width=2,text = "B2",command=lambda: [moves.rotateBack2(),showSide(selected)]).grid(row = 2, column = 3)
    Button(scramble,width=2,text = "U2",command=lambda: [moves.rotateUp2(),showSide(selected)]).grid(row = 2, column = 4)
    Button(scramble,width=2,text = "D2",command=lambda: [moves.rotateDown2(),showSide(selected)]).grid(row = 2, column = 5)

    Button(options,width=10,text="RESET CUBE",command=lambda:reset(opt,mode)).grid(row=0,column=0)
    Button(options,width=17,text="GENERATE SOLUTION",command=lambda:solve(opt)).grid(row=1,column=0)

    opt = Entry(output,width=71,state = "readonly")
    opt.grid(row = 0, column = 0)

    ex = Button(root,text = "EXIT",command = root.destroy)
    ex.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = W+E)

    holder = LabelFrame(dispcube,bg="white")
    holder.grid(row = 1,column = 1, rowspan = 3, columnspan = 3)

    buttons = [
            Button(holder,width=3,height=3),
            Button(holder,width=3,height=3),
            Button(holder,width=3,height=3),
            Button(holder,width=3,height=3),
            Button(holder,width=3,height=3),
            Button(holder,width=3,height=3),
            Button(holder,width=3,height=3),
            Button(holder,width=3,height=3),
            Button(holder,width=3,height=3)
        ]
    showSide(selected)


