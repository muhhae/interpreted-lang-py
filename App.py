import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as tkmessagebox

import subprocess
import os
from syntax_identifier import syntax_identifier
from LogicOperation import isOpLgc

app = ctk.CTk()
app.title("PyHaekal IDE")
app.geometry("1280x720")

main_frame = ctk.CTkFrame(app)

frame1 = ctk.CTkFrame(main_frame)
frame1.grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="nsew")
frame1.grid_remove()

frame2 = ctk.CTkFrame(main_frame, fg_color="transparent")
frame2.grid(row=2, column=1, padx=(10, 10), pady=(0, 10), sticky="nsew")

folder_frame = ctk.CTkScrollableFrame(frame1)
folder_frame.grid(row=10, column=0, padx=10, pady=10, sticky="nsew")
folder_frame.grid_remove()
frame1.grid_rowconfigure(10, weight=1)

frame1.grid_columnconfigure(0, weight=1)

# app.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=20)
main_frame.grid_rowconfigure(2, weight=1)

text_box = ctk.CTkTextbox(frame2, activate_scrollbars=True)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_rowconfigure(0, weight=3)
text_box.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

text_box.cget("font").configure(size=18)
text_box.cget("font").configure(family="fira code")
text_box.configure(undo=True)


def tab_pressed(event: tk.Event) -> str:
    text_box.insert(tk.INSERT, "    ")
    return "break"


text_box.bind("<Tab>", tab_pressed)

current_file = ""
current_folder = ""


class index_counter:
    def __init__(self):
        self.index = 0

    def reset(self):
        self.index = 0

    def get(self):
        a = self.index
        self.index += 1
        return a


class file_button:
    def __init__(self, name, path, depth, index: index_counter):
        self.label = os.path.basename(path)
        self.path = path
        self.button = ctk.CTkButton(
            folder_frame, text="  " * depth + "  " + name, command=lambda: openFilePath(path))
        self.button.grid(row=index.get(), column=0,
                         padx=2, pady=2, sticky="ew")
        self.button.grid_remove()
        self.button.configure(anchor="w")
        self.button.cget("font").configure(size=14)
        self.button.cget("font").configure(family="fira code")
        self.button.configure(fg_color="transparent")

    def destroy(self):
        self.button.destroy()


class folder_button:
    def __init__(self, name, path, depth, index: index_counter):
        self.index = index
        self.label = os.path.basename(path)
        self.path = path
        self.showed = False
        self.depth = depth
        self.files = []
        self.button = ctk.CTkButton(
            folder_frame, text="  " * depth + "⏵ " + name, command=self.toggle)
        self.button.grid(row=self.index.get(), column=0,
                         padx=2, pady=2, sticky="ew")
        self.button.grid_remove()
        self.listfiles()
        if depth == 0:
            self.button.grid()
            self.show()
        self.button.cget("font").configure(size=14)
        self.button.cget("font").configure(family="fira code")
        self.button.configure(anchor="w")
        self.button.configure(fg_color="transparent")

    def toggle(self):
        if self.showed:
            self.hide()
        else:
            self.show()

    def show(self):
        self.button.configure(text="  " * self.depth + "⏷ " + self.label)
        self.showed = True
        for e in self.files:
            e.button.grid()

    def hide(self):
        self.button.configure(text="  " * self.depth + "⏵ " + self.label)
        for e in self.files:
            if isinstance(e, folder_button):
                e.hide()
            e.button.grid_remove()
        self.showed = False

    def destroy(self):
        self.button.destroy()
        for e in self.files:
            e.destroy()

    def listfiles(self):
        tmp_files = []
        for e in os.listdir(self.path):
            try:
                if os.path.isdir(os.path.join(self.path, e)):
                    self.files.append(folder_button(
                        e, os.path.join(self.path, e), self.depth + 1, self.index))
                else:
                    tmp_files.append(e)
            except:
                continue
        for e in tmp_files:
            self.files.append(file_button(e, os.path.join(
                self.path, e), self.depth + 1, self.index))


current_folder_button = None


def openFolder():
    global current_folder, current_folder_button
    directory = ctk.filedialog.askdirectory()
    if directory == "":
        return
    if current_folder_button != None:
        current_folder_button.destroy()
    current_folder = directory
    current_folder_button = folder_button(
        os.path.basename(directory), directory, 0, index_counter())
    frame1.grid()
    folder_frame.grid()


def refreshFolder():
    global current_folder, current_folder_button
    if current_folder == "":
        return
    if current_folder_button != None:
        current_folder_button.destroy()
    folder_frame.grid()
    current_folder_button = folder_button(
        os.path.basename(current_folder), current_folder, 0, index_counter())
    current_folder_button.show()


