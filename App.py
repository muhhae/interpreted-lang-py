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
        self.button.configure(text_color=("black", "white"))
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
        self.button.configure(text_color=("black", "white"))
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
    scroll_pos = text_box.yview()
    text_box.delete("1.0", "end")
    word_color = {}
    block = ['fn', 'if', 'while', 'else',
             'else_if', 'end', 'return', 'class', ':', 'import', 'goto']
    for e in block:
        word_color.update({e: 'block'})

    identifier = syntax_identifier(current_folder)
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
        in_comment = False
        for i, char in enumerate(line):
            separator = [' ', '\t', ',', '(', ')', '[', ']', ':',
                         '.', '=', '+', '/', '*', '-', '^', '%', '<', '>']
            if char == '"':
                text_box.insert('end', char, 'quote')
                quoted += 1
                continue
            if quoted % 2 != 0:
                text_box.insert('end', char, 'string')
                continue
            if char == '#':
                in_comment = True
            if in_comment:
                text_box.insert('end', char, 'comment')
                continue
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
    text_box.yview_moveto(scroll_pos[0])


def openFilePath(path):
    save()
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


def save(confirmed=False):
    current_doc = text_box.get("1.0", "end")
    current_doc = current_doc.strip()
    if current_doc == '' and not confirmed:
        return
    global current_file
    if current_file == "":
        saveFile()
        return
    if not os.path.exists(current_file):
        saveFile()
        return
    if open(current_file, "r").read().strip() == current_doc:
        return
    if not confirmed and not tkmessagebox.askyesno("Save", "Do you want to save your code?"):
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
    print('current working directory:', os.getcwd())
    subprocess.call('start ipython -- ./interpreter.py ' +
                    current_file, shell=True)


def run_interactive():
    global current_file
    if current_file == "":
        openFile()
    if current_file == "":
        return
    save()
    subprocess.call('start ipython -- ./interpreter.py -i ' +
                    current_file, shell=True)


def new_file():
    save()
    global current_file
    current_file = ""
    text_box.delete("1.0", "end")
    refreshCode()


def new_folder():
    new_dir = ctk.filedialog.askdirectory()
    if new_dir == "":
        return
    os.mkdir(new_dir)
    refreshFolder()


def tes():
    refreshCode()


def menu_action(action):
    if action == "Open File":
        openFile()
    elif action == "Open Folder":
        openFolder()
    elif action == "Save":
        save(True)
    elif action == "Save as":
        saveFile()
    elif action == "Run":
        runCurrent()
    elif action == "Tes":
        tes()
    elif action == "New File":
        new_file()
    # elif action == "New Folder":
    #     new_folder()
    menubar.set("Menu")


menu_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
menu_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew", columnspan=2)

run_menu = ctk.CTkOptionMenu(menu_frame, values=['Run', 'Run in interactive mode'],
                             command=lambda x: (run_interactive() if x == 'Run in interactive mode'
                                                else runCurrent(), run_menu.set('Run')), width=100)
run_menu.configure(font=("fira code", 14))
run_menu.configure(dropdown_font=("fira code", 14))
run_menu.grid(row=0, column=1, padx=0, pady=10, sticky="nsew")


# runButton = ctk.CTkButton(menu_frame, text="Run", command=runCurrent, width=10)
# runButton.grid(row=0, column=1, padx=0, pady=10, sticky="w")


menubar = ctk.CTkOptionMenu(menu_frame, bg_color="transparent", values=[
                            'New File', "Open File", "Open Folder", "Save", "Save as", "Run", "Tes"], command=menu_action, width=100)
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
text_box.tag_config("comment", foreground='gray')
text_box.tag_config("string", foreground='white')
text_box.tag_config("quote", foreground='orange')
# text_box.configure(state="disabled")
# text_box.insert("end", "testes", "block")

# text_box.tag_config("block", foreground=('brown4', "brown1"))
# text_box.tag_config("class", foreground=('yellow4', "yellow"))
# text_box.tag_config("funct", foreground=('azure', "aqua"))
# text_box.tag_config("var", foreground=('orange4', 'orange'))
# text_box.tag_config("digit", foreground=('yellow4', 'yellow'))
# text_box.tag_config("operator", foreground=('cadetblue4', 'cadetblue'))
# text_box.tag_config("label", foreground=('brown4', 'brown1'))
# text_box.tag_config("comment", foreground=('gray20', 'gray'))
# text_box.tag_config("string", foreground=('black', 'white'))
# text_box.tag_config("quote", foreground=('orange4', 'orange'))


