import customtkinter as ctk
import os

app = ctk.CTk()
app.title("CTk App")
app.geometry("800x600")


frame1 = ctk.CTkFrame(app)
frame1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

frame2 = ctk.CTkFrame(app)
frame2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")


def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)


optionmenu = ctk.CTkOptionMenu(frame1, values=["option 1", "option 2"],
                               command=optionmenu_callback)
optionmenu.set("option 2")
optionmenu.grid(row=0, column=0, padx=5, pady=5, sticky="ew")


def switch_event():
    print("switch toggled, current value:", switch_var.get())


switch_var = ctk.StringVar(value="on")
switch = ctk.CTkSwitch(frame1, text="CTkSwitch", command=switch_event,
                       variable=switch_var, onvalue="on", offvalue="off")

switch.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

tk_textbox = ctk.CTkTextbox(frame1, activate_scrollbars=False)

# create CTk scrollbar
ctk_textbox_scrollbar = ctk.CTkScrollbar(frame1, command=tk_textbox.yview)
# ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

# connect textbox scroll event to CTk scrollbar
tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)
tk_textbox.grid(row=2, column=0, padx=5, pady=5, sticky="ew")


def segmented_button_callback(value):
    print("segmented button clicked:", value)


segemented_button_var = ctk.StringVar(value="Value 1")
segemented_button = ctk.CTkSegmentedButton(frame1, values=["Value 1", "Value 2", "Value 3"],
                                           command=segmented_button_callback,
                                           variable=segemented_button_var,
                                           )
segemented_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")


def slider_event(value):
    print(value)


slider = ctk.CTkSlider(frame1, from_=0, to=100, command=slider_event)
slider.grid(row=4, column=0, padx=5, pady=5, sticky="ew")


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)


label = ctk.CTkLabel(frame1, text="ComboBox", fg_color="transparent")
label.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
combobox = ctk.CTkComboBox(frame1, values=["option 1", "option 2"],
                           command=combobox_callback)
combobox.set("option 2")
combobox.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

frame1.grid_columnconfigure(0, weight=1)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=10)
app.grid_rowconfigure(0, weight=1)

text_box = ctk.CTkTextbox(frame2, activate_scrollbars=True)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_rowconfigure(0, weight=5)
text_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

text_box.cget("font").configure(size=18)
text_box.cget("font").configure(family="fira code")


def openFile():
    directory = ctk.filedialog.askopenfiles()
    directory = directory[0].name
    file = open(directory, "r")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", file.read())


def saveFile():
    directory = ctk.filedialog.asksaveasfilename()
    # print(directory)
    file = open(directory, "w")
    file.write(text_box.get("1.0", "end"))
    file.close()


def runCurrent():
    os.system("pwsh py interpreter.py")


runButton = ctk.CTkButton(frame1, text="Run Current", command=runCurrent)
runButton.grid(row=9, column=0, padx=5, pady=5, sticky="ew")

saveFileButton = ctk.CTkButton(frame1, text="Save File", command=saveFile)
saveFileButton.grid(row=8, column=0, padx=5, pady=5, sticky="ew")

openfilebutton = ctk.CTkButton(frame1, text="Open File", command=openFile)
openfilebutton.grid(row=7, column=0, padx=5, pady=5, sticky="ew")

app.state("zoomed")
app.mainloop()
