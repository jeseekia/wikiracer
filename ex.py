from tkinter import *
import subprocess
import ast

def makeform(root, fields):
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width = 22, text = field+": ", anchor='w')
        ent = Entry(row)
        ent.insert(0,"0")
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
    return entries

def sayhi(entries):
    print("Hello")
    print(str(entries['Article 1'].get()))
    print(str(entries['Article 2'].get()))

def trycall(e):
    #output = subprocess.call(['python3 main.py \'Wild yak\' \'Phil McGraw\' > output.txt', '-1'], shell=True)
    output = subprocess.call(['python3 main.py \'' + str(e['Article 1'].get()) + '\' \'' + str(e['Article 2'].get()) + '\' > output.txt', '-1'], shell=True)
    file = open("output.txt", "r")
    parser = file.read()
    #print(parser)
    parser = parser[0 : parser.find("]") + 1]
    testarray = ast.literal_eval(parser)
    box_text = ""
    for i in testarray:
        #print(i)
        box_text += str(i) + ", "
    popupmessage(box_text[0 : len(box_text) - 2])

def popupmessage(path):
    popup = Tk()
    popup.wm_title("Your Results")
    label = Label(popup, text= path)
    label.pack(side="top", fill="x", padx = 10, pady=10)
    B1 = Button(popup, text="Done!", command=popup.destroy)
    B1.pack()
    popup.mainloop()

top = Tk()
top.wm_title("Wikipedia Golf")
fields = ('Article 1', 'Article 2')
ents = makeform(top, fields)
top.bind('<Return>', (lambda event, e=ents: fetch(e)))
b2 = Button(top, text='Find the Link', command=(lambda e=ents: trycall(e)))
b2.pack(side=LEFT, padx=5, pady=5)
top.mainloop()