def refreshCode():
    current_code = text_box.get('1.0', 'end')
    if current_code.strip() == '':
        return
    insert_cursor = text_box.index(tk.INSERT)
    text_box.delete("1.0", "end")
    word_color = {}
    block = ['fn', 'if', 'while', 'else',
             'else_if', 'end', 'return', 'class', ':']
    for e in block:
        word_color.update({e: 'block'})

    identifier = syntax_identifier()
    identifier.identify_string(current_code)
    for e in identifier.var_list:
        word_color.update({e: 'var'}) if e not in word_color else None
    for e in identifier.funct_list:
        word_color.update({e: 'funct'}) if e not in word_color else None
    for e in identifier.class_list:
        word_color.update({e: 'class'}) if e not in word_color else None
    for e in identifier.label_list:
        word_color.update({e: 'label'}) if e not in word_color else None

    for l, line in enumerate(current_code.split('\n')):
        # print('line', line)
        # stripped = line.lstrip()
        # text_box.insert('end', ' ' * (len(line) - len(stripped)))
        quoted = 0
        tmp = ''
        for i, char in enumerate(line):
            # print('char', char)
            # print('end', line[-1])
            if char == '"':
                quoted += 1
            if quoted % 2 == 1:
                tmp += char
                continue
            separator = [' ', '\t', ',', '(', ')', '[', ']', ':',
                         '.', '=', '+', '/', '*', '-', '^', '%', '<', '>']
            if char in separator or i == len(line) - 1:
                char_in_tmp = False

                if i == len(line) - 1 and char not in separator:
                    char_in_tmp = True
                    tmp += char
                if tmp in word_color:
                    text_box.insert('end', tmp, word_color[tmp])
                elif tmp.isdigit() or tmp == 'NULL':
                    text_box.insert('end', tmp, 'digit')
                elif isOpLgc(tmp):
                    text_box.insert('end', tmp, 'operator')
                else:
                    text_box.insert('end', tmp)
                tmp = ''

                if char_in_tmp:
                    continue

                if char in word_color:
                    text_box.insert('end', char, word_color[char])
                elif isOpLgc(char):
                    text_box.insert('end', char, 'operator')
                elif char in ['[', ']', '=', '.']:
                    text_box.insert('end', char, 'operator')
                else:
                    text_box.insert('end', char)
            else:
                tmp += char
        # print('l', l)
        # print('len', len(current_code.split('\n')) - 2)
        if l < len(current_code.split('\n')) - 2:
            text_box.insert('end', '\n')
    text_box.mark_set(tk.INSERT, insert_cursor)


def openFilePath(path):
    global current_file
    current_file = path
    file = open(path, "r")
    text_box.delete("1.0", "end")
    text_box.insert('1.0', file.read())
    refreshCode()


def openFile():
    global current_file
    directory = ctk.filedialog.askopenfiles()
    if len(directory) == 0:
        return
    current_file = directory[0].name
    openFilePath(current_file)


def saveFile():
    global current_file
    directory = ctk.filedialog.asksaveasfilename()
    if directory == "":
        return
    current_file = directory
    file = open(directory, "w")
    file.write(text_box.get("1.0", "end"))
    file.close()
    refreshFolder()


def save():
    global current_file
    if current_file == "":
        saveFile()
        return
    file = open(current_file, "w")
    file.write(text_box.get("1.0", "end"))
    file.close()


def runCurrent():
    global current_file
    if current_file == "":
        openFile()
    if current_file == "":
        return
    save()
    if current_file != "":
        subprocess.call('start ipython ./interpreter.py ' +
                        current_file, shell=True)


top_level = None


def tes():
    refreshCode()


def menu_action(action):
    if action == "Open File":
        openFile()
    elif action == "Open Folder":
        openFolder()
    elif action == "Save":
        save()
    elif action == "Save as":
        saveFile()
    elif action == "Run":
        runCurrent()
    elif action == "Tes":
        tes()
    menubar.set("Menu")


menu_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
menu_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew", columnspan=2)

runButton = ctk.CTkButton(menu_frame, text="Run", command=runCurrent)
runButton.grid(row=0, column=1, padx=0, pady=10, sticky="w")

runButton.cget("font").configure(size=14)
runButton.cget("font").configure(family="fira code")

menubar = ctk.CTkOptionMenu(menu_frame, bg_color="transparent", values=[
                            "Open File", "Open Folder", "Save", "Save as", "Run", "Tes"], command=menu_action)
menubar.set("Menu")
menubar.configure(font=("fira code", 14))
menubar.configure(dropdown_font=("fira code", 14))
# menubar._dropdown_menu.configure()

menubar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

text_box.tag_config("block", foreground="brown1")
text_box.tag_config("class", foreground="yellow")
text_box.tag_config("funct", foreground="aqua")
text_box.tag_config("var", foreground='orange')
text_box.tag_config("digit", foreground='yellow')
text_box.tag_config("operator", foreground='cadetblue')
text_box.tag_config("label", foreground='brown1')
# text_box.configure(state="disabled")
# text_box.insert("end", "testes", "block")


main_frame.pack(fill=ctk.BOTH, expand=1)
app.after(0, lambda: app.state('zoomed'))


def on_closing():
    if not text_box.get("1.0", "end").strip() == '':
        if tkmessagebox.askokcancel("Save", "Do you want to save your document?"):
            save()
    if tkmessagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()


app.protocol("WM_DELETE_WINDOW", on_closing)

refresh_cycle_delay = 1000


def set_refresh_cycle_delay(x):
    global refresh_cycle_delay
    x = x.replace(' ms', '')
    refresh_cycle_delay = int(x)


delay_label = ctk.CTkLabel(menu_frame, text="Refresh delay :")
delay_label.grid(row=0, column=2, padx=(10, 0), pady=10, sticky="nsew")
delay_label.configure(font=("fira code", 14))


delay_input = ctk.CTkOptionMenu(
    menu_frame, values=['100 ms', '500 ms', '1000 ms', '2000 ms', '3000 ms', '4000 ms', '5000 ms'], command=set_refresh_cycle_delay)
delay_input.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")


def refresh_cycle():
    print('refresh', refresh_cycle_delay)
    refreshCode()
    app.after(refresh_cycle_delay, refresh_cycle)


app.after(refresh_cycle_delay, refresh_cycle)
app.mainloop()
