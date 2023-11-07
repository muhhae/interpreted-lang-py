import customtkinter as ctk
import tkinter as tk
import subprocess

app = ctk.CTk()
app.title("PyHaekal IDE")
app.geometry("1280x720")


frame1 = ctk.CTkFrame(app)
frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

frame2 = ctk.CTkFrame(app)
frame2.grid(row=0, column=1, padx=0, pady=10, sticky="nsew")

frame1.grid_columnconfigure(0, weight=1)

# app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=20)
app.grid_rowconfigure(0, weight=1)

text_box = ctk.CTkTextbox(frame2, activate_scrollbars=True)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_rowconfigure(0, weight=5)
text_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

text_box.cget("font").configure(size=18)
text_box.cget("font").configure(family="fira code")
text_box.configure(undo=True)

current_file = ""


def openFile():
    global current_file
    directory = ctk.filedialog.askopenfiles()
    directory = directory[0].name
    current_file = directory
    # print("current file open", current_file)
    file = open(directory, "r")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", file.read())


def saveFile():
    directory = ctk.filedialog.asksaveasfilename()
    file = open(directory, "w")
    file.write(text_box.get("1.0", "end"))
    file.close()


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
    subprocess.call('start /wait py ./interpreter.py ' +
                    current_file, shell=True)


saveButton = ctk.CTkButton(frame1, text="Save", command=save)
saveButton.grid(row=9, column=0, padx=10, pady=5, sticky="ew")

runButton = ctk.CTkButton(frame1, text="Run", command=runCurrent)
runButton.grid(row=10, column=0, padx=10, pady=5, sticky="ew")

saveFileButton = ctk.CTkButton(frame1, text="Save as", command=saveFile)
saveFileButton.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

openfilebutton = ctk.CTkButton(frame1, text="Open", command=openFile)
openfilebutton.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

for e in [saveButton, runButton, saveFileButton, openfilebutton]:
    e.cget("font").configure(size=14)
    e.cget("font").configure(family="fira code")


# menu_bar = tk.Menu(app, background="#242424", foreground="#ffffff",
#                    activebackground="#242424", activeforeground="#ffffff")
# FileMenu = tk.Menu(menu_bar, tearoff=0, background="#242424", foreground="#ffffff",
#                    activebackground="#242424", activeforeground="#ffffff")
# FileMenu.add_command(label="Open", command=openFile)
# FileMenu.add_command(label="Save", command=save)
# FileMenu.add_command(label="Save as", command=saveFile)

# menu_bar.add_cascade(label="File", menu=FileMenu)
# menu_bar.add_command(label="Run", command=runCurrent)

# menu_bar.config(font=("fira code", 18))
# menu_bar.config(bg="#242424")

# app.config(menu=menu_bar)

app.state("zoomed")
app.mainloop()
