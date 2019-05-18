import matplotlib
matplotlib.use('Agg')

import tkinter
from tkinter.filedialog  import askdirectory, askopenfilename, asksaveasfilename
from os import getcwd

root = tkinter.Tk()
root.withdraw()


def ask_open_directory(initialdir=None, title='Select a folder'):
    return askdirectory(parent=root,
                        initialdir=(initialdir or getcwd()),
                        title=title)


def ask_open_file (initialdir=None, title='Select a file', filetypes=None):
    return askopenfilename(parent=root,
                           initialdir=getcwd(),
                           title=title,
                           filetypes=filetypes)


def ask_save_file(initialdir=None, title='Save as', confirmoverwrite=True, defaultextension='.txt'):
    return asksaveasfilename(initialdir=None,
                             title=title,
                             confirmoverwrite=confirmoverwrite,
                             defaultextension=defaultextension)
#
# def pretty_df(df):
#     from IPython.display import HTML
#     display(HTML(df.to_html()))
#     return

