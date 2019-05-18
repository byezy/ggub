import matplotlib
import tkinter
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames, asksaveasfilename
from tkinter import colorchooser, Frame, BOTH
from os import getcwd
from pandas import set_option
from ..pandastable import Table, TableModel

matplotlib.use('Agg')
set_option('display.max_colwidth', -1)
root = tkinter.Tk()
root.withdraw()


def ask_directory(initialdir=None, title='Select a folder'):
    return askdirectory(parent=root,
                        initialdir=(initialdir or getcwd()),
                        title=title)


def ask_open_file(initialdir=None, title='Select a file', filetypes=None):
    return askopenfilename(parent=root,
                           initialdir=(initialdir or getcwd()),
                           title=title,
                           filetypes=filetypes)


def ask_open_files(initialdir=None, title='Select one or more files', filetypes=None):
    return askopenfilename(parent=root,
                           initialdir=(initialdir or getcwd()),
                           title=title,
                           filetypes=filetypes)


def ask_save_file(initialdir=None, title='Save as', confirmoverwrite=True, defaultextension='.txt'):
    return asksaveasfilename(parent=root,
                             initialdir=(initialdir or getcwd()),
                             title=title,
                             confirmoverwrite=confirmoverwrite,
                             defaultextension=defaultextension)


def ask_colour(initialcolor=None):
    rgb_color, web_color = colorchooser.askcolor(parent=root, initialcolor=(initialcolor or (255, 0, 0)))
    return rgb_color, web_color


# def pretty_df(df):
#     from IPython.display import HTML
#     display(HTML(df.to_html()))
#     return


class InteractTable(Frame):
    """Basic test frame for the table"""

    def __init__(self, dataframe, showtoolbar, showstatusbar, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Table View')
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=1)
        # df = TableModel.getSampleData()
        self.table = pt = Table(f, dataframe=dataframe, showtoolbar=showtoolbar, showstatusbar=showstatusbar)
        pt.show()
        return


def interact_table(dataframe, showtoolbar=True, showstatusbar=True):
    app = InteractTable(dataframe, showtoolbar, showstatusbar)
    print("starting loop")
    app.mainloop()
    return
