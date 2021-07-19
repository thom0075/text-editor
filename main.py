import os
import time
import tkinter as tk
from threading import Thread
from tkinter import Menu
from tkinter.filedialog import askopenfilename, asksaveasfilename

from win10toast import ToastNotifier

# TODO create auto-save function (DONE)
# TODO create notifier function (DONE)
# TODO create compile function 
# TODO create run file function 
# TODO create the edit text tab (DONE)

# set variable for openfilename
global st_open, font_size
sidebar_color = "Black"
st_open = False
font_size = 12


def send_notification(notification="Notification", alert="Alert!", iconpath=None, no_duration=3):
    toaster = ToastNotifier()
    toaster.show_toast(notification, alert, threaded=True, icon_path=iconpath, duration=no_duration)


def open_file():
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All files", "*.*")])
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    global st_open
    st_open = filepath
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")


def save_file():
    global st_open
    if st_open:
        text_file = open(st_open, "w")
        text_file.write(txt_edit.get(1.0, tk.END))
        text_file.close()
        send_notification("File saved correctly", f"{st_open} - saved", None, 3)
    else:
        save_file_as()


def dark_theme():
    txt_edit.config(fg="white", bg="black")


def light_theme():
    txt_edit.config(fg="black", bg="white")


def refresher():
    pass
    # TODO implement refresher function for syntax highlighting


def save_file_as():
    filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt"), ("All files", "*.*")])
    global st_open
    st_open = False
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
        window.title(f"Simple Text Editor - {filepath}")
        send_notification("File saved correctly", f" Saved as: {filepath}", None, 3)
        st_open = filepath


def auto_save():  # auto save functions
    time.sleep(2)  # auto saves the file every 4 seconds
    global st_open
    if not st_open:
        save_file_as()
    else:
        text_file = open(st_open, "w")
        text_file.write(txt_edit.get(1.0, tk.END))
        text_file.close()
    time.sleep(2)


def auto_save_final():
    while True:
        auto_save()


def show_values():
    print(slider_text_size.get())
    global font_size
    font_size = slider_text_size.get()
    print(f"Font size is set to: {font_size}")
    txt_edit.config(font=("Fira Code", font_size))


def open_edit_text_window():
    global txt_edit
    global font_size
    global newWindow
    global slider_text_size
    newWindow = tk.Toplevel(window)
    newWindow.geometry("150x150")
    newWindow.title("Edit - Font")
    label = tk.Label(master=newWindow, text="Edit text")
    label.grid(row=0, column=0)

    slider_text_size = tk.Scale(newWindow, from_=0, to=200, orient="horizontal")
    button = tk.Button(newWindow, text="Show", command=show_values)
    slider_text_size.grid(row=1, column=0)
    button.grid(row=3, column=0)


def get_color():
    global fr_buttons, sidebar_color, entry_box, sidebar_color
    print(entry_box.get())
    sidebar_color = entry_box.get()
    fr_buttons.config(bg=str(sidebar_color))


def open_personalize_window():
    global entry_box, personalize_window, sidebar_color
    personalize_window = tk.Toplevel(window)
    personalize_window.geometry("200x200")
    personalize_window.title("Edit - Personalize")
    label = tk.Label(master=personalize_window, text="Insert sidebar color")
    label.grid(row=0, column=0)
    entry_box = tk.Entry(master=personalize_window)
    entry_box.grid(row=1, column=0)
    btn_confirm = tk.Button(personalize_window, text="Apply", command=get_color)
    btn_confirm.grid(row=2, column=0)


def compile_file():
    # os.system(f"g++ -o {st_open}")
    try:
        os.system(rf'cmd.exe /k "g++ -o test123 {st_open}"')
    except:
        pass


def run_file():
    try:
        os.system(r'cmd.exe /k "test123.exe"')
    except:
        pass


window = tk.Tk()
window.title("Simple Text Editor")

mn_bar = tk.Menu()  # TODO finish menu

mn_file = Menu(mn_bar, tearoff=0)
mn_edit = Menu(mn_bar, tearoff=0)
mn_cut = Menu(mn_bar, tearoff=0)
mn_copy = Menu(mn_bar, tearoff=0)
mn_paste = Menu(mn_bar, tearoff=0)
mn_settings = Menu(mn_bar, tearoff=0)
mn_about = Menu(mn_bar, tearoff=0)

mn_bar.add_cascade(label="File", menu=mn_file)  # adds the file menu to the main menu
mn_bar.add_cascade(label="Edit", menu=mn_edit)
mn_bar.add_cascade(label="Cut", menu=mn_cut)
mn_bar.add_cascade(label="Copy", menu=mn_copy)
mn_bar.add_cascade(label="Paste", menu=mn_paste)
mn_bar.add_cascade(label="Settings", menu=mn_settings)
mn_bar.add_cascade(label="About", menu=mn_about)

mn_file.add_command(label="Open", command=open_file)  # adds commands to the file menu
mn_file.add_command(label="Save ", command=save_file)
mn_file.add_command(label="Save as", command=save_file_as)

mn_edit.add_command(label="Font", command=open_edit_text_window)
mn_edit.add_command(label="Personalize", command=open_personalize_window)

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)  # create frame and text window
txt_edit.config(font=("Fira Code", int(font_size)))
fr_buttons = tk.Frame(window)
# fr_buttons.config(bg=str(sidebar_color))  # set frame background (not necessary)
btn_open = tk.Button(fr_buttons, text="Compile", command=compile_file)
btn_save = tk.Button(fr_buttons, text="Run file", command=run_file)
click_btn = tk.PhotoImage(r"F:\CODING\text editor\Save_as.png")

btn_light_theme = tk.Button(fr_buttons, text="Light theme ", command=light_theme)
btn_dark_theme = tk.Button(fr_buttons, text="Dark theme ", command=dark_theme)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
btn_light_theme.grid(row=2, column=0, sticky="ew", padx=5)
btn_dark_theme.grid(row=3, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

# font_tuple = ("Fira Code", int(font_size))
t = Thread(target=auto_save_final)
t.start()

window.config(menu=mn_bar)
window.mainloop()

r"""
os.system(r'cmd.exe /k "g++ -o test123  C:\Users\thoma\Desktop\new.cpp"')   #compile the file
os.system(r'cmd.exe /k "test123.exe"')  #execute the file
"""
