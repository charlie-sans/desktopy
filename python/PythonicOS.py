import tkinter as tk
import subprocess
from tkinter import messagebox
import sys
import time
import configparser
import os
import shutil
import datetime
import file


# subprocess.call('setup.py')
#-----------------------------------#
#   welcome to PythonicOS's desktop module
#   this module should not be touched unless you know what your doing and you have a backup of it!
#   this module is the main module of the OS, it is the desktop, it is the thing that you see when you open the OS
#   it has multiple functions that allow you to do things like open files, create files, delete files, and more!
#-----------------------------------#


#----------------------------------#
#   config.ini
#   this is the config file for the desktop
#   it is used to set the desktop's background color, taskbar color, and more!
#----------------------------------#
if os.path.isfile('python/config.ini'):# check if the config file exists
    try:
    # if it does, load it
        config = configparser.ConfigParser()# get the config thing setup
        config.read('python/config.ini')# read the config file to set the desktop! 
# if you want to change the background color or something, modify config.ini
        bkgr = config.get('desktop', 'background')
        tskbr = config.get('desktop', 'taskbar')
        ttl = config.get('desktop', 'title')
        geo = config.get('desktop', 'geometry')
        taskbar_height = config.get('taskbar', 'taskbar_height')
        taskbar_color = config.get('taskbar', 'taskbar_color')
        print("Config loaded.")
    except:
        print("Error loading config.ini. Please check your config.ini file.")
        print("If you do not have a config.ini file, please create one.")
        print("If you do not know how to create a config.ini file, please read the documentation.")
        print("defaluting to built-in confuguration...")
else:
    bkgr = 'darkgray'
tskbr = 'True'
ttl = 'PythonicOS'
geo = '800x600'
taskbar_height = '30'
taskbar_color = 'black'







#----------------------------------#

print("Config loaded.")
time.sleep(1)
print("Loading PythonicOS...")
time.sleep(1)
root = tk.Tk()
root.title(ttl)
root.geometry(geo)

if tskbr == 'True':
    try:
        taskbar = tk.Frame(root, height=taskbar_height, bg=taskbar_color)
        taskbar.pack(side=tk.TOP, fill=tk.X)
    except:
        print("Error loading taskbar. Please check your config.ini file.")
else:
    print("Taskbar disabled. To enable the taskbar, please edit config.ini and set taskbar to True.")
desktop = tk.Frame(root, bg=bkgr)

#----------------------------------#

desktop.pack(expand=True, fill=tk.BOTH)

#-----------------------#

syst = 'sys'
system = 'system'
home_dir = 'system/home'
sys_bin = 'system/bin'
sys_scripts = 'system/scripts'
sys_addr = 'system/addons'
sys_docu = 'system/documents'
sys_hom_usr = 'system/home/user'
sys_hom_usr_doc = 'system/home/user/documents'
sys_hom_usr_doc_pro = 'system/home/user/documents/projects'
sys_logs = 'system/logs'
sys_wel = 'system/welcome'
sys_wel_bin = 'system/welcome/bin'
mount = 'mount'

#---------------------------------#
def start_rename(home_dir, label):
    entry = tk.Entry(label, relief=tk.FLAT)
    entry.insert(0, label.cget("text"))
    entry.bind("<Return>", lambda event, path=home_dir, entry=entry: finish_rename(path, entry))
    entry.bind("<FocusOut>", lambda event, entry=entry: entry.destroy())
    entry.pack()
    entry.select_range(0, tk.END)
    entry.focus()

def finish_rename(home_dir, entry):
    new_filename = entry.get().strip()
    new_home_dir = os.path.join(os.path.dirname(home_dir), new_filename)

    # Close any open file handles
    entry.destroy()

    # Rename the file
    try:
        os.rename(home_dir, new_home_dir)
        load_files(home_dir)
    except PermissionError as e:
        messagebox.showerror("Error", str(e))
        return
    load_files(home_dir)
    if is_pinned(home_dir):
        unpin_from_taskbar(home_dir)
        pin_to_taskbar(new_home_dir)
    load_files(new_home_dir)

def delete_file(home_dir):
    if os.path.isfile(home_dir):
        os.remove(home_dir)
        load_files(home_dir)
        print(f'{home_dir} has been deleted.')
        load_files(home_dir)
def pin_to_taskbar(home_dir):
    if not is_pinned(home_dir):
        taskbar_label = tk.Label(taskbar, text=os.path.basename(home_dir), padx=10)
        taskbar_label.pack(side=tk.LEFT)

        def open_pinned_file(path=home_dir):
            open_file(path)

        taskbar_label.bind("<Button-1>", lambda event: open_pinned_file())
        taskbar_label.bind("<Button-3>", lambda event: show_files_context_menu(event))
        load_files(home_dir)
