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

def trycall():
    output = subprocess.Popen('python3 main.py \'Wild Yak\' \'Phil McGraw\'',shell=True, stdout=subprocess.PIPE)
    print(output.stdout.read())
    #print(output.find(']'))
    #testarray = ast.literal_eval(output)
    #print(testarray)
    #print(output)
top = Tk()
fields = ('Article 1', 'Article 2')
ents = makeform(top, fields)
top.bind('<Return>', (lambda event, e=ents: fetch(e)))
b1 = Button(top, text='Activate', command=(lambda e=ents: sayhi(e)))
b1.pack(side=LEFT, padx=5, pady=5)
b2 = Button(top, text='Try Command Prompt', command=(lambda: trycall()))
b2.pack(side=LEFT, padx=5, pady=5)
top.mainloop()

