import tkinter as tk
import tkinter.ttk as ttk

PROJS = ['tinydb-pipedb', 'xml-pipedb', 'fluidpy']


class MainWindow:
    def __init__(self, master=None):
        self.master = master
        master.title('Some python projects')
        master.geometry('200x500')
        self.projList = {}
        self.loadProjectList()

    def loadProjectList(self):
        i = 0
        for proj in PROJS:
            lblProject = tk.Label(self.master, text=proj)
            btnProject = tk.Button(self.master, text='Open', )
            lblProject.grid(column=0, row=i)
            btnProject.grid(column=1, row=i)
            self.projList[proj] = [lblProject, btnProject]
            lblProject = None
            btnProject = None
            i += 1
