import matplotlib
import tkinter
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames, asksaveasfilename
from tkinter import colorchooser, Frame
from os import getcwd
from pandas import set_option

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


def pretty_df(df):
    from IPython.display import HTML
    display(HTML(df.to_html()))
    return


def interact_table(dataframe, showtoolbar=True, showstatusbar=True):
    from ..pandastable import Table
    frame = Frame(root)
    pt = Table(frame, dataframe=dataframe, showtoolbar=showtoolbar, showstatusbar=showstatusbar)
    pt.show()
    # root.mainloop()
    return
