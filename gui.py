import tkinter as tk
from saving import saveToExcel
import win32gui
import os
from anki import return_diki_word
import string


def windowonTOP(w, h, x, y):
    def enumHandler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            # print(win32gui.GetWindowText(hwnd))
            if "_OCR_" in win32gui.GetWindowText(hwnd):
                # print(w,h,x,y)
                win32gui.SetWindowPos(hwnd, 0, int(w), int(h), int(x), int(y), 0x0001)
                return True

    win32gui.EnumWindows(enumHandler, None)


def parseTextToString(diki_word):
    output = []  # [("", False)]
    if diki_word is not None:
        for it, tlumaczenie in enumerate(diki_word["tlumaczenia"]):
            output.append(
                [
                    (",".join(tlumaczenie["znaczenie"])).strip(),
                    True if it < 1 else False,
                ]
            )  # + "\n"
    else:
        output = [["Nic tu po mnie", False]]
    # print(output)
    return output


class CEntry(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)

        self.changes = [""]
        self.steps = int()

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut")
        self.context_menu.add_command(label="Copy")
        self.context_menu.add_command(label="Paste")

        self.bind("<Button-3>", self.popup)

        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)

        self.bind("<Key>", self.add_changes)

    def popup(self, event):
        self.context_menu.post(event.x_root, event.y_root)
        self.context_menu.entryconfigure(
            "Cut", command=lambda: self.event_generate("<<Cut>>")
        )
        self.context_menu.entryconfigure(
            "Copy", command=lambda: self.event_generate("<<Copy>>")
        )
        self.context_menu.entryconfigure(
            "Paste", command=lambda: self.event_generate("<<Paste>>")
        )

    def undo(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.delete(0, tk.END)
            self.insert(tk.END, self.changes[self.steps])

    def redo(self, event=None):
        if self.steps < len(self.changes):
            self.delete(0, tk.END)
            self.insert(tk.END, self.changes[self.steps])
            self.steps += 1

    def add_changes(self, event=None):
        if self.get() != self.changes[-1]:
            self.changes.append(self.get())
            self.steps += 1


def showblankcard():
    openWindow(return_diki_word(""))


def openNotFoundWindow():
    root = tk.Tk()
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    MsgBox = tk.messagebox.showerror("Error", "Błąd podczas tłumaczennia")
    if str(MsgBox) == "ok":
        root.destroy()


def openWindow(diki_word):
    global TO_SHOW
    TO_SHOW = parseTextToString(diki_word)
    window = tk.Tk()
    window.title("_OCR_")

    # window.overrideredirect(1)

    message = tk.StringVar()
    # ==========================fUNKCJE#==========================
    import ctypes

    set_to_foreground = ctypes.windll.user32.SetForegroundWindow
    keybd_event = ctypes.windll.user32.keybd_event
    alt_key = 0x12
    extended_key = 0x0001
    key_up = 0x0002

    def steal_focus():
        # print('steal_focus')
        keybd_event(alt_key, 0, extended_key | 0, 0)
        set_to_foreground(window.winfo_id())
        keybd_event(alt_key, 0, extended_key | key_up, 0)

        window.focus_set()

    def wychodzenie(e):
        # os.system('cls')
        # print('Okno zamknięte, oczekiwanie na kolejne..')
        window.destroy()

    def ignore(event):
        # print ("ignore")
        return "break"

    def showAnswer():
        global TO_SHOW
        translation_box["state"] = "normal"
        translation_box.delete("1.0", tk.END)
        for i in range(len(TO_SHOW)):
            # print(TO_SHOW[i][0])
            translation_box.insert(tk.END, TO_SHOW[i][0] + "\n")
            if not TO_SHOW[i][1]:
                translation_box.tag_add("greyy", str(i + 1) + ".0", str(i + 1) + ".end")
                # translation_box.tag_add('color', str(i + 1)+'.0', str(i + 1)+'.end')
        translation_box["state"] = "disabled"
        # print('showans', TO_SHOW)

    def bindit():
        window.bind("<FocusIn>", on_focus_in)
        window.bind("<FocusOut>", on_focus_in)
        # print("Step 3 = ready for more input")

    def saveWord(e):
        global TO_SHOW
        # os.system('cls')
        # print("Saved: ",word_box.get(), '\noczekiwanie na kolejne..')
        if saveToExcel(word_box.get(), TO_SHOW):
            window.destroy()
        else:
            pass
            # print('ERROR')

    def trybwyswietlania(e):
        # brak możliwości edycji
        global TO_SHOW
        window.bind("<FocusIn>", ignore)
        window.bind("<FocusOut>", ignore)
        window.bind("<Return>", saveWord)
        window.bind("<Escape>", wychodzenie)
        window.bind("<Key>", trybedycji)
        translation_box.bind("<Button-1>", checkText)
        # window.focus_force()
        window.after(10, bindit)
        if str(e.keysym) == "Return":
            TO_SHOW = parseTextToString(return_diki_word(word_box.get()))
            showAnswer()
        else:
            word_box.delete(0, "end")
            word_box.insert(0, message.get())
        word_box["state"] = "readonly"
        translation_box["state"] = "disabled"
        # window.bind("<FocusIn>", on_focus_in)
        # window.bind("<FocusOut>", on_focus_in)

    def trybedycji(e):
        # print('trybedycji')
        word_box["state"] = "normal"
        message.set(word_box.get())
        word_box.focus_force()
        window.bind("<Key>", ignore)
        window.bind("<Return>", trybwyswietlania)
        window.bind("<Escape>", trybwyswietlania)

    # uncoment 1!
    # def onClickTag(e):
    #   print(e)
    #   if e.keysym_num > 0 and e.keysym_num < 60000:
    #     print(str(translation_box.index(tk.INSERT)).split('.'))
    #     idx = str(translation_box.index(tk.INSERT)).split('.')
    #     translation_box.tag_add('editt', idx[0] + '.' + str(int(idx[1]) - 1), idx[0] + '.' + idx[1])
    # def editNote(indx):
    #   print(translation_box['state'])
    #   if translation_box['state'] == 'disabled':
    #     window.bind("<Key>", ignore)
    #     window.bind("<KeyPress>", onClickTag)
    #     translation_box.bind("<Button-1>", ignore)
    #     window.bind("<Return>", trybwyswietlania)
    #     window.bind("<Escape>", trybwyswietlania)
    #     translation_box['state'] = 'normal'
    #     translation_box.focus_force()
    #     translation_box.mark_set("insert", "%d.%d" % (indx,0), )
    # uncoment 1!

    def checkText(e):
        # print(e.num)
        indx = int(translation_box.index(f"@0,{e.y}").split(".")[0])
        if e.num == 1:
            TO_SHOW[indx - 1][1] = False if TO_SHOW[indx - 1][1] else True
            showAnswer()

    # uncoment !  /
    # elif e.num == 3:
    #   editNote(indx)
    # uncoment !  /

    def on_focus_in(event):
        window.bind("<FocusIn>", ignore)
        window.bind("<FocusOut>", ignore)
        if str(event) == "<FocusOut event>" and window.focus_get() == None:
            # window.bind('<Button-1>', ignore)
            window.overrideredirect(False)
            # print("I have OUT", event)
        elif str(event) == "<FocusIn event>":
            # window.bind('<Button-1>', checkText)
            # print("I have IN", event)
            window.overrideredirect(1)
            # window.focus_force()
        # print("WAIT")
        window.after(10, bindit)

    # ==========================
    # ==============OKNO============
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = screen_width / 2 - 400 / 2
    y = screen_height / 2 - 200 / 2

    # ==============ELEMENTY============
    # word_box = tk.Label(text = diki_word['word'])
    # word_box.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    # font = "Helvetica 44 bold",justify="center",width=6,bg="#1E6FBA",fg="yellow",disabledbackground="#1E6FBA",disabledforeground="yellow",highlightbackground="black",highlightcolor="red",highlightthickness=1,bd=0
    border = tk.Frame(window, borderwidth=2, bg="#BDD0e7")
    border.pack(fill=tk.BOTH)

    word_box = CEntry(
        border,
        justify="center",
        font=("Arial 17 bold"),
        borderwidth=0,
        bg="#C8A2C8",
        readonlybackground="#BDD0e7",
        selectbackground="#d3d3d3",
        selectforeground="black",
        cursor="dot",
    )
    word_box.insert(tk.END, str(diki_word["word"]))
    word_box["state"] = "readonly"
    word_box.pack(ipady=3, fill=tk.BOTH, side=tk.TOP, expand=True)

    translation_box = tk.Text(
        border,
        font=("Arial 12"),
        borderwidth=0,
        bg="#FEFEF4",
        selectbackground="#d3d3d3",
        selectforeground="black",
        cursor="dot",
    )
    translation_box.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    # translation_box.tag_config('colorr', background="red", foreground="yellow")
    translation_box.tag_config("greyy", foreground="grey")
    translation_box.tag_config("editt", foreground="blue")
    showAnswer()
    # var1 = tk.IntVar()
    # chec = tk.Checkbutton(window, text="male", variable=var1)
    # chec.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    # FEFEF4
    # ==============BINDY============
    # window.bind("<Return>", saveWord)
    window.bind("<Escape>", wychodzenie)
    window.bind("<FocusIn>", on_focus_in)
    window.bind("<FocusOut>", on_focus_in)
    window.bind("<Return>", saveWord)
    window.bind("<Key>", trybedycji)
    translation_box.bind("<Button-1>", checkText)
    # translation_box.bind("<Button-3>", checkText)# uncoment !  /
    # window.bind("E", trybedycji)
    window.protocol("WM_DELETE_WINDOW", window.destroy)
    # windowonTOP(x, y, 450, 200)
    # win32gui.EnumWindows(enumHandler, None)
    # window.lift()
    window.overrideredirect(1)
    window.wm_attributes("-topmost", 1)
    window.geometry("450x200+%d+%d" % (x, y))
    window.wait_visibility()
    window.after(0, lambda: window.attributes("-topmost", False))
    window.after(1, steal_focus)
    window.focus()
    window.mainloop()
