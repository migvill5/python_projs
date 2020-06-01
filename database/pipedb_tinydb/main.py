from tkinter import ttk
import tkinter as tk
from tkinter import *
from tinydb import TinyDB, Query, where

import os

DIRPATH = os.path.dirname(os.path.realpath(__file__))

# FIXME: When you try to edit a record the table of that specific
# record, it has to be show in the option menu as well.


class PipeWindow:

    db = TinyDB(os.path.join(DIRPATH, "data\\data.json"))
    table_info = {'idx': 0, 'value': ''}

    def __init__(self, window):
        self.wind = window
        self.wind.title('PIPE DATABASE')
        self.opm_var = StringVar()
        self.c_item = ''
        self.edit_std = False
        self.old_pipeid = ''

        # WIDGET CREATION
        frame = LabelFrame(self.wind, text='Register new pipe')
        # Table
        self.lbl_table = Label(frame, text='Table: ')
        self.opm_var.set(list(self.db.tables())[0])
        self.opm_table = OptionMenu(frame, self.opm_var, *self.db.tables())
        self.btn_table = Button(frame, text='+/-', command=self.__edit_table)
        # Pipe ID
        self.lbl_id = Label(frame, text='PIPE ID: ')
        self.idpipe = Entry(frame)
        self.idpipe.focus()
        # NPS entry
        self.lbl_nps = Label(frame, text='NPS [in]: ')
        self.nps = Entry(frame)
        # DN entry
        self.lbl_dn = Label(frame, text='DN [mm]: ')
        self.dn = Entry(frame)
        # Outside diameter
        self.lbl_outd = Label(frame, text='Outside diameter [mm]: ')
        self.outd = Entry(frame)
        # Inside Diameter
        self.lbl_ind = Label(frame, text='Inside Diameter [mm]: ')
        self.ind = Entry(frame)
        # Add button
        self.btn_add = Button(frame, text='SAVE PIPE',
                              command=self.__save_pipe)

        # Message label
        self.lbl_mssg = Label(text='msg-txt', fg='red')
        # Table
        self.tbl_data = ttk.Treeview(height=10, columns=4)
        self.tbl_data['columns'] = ('NPS', 'DN', 'OD', 'ID')
        self.tbl_data.column('#0', width=200)
        self.tbl_data.column('NPS', width=100)
        self.tbl_data.column('DN', width=100)
        self.tbl_data.column('OD', width=100)
        self.tbl_data.column('ID', width=100)
        self.tbl_data.heading('#0', text='PIPE ID')
        self.tbl_data.heading('NPS', text='NPS')
        self.tbl_data.heading('DN', text='DN')
        self.tbl_data.heading('OD', text='OD')
        self.tbl_data.heading('ID', text='ID')

        # DELETE/EDIT button
        self.btn_del = Button(text='DELETE', command=self.__delete_pipe)
        self.btn_edit = Button(text='EDIT', command=self.__edit_pipe)

        # WIDGET's PLACEMENT
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        # Table list
        self.lbl_table.grid(row=1, column=0)
        self.opm_table.grid(row=1, column=1)
        self.btn_table.grid(row=1, column=2)
        # Pipe ID
        self.lbl_id.grid(row=2, column=0)
        self.idpipe.grid(row=2, column=1)
        # NPS entry
        self.lbl_nps.grid(row=3, column=0)
        self.nps.grid(row=3, column=1)
        # DN entry
        self.lbl_dn.grid(row=4, column=0)
        self.dn.grid(row=4, column=1)
        # Outside diameter
        self.lbl_outd.grid(row=5, column=0)
        self.outd.grid(row=5, column=1)
        # Inside Diameter
        self.lbl_ind.grid(row=6, column=0)
        self.ind.grid(row=6, column=1)
        # Add button
        self.btn_add.grid(row=7, columnspan=3, sticky=W+E)
        # Message label
        self.lbl_mssg.grid(row=2, column=0, columnspan=2, sticky=W+E)
        # Table
        self.tbl_data.grid(row=3, column=0, columnspan=2)
        # DELETE butto
        self.btn_del.grid(row=4, column=0, sticky=W+E)
        self.btn_edit.grid(row=4, column=1, sticky=W+E)

        # Binding events
        self.tbl_data.bind('<ButtonRelease-1>', self.select_item)

        # Fill table
        self.__get_data()

    # Function to get data from database
    def __get_data(self):

        # Clean table
        records = self.tbl_data.get_children()
        for elem in records:
            self.tbl_data.delete(elem)

        # Getting data
        for table_name in self.db.tables():
            table = self.db.table(table_name)
            tbl = self.tbl_data.insert('', 1, text=table_name)

            for row in table:
                self.tbl_data.insert(tbl, 'end', text=row['_id'],
                                     value=(row['_nps'], row['_dn'], row['_outd'],
                                            row['_ind']))

    # Function to save newe pipe
    def __save_pipe(self):
        if self.validation():
            table = self.db.table(self.opm_var.get())
            if self.edit_std is False:
                # Create a new record in a table
                table.insert({'_id': self.idpipe.get(),
                              '_nps': self.nps.get(),
                              '_dn': self.dn.get(),
                              '_outd': self.outd.get(),
                              '_ind': self.ind.get()})
            else:
                # TODO: Update a existent record on a table.
                print(self.old_pipeid)
                table.update({'_id': self.idpipe.get(),
                              '_nps': self.nps.get(),
                              '_dn': self.dn.get(),
                              '_outd': self.outd.get(),
                              '_ind': self.ind.get()}, where('_id') == self.old_pipeid)
                self.edit_std = False

            self.clear_entries()
            self.__get_data()
        else:
            self.lbl_mssg.configure(
                text='Some info is needed to save a pipe. Please fill all form entries.')

    def validation(self):
        # Checking of empty entries
        return (len(self.nps.get()) != 0) and (len(self.dn.get()) != 0) and \
            (len(self.outd.get()) != 0) and (
                len(self.ind.get()) != 0) and (len(self.idpipe.get()) != 0)

    # Function to delete a pipe
    def __delete_pipe(self):
        # TODO: Delete tables and records inside tables
        record = Query()
        if self.c_item != '':
            if self.c_item['values'] != '':
                try:
                    print(record._id.search(self.c_item['text']))
                except:
                    pass

                self.__get_data()
            else:
                self.lbl_mssg.configure(
                    text='Please select a pipe record to be edited.')
        else:
            self.lbl_mssg.configure(
                text="There's no selection. Please select a pipe record to be edited.")

    # Function to edit a pipe
    def __edit_pipe(self):
        if self.c_item != '':                   # Checking no selection
            if self.c_item['values'] != '':     # Checking if pipe was selected
                self.edit_std = True
                # Create var to modify entries content
                v_id = StringVar()
                v_nps = StringVar()
                v_dn = StringVar()
                v_outd = StringVar()
                v_ind = StringVar()
                # Assign of content vars
                self.idpipe.configure(text=v_id)
                self.nps.configure(text=v_nps)
                self.dn.configure(text=v_dn)
                self.outd.configure(text=v_outd)
                self.ind.configure(text=v_ind)
                # Change entries' content
                v_id.set(self.c_item['text'])
                v_nps.set(self.c_item['values'][0])
                v_dn.set(self.c_item['values'][1])
                v_outd.set(self.c_item['values'][2])
                v_ind.set(self.c_item['values'][3])

                self.old_pipeid = self.c_item['text']
            else:
                self.lbl_mssg.configure(
                    text='Please select a pipe record to be edited.')
        else:
            self.lbl_mssg.configure(
                text="There's no selection. Please select a pipe record to be edited.")

    # Function to call tab edition window
    def __edit_table(self):
        self.new_window = tk.Toplevel(self.wind)
        self.__table_wind = TableWindow(self.new_window)

    # Function binded to treeview
    def select_item(self, event):
        self.c_item = self.tbl_data.item(self.tbl_data.focus())

    def clear_entries(self):
        self.idpipe.delete(0, 'end')
        self.nps.delete(0, 'end')
        self.dn.delete(0, 'end')
        self.outd.delete(0, 'end')
        self.ind.delete(0, 'end')


