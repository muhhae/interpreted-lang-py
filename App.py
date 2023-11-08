import customtkinter as ctk
import tkinter as tk
import subprocess
import CTkMenuBar.CTkMenuBar as CTkMenuBar
import tkterminal as tkterm
import os

app = ctk.CTk()
app.title("PyHaekal IDE")
app.geometry("1280x720")


frame1 = ctk.CTkFrame(app)
frame1.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

frame2 = ctk.CTkFrame(app, fg_color="transparent")
frame2.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

folder_frame = ctk.CTkScrollableFrame(frame1)
folder_frame.grid(row=10, column=0, padx=10, pady=10, sticky="nsew")
folder_frame.grid_remove()
frame1.grid_rowconfigure(10, weight=1)


frame1.grid_columnconfigure(0, weight=1)

# app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=20)
app.grid_rowconfigure(1, weight=1)

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
            if os.path.isdir(os.path.join(self.path, e)):
                self.files.append(folder_button(
                    e, os.path.join(self.path, e), self.depth + 1, self.index))
            else:
                tmp_files.append(e)
        for e in tmp_files:
            self.files.append(file_button(e, os.path.join(
                self.path, e), self.depth + 1, self.index))
        for e in self.files:
            e.button.cget("font").configure(size=14)
            e.button.cget("font").configure(family="fira code")


current_folder_button = None


def openFolder():
    global current_folder, current_folder_button
    directory = ctk.filedialog.askdirectory()
    if directory == "":
        return
    if current_folder_button != None:
        current_folder_button.destroy()
    folder_frame.grid()
    current_folder = directory
    current_folder_button = folder_button(
        os.path.basename(directory), directory, 0, index_counter())
    current_folder_button.show()


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


def openFilePath(path):
    global current_file
    current_file = path
    file = open(path, "r")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", file.read())


def openFile():
    global current_file
    directory = ctk.filedialog.askopenfiles()
    if len(directory) == 0:
        return
    directory = directory[0].name
    current_file = directory
    # print("current file open", current_file)
    file = open(directory, "r")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", file.read())


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
    save()
    if current_file != "":
        subprocess.call('start /wait py ./interpreter.py ' +
                        current_file, shell=True)


# saveButton = ctk.CTkButton(frame1, text="Save", command=save)
# saveButton.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

runButton = ctk.CTkButton(app, text="Run", command=runCurrent)
runButton.grid(row=0, column=1, padx=0, pady=10, sticky="w")

# saveFileButton = ctk.CTkButton(frame1, text="Save as", command=saveFile)
# saveFileButton.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

# openfilebutton = ctk.CTkButton(frame1, text="Open", command=openFile)
# openfilebutton.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

# openfolderbutton = ctk.CTkButton(
#     frame1, text="Open Folder", command=openFolder)
# openfolderbutton.grid(row=4, column=0, padx=10, pady=5, sticky="ew")


# for e in [saveButton, runButton, saveFileButton, openfilebutton, openfolderbutton]:
#     e.cget("font").configure(size=14)
#     e.cget("font").configure(family="fira code")

runButton.cget("font").configure(size=14)
runButton.cget("font").configure(family="fira code")


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
    menubar.set("Menu")


menubar = ctk.CTkOptionMenu(app, bg_color="transparent", values=[
                            "Open File", "Open Folder", "Save", "Save as", "Run"], command=menu_action)
menubar.set("Menu")
menubar.configure(font=("fira code", 14))
menubar.configure(dropdown_font=("fira code", 14))


menubar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


app.state("zoomed")
app.mainloop()