def open_file(home_dir):
    if home_dir:
        subprocess.Popen(['python', 'system/addons/panno.py', home_dir])
        print(home_dir)
    else:
        print("No file path provided.")

def unpin_from_taskbar(home_dir):
    for widget in taskbar.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("text") == os.path.basename(home_dir):
            widget.destroy()

def find_label(home_dir):
    for widget in desktop.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("text") == os.path.basename(home_dir):
            return widget

def is_pinned(home_dir):
    for widget in taskbar.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("text") == os.path.basename(home_dir):
            return True
    return False

def create_file(home_dir):
    if not os.path.exists(home_dir):
        os.mkdir(home_dir)

    filename = 'file{}.py'.format(len(os.listdir(home_dir)))

    with open(os.path.join(home_dir, filename), 'w') as file:
        file.write('This is the content of {}'.format(filename))
        print("print com1")
    load_files(home_dir)

def show_popup(message):
    popup = tk.Tk()
    popup.wm_title("Popup")
    label = tk.Label(popup, text=message)
    label.pack()
    popup.after(3000, lambda: popup.destroy())  # Close the popup after 3000 milliseconds (3 seconds)
    popup.mainloop()

def show_files_context_menu(event):
    context_menu = tk.Menu(desktop, tearoff=0)

    label = event.widget
    home_dir = os.path.join(os.path.dirname(__file__), 'home', label.cget("text"))

    if not is_pinned(home_dir):
        context_menu.add_command(label='Pin to Taskbar', command=lambda: pin_to_taskbar(home_dir))
    if is_pinned(home_dir):
        context_menu.add_command(label='Unpin from Taskbar', command=lambda: unpin_from_taskbar(home_dir))
    context_menu.add_command(label='Rename', command=lambda: start_rename(home_dir, label))
    context_menu.add_command(label='Refresh', command=lambda: refresh_code())
    context_menu.add_command(label='Delete', command=lambda: (delete_file(home_dir), load_files(home_dir)))
    context_menu.post(event.x_root, event.y_root)

def load_files(home_dir):
    for widget in desktop.winfo_children():
        widget.destroy()

    if not os.path.exists(home_dir):
        os.makedirs(home_dir)

    files = sorted(os.listdir(home_dir))  # Sort files alphabetically
    grid_columns = 9
    grid_row = 0
    grid_column = 0

    for file in files:
        file_path = os.path.join(home_dir, file)
        label = tk.Label(desktop, text=file, pady=10)

        # Get the file extension
        _, extension = os.path.splitext(file_path)

        # Set the background color based on the file extension
        if extension == '.cs':
            label.configure(background='darkblue')
        elif extension == '.html':
            label.configure(background='red')
        elif extension == '.py':
            label.configure(background='yellow')
        elif extension == '.css':
            label.configure(background='blue')
        elif extension == '.js':
            label.configure(background='orange')
        elif extension == '.txt':
            label.configure(background='white')

        grid_column += 1
        if grid_column == grid_columns:
            grid_column = 0
            grid_row += 1

        def open_file_with_path(path):
            open_file(path)

        label.bind("<Button-1>", lambda event, path=file_path: open_file_with_path(path))
        label.bind("<Button-3>", lambda event, path=file_path: show_files_context_menu(event))
        label.grid(row=grid_row, column=grid_column, padx=10, pady=10, sticky='w')

def refresh_code(home_dir):
    load_files(home_dir)

load_files(home_dir)

def show_desktop_context_menu(event):
    global file_context_menu
    file_context_menu = tk.Menu(desktop, tearoff=False)
    home_dir = os.path.join(os.path.dirname(__file__), 'home')

    if not is_pinned(home_dir):
        file_context_menu.add_command(label='Pin to Taskbar', command=lambda: pin_to_taskbar(home_dir))
    if is_pinned(home_dir):
        file_context_menu.add_command(label='Unpin from Taskbar', command=lambda: unpin_from_taskbar(home_dir))

    file_context_menu.add_command(label='New File', command=lambda: create_file(home_dir))
    file_context_menu.add_command(label='Load Files', command=lambda: load_files(home_dir))
    file_context_menu.add_command(label='Refresh', command=lambda: refresh_code(home_dir))
    file_context_menu.add_command(label='Delete', command=lambda: (delete_file(home_dir), load_files(home_dir)))
    file_context_menu.post(event.x_root, event.y_root)

desktop.bind("<Button-3>", show_desktop_context_menu)
load_files(home_dir)
load_files(home_dir)

root.mainloop()

if __name__ =='__main__':
    load_files(home_dir)
