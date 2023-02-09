import os
import sys
import pandas as pd
import numpy as np

import tkinter.filedialog
import tkinter.messagebox
import tkinter as tk

import json
import io

PATH = ""
jsonPATH = ".\\config.json"


def Filevalidation(path):
    if path != "" and os.path.isfile(path) and os.access(path, os.R_OK):
        data = pd.read_excel(path, index_col=None)
        # print(data.columns)
        if (len(data.columns) == 2) and {"Word", "Tlumaczenie"}.issubset(data.columns):
            return True
        return False


def newExcelFile(tempdir):
    # print('fun:newExcelFile in ', tempdir)
    df_total = pd.DataFrame(dtype="string", columns=["Word", "Tlumaczenie"])
    # df_total = df_total.append({'Word' : word, 'Tlumaczenie' : tlumaczenie} , ignore_index=True)
    df_total.to_excel(tempdir, index=False, columns=["Word", "Tlumaczenie"])
    if setPATH(tempdir):
        return True


def initPATH():
    global PATH
    if os.path.isfile(jsonPATH) and os.access(jsonPATH, os.R_OK):
        # print ("File exists and is readable")
        with open(jsonPATH) as json_file:
            conf = json.load(json_file)
            # print(conf)
            if Filevalidation(conf["PATH"]):
                PATH = conf["PATH"]
            else:
                with open(jsonPATH, "w") as outfile:
                    json.dump({"PATH": ""}, outfile)
    else:
        # print ("Either file is missing or is not readable, creating file...")
        with io.open(os.path.join(jsonPATH), "w") as db_file:
            db_file.write(json.dumps({"PATH": ""}))


def setPATH(path):
    global PATH
    if Filevalidation(path):
        data = {"PATH": path}
        PATH = path
        with open(jsonPATH, "w") as outfile:
            json.dump(data, outfile)
        return True
    else:
        return False


def ChangeDirWindow(e):
    global PATH

    def newExcelFileName():
        currdir = os.getcwd()
        tempdir = tkinter.filedialog.asksaveasfilename(
            parent=root,
            defaultextension=".xlsx",
            initialdir=currdir,
            title="Save as",
            filetypes=(("Excel file", "*.xlsx"),),
        )
        if len(tempdir) > 0:
            # print ("You chose %s" % tempdir)
            pass
        if newExcelFile(tempdir):
            root.destroy()
        else:
            tkinter.messagebox.showerror("Error", "Błąd podczas tworzenia pliku")

    def ChangeFile_Window():
        currdir = os.getcwd()
        tempdir = tkinter.filedialog.askopenfilename(
            parent=root,
            initialdir=currdir,
            title="Please select a directory",
            defaultextension=".xlsx",
            filetypes=(("Excel file", "*.xlsx"),),
        )
        if len(tempdir) > 0:
            pass
            # print ("You chose %s" % tempdir)
        if setPATH(tempdir):
            # print('zmienianie lokacji') #TODO
            root.destroy()
        else:
            tkinter.messagebox.showerror("Error", "Wybrano niewłaściwy plik")

    root = tk.Tk()
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = 3.7 * screen_width / 4 - 400 / 2
    y = 3.7 * screen_height / 4 - 200 / 2

    win = tk.Toplevel()
    win.protocol("WM_DELETE_WINDOW", root.destroy)
    win.wm_title("Wybór pliku")
    win.geometry("300x80+%d+%d" % (x, y))
    l = tk.Label(win, text="Zmiana pliku zapisu")
    l.pack(fill=tk.X, side=tk.TOP, expand=True)

    b1 = tk.Button(win, text="Utwórz nowy", command=newExcelFileName)
    b1.pack(fill=tk.X, side=tk.LEFT, expand=True)

    b2 = tk.Button(win, text="Wybierz", command=ChangeFile_Window)
    b2.pack(fill=tk.X, side=tk.RIGHT, expand=True)

    root.mainloop()


def init_SaveDir():
    global PATH

    def newExcelFileName():
        currdir = os.getcwd()
        tempdir = tkinter.filedialog.asksaveasfilename(
            parent=root,
            defaultextension=".xlsx",
            initialdir=currdir,
            title="Save as",
            filetypes=(("Excel file", "*.xlsx"),),
        )
        if len(tempdir) > 0:
            # print ("You chose %s" % tempdir)
            pass
        if newExcelFile(tempdir):
            root.destroy()
        else:
            tkinter.messagebox.showerror("Error", "Błąd podczas tworzenia pliku")

    def ChangeFile_Window():
        currdir = os.getcwd()
        tempdir = tkinter.filedialog.askopenfilename(
            parent=root,
            initialdir=currdir,
            title="Please select a directory",
            defaultextension=".xlsx",
            filetypes=(("Excel file", "*.xlsx"),),
        )
        if len(tempdir) > 0:
            pass
            # print ("You chose %s" % tempdir)
        if setPATH(tempdir):
            # print('zmienianie lokacji') #TODO
            root.destroy()
        else:
            tkinter.messagebox.showerror("Error", "Wybrano niewłaściwy plik")

    initPATH()
    # print('Plik zapisu:',PATH)
    if PATH == "":
        root = tk.Tk()
        root.withdraw()

        win = tk.Toplevel()
        win.wm_title("Wybór pliku")
        win.protocol("WM_DELETE_WINDOW", sys.exit)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = screen_width / 2 - 400 / 2
        y = screen_height / 2 - 200 / 2
        win.geometry("300x80+%d+%d" % (x, y))

        l = tk.Label(win, text="Nie wybrano pliku zapisu")
        l.pack(fill=tk.X, side=tk.TOP, expand=True)

        b1 = tk.Button(win, text="Utwórz nowy", command=newExcelFileName)
        b1.pack(fill=tk.X, side=tk.LEFT, expand=True)

        b2 = tk.Button(win, text="Wybierz", command=ChangeFile_Window)
        b2.pack(fill=tk.X, side=tk.RIGHT, expand=True)

        root.mainloop()


def saveToExcel(word, TO_SHOW):
    if PATH != "" and os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        tlumaczenie = " | ".join([wrd[0] for wrd in TO_SHOW if wrd[1]])

        df_total = pd.DataFrame(dtype="string")
        excel_file = pd.ExcelFile(PATH)

        df_total = df_total.append(
            excel_file.parse(sheet_name=excel_file.sheet_names[0]), ignore_index=True
        )
        df_total = df_total.append(
            {"Word": word, "Tlumaczenie": tlumaczenie}, ignore_index=True
        )
        df_total.to_excel(PATH, index=False)
        return True
    else:
        init_SaveDir()