class TableWindow:

    def __init__(self, master):
        self.master = master

        self.frame = LabelFrame(self.master, text='Register table')
        self.frame_controls = LabelFrame(self.frame, text='Controls')
        self.lst_table = Listbox(self.frame)
        self.table_name = Entry(self.frame_controls)
        self.btn_save = Button(self.frame_controls,
                               text='ADD', command=self.__add_table)
        self.btn_delete = Button(
            self.frame_controls, text='DELETE', command=self.__delete_table)

        self.frame.grid(row=0, column=0)
        self.lst_table.grid(row=0, column=0)
        self.frame_controls.grid(row=0, column=1, pady=0)
        self.table_name.grid(row=1, column=0, pady=10)
        self.btn_save.grid(row=2, column=0, sticky=E+W)
        self.btn_delete.grid(row=3, column=0, sticky=E+W)

        self.lst_table.bind('<<ListboxSelect>>', self.on_select)

        self.__get_data()

    def __get_data(self):
        if self.validation():
            self.lst_table.insert(0, *PipeWindow.db.tables())
        else:
            pass

    def __add_table(self):
        PipeWindow.db.table(self.table_name.get())
        print('{} was inserted...'.format(self.table_name.get()))
        self.lst_table.delete(0, 'end')
        self.table_name.delete(0, 'end')
        self.__get_data()

    def __delete_table(self):
        PipeWindow.db.purge_table(self.table_name.get())
        self.lst_table.delete(0, 'end')
        self.table_name.delete(0, 'end')
        self.__get_data()

    def validation(self):
        return (len(PipeWindow.db.tables()) != 0)

    def on_select(self, evt):
        try:
            w = evt.widget
            PipeWindow.table_info['idx'] = int(w.curselection()[0])
            PipeWindow.table_info['value'] = w.get(
                PipeWindow.table_info['idx'])
            v = StringVar()
            self.table_name.configure(textvariable=v)
            v.set(PipeWindow.table_info['value'])
        except:
            pass


if __name__ == "__main__":
    window = Tk()
    application = PipeWindow(window)
    window.mainloop()
