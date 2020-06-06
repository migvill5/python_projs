import tkinter as tk
import tkinter.ttk as ttk
from database.pipedb_tinydb.main import PipeWindow

PROJS = ['tinydb-pipedb', 'xml-pipedb', 'fluidpy']


class MainWindow:
    def __init__(self, master=None):
        self.master = master
        master.title('Some python projects')

        # List of widgets
        self.projList = {}
        self.currentProject = None

        # Main frame
        self.frame = tk.LabelFrame(self.master, text='Projects')
        self.frame.grid(column=0, row=0, padx=10)
        # Create controls
        self.loadProjectList()

        # Quit button
        self.btnQuit = tk.Button(text='Quit', command=self.master.quit)
        self.btnQuit.grid(column=0, row=1, sticky="EW")

    def loadProjectList(self):
        i = 0
        for proj in PROJS:
            lblProject = tk.Label(self.frame, text=proj, width=15)
            btnProject = tk.Button(self.frame, text='Open', width=15)
            lblProject.grid(column=0, row=i)
            btnProject.grid(column=1, row=i)
            btnProject.bind('<Button-1>', self.openProject)
            self.projList[proj] = [lblProject, btnProject]
            lblProject = None
            btnProject = None
            i += 1

    def openProject(self, event):
        for proj in self.projList:
            if (str(event.widget) == str(self.projList[proj][1])):
                print('Please wait. Trying to open {} project...'.format(proj))
                self.currentProject = proj

        if self.currentProject == 'tinydb-pipedb':
            pass
            #window = tk.Tk()
            #application = PipeWindow(window)
            # window.mainloop()