main_frame.pack(fill=ctk.BOTH, expand=1)
app.after(0, lambda: app.state('zoomed'))


def on_closing():
    save()
    if tkmessagebox.askyesno("Quit", "Do you want to quit?"):
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
    menu_frame, values=['100 ms', '500 ms', '1000 ms', '2000 ms', '3000 ms', '4000 ms', '5000 ms'], command=set_refresh_cycle_delay, width=100)
delay_input.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
delay_input.configure(font=("fira code", 14))
delay_input.set('1000 ms')

is_auto_save = False
auto_save_delay = 1000


def set_auto_save_delay(x):
    global auto_save_delay
    x = x.replace(' ms', '')
    auto_save_delay = int(x)


auto_save_delay_input = ctk.CTkOptionMenu(menu_frame, values=[
                                          '100 ms', '500 ms', '1000 ms', '2000 ms', '3000 ms', '4000 ms', '5000 ms'], command=set_auto_save_delay, width=100)
auto_save_delay_input.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")
auto_save_delay_input.configure(font=("fira code", 14))
auto_save_delay_input.set('1000 ms')
auto_save_delay_input.grid_remove() if not is_auto_save else None


def set_auto_save():
    global is_auto_save
    is_auto_save = auto_save_input.get()
    auto_save_delay_input.grid() if is_auto_save else auto_save_delay_input.grid_remove()
    # print(is_auto_save)


auto_save_label = ctk.CTkLabel(menu_frame, text="Auto save")
auto_save_label.grid(row=0, column=4, padx=(10, 0), pady=10, sticky="nsew")
auto_save_label.configure(font=("fira code", 14))

auto_save_input = ctk.CTkSwitch(
    menu_frame, text='', command=set_auto_save, width=20)
auto_save_input.grid(row=0, column=5, padx=(10, 0), pady=10,
                     sticky="nsew")
auto_save_input.configure(font=("fira code", 14))


def refresh_cycle():
    # print('refresh', refresh_cycle_delay)
    refreshCode()
    app.after(refresh_cycle_delay, refresh_cycle)


def auto_save_cycle():
    # print('auto save cycle')
    # print('auto save', is_auto_save)
    if is_auto_save and current_file != "" and text_box.get("1.0", "end").strip() != '':
        print('auto save')
        save(True)
    app.after(auto_save_delay, auto_save_cycle)


def switch_mode():
    ctk.set_appearance_mode('dark' if mode_switch.get() else 'light')
    if mode_switch.get():
        text_box.tag_config("block", foreground="brown1")
        text_box.tag_config("class", foreground="yellow")
        text_box.tag_config("funct", foreground="aqua")
        text_box.tag_config("var", foreground='orange')
        text_box.tag_config("digit", foreground='yellow')
        text_box.tag_config("operator", foreground='cadetblue')
        text_box.tag_config("label", foreground='brown1')
        text_box.tag_config("comment", foreground='gray')
        text_box.tag_config("string", foreground='white')
        text_box.tag_config("quote", foreground='orange')
    else:
        text_box.tag_config("block", foreground='brown4')
        text_box.tag_config("class", foreground='yellow4')
        text_box.tag_config("funct", foreground='blue4')
        text_box.tag_config("var", foreground='orange4')
        text_box.tag_config("digit", foreground='yellow4')
        text_box.tag_config("operator", foreground='cadetblue4')
        text_box.tag_config("label", foreground='brown4')
        text_box.tag_config("comment", foreground='gray20')
        text_box.tag_config("string", foreground='black')
        text_box.tag_config("quote", foreground='orange4')


mode_switch = ctk.CTkSwitch(menu_frame, text='Dark mode', width=20)
mode_switch.grid(row=0, column=7, padx=(10, 0), pady=10, sticky="nsew")
mode_switch.configure(font=("fira code", 14))
mode_switch.configure(command=switch_mode)
mode_switch.toggle()

app.after(auto_save_delay, auto_save_cycle)
app.after(refresh_cycle_delay, refresh_cycle)
app.mainloop()
