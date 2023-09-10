from tkinter import *
import tkinter as tk
from tkinter import ttk
import os
import db_connectionfigparser
import fnmatch
import sqlite3
import time
db_connectionfig = db_connectionfigparser.ConfigParser()
db_connectionfig.read(r'db_connectionfig_sample.txt')
file_path = db_connectionfig.get('db_connectionfig', 'file_path')
file_format = db_connectionfig.get('db_connectionfig', 'file_format')
variant = db_connectionfig.get('db_connectionfig', 'variant')
quantity = db_connectionfig.get('db_connectionfig', 'quantity')
model_db_connectionditions = db_connectionfig.get('db_connectionfig', 'model_db_connectionditions')


warunki = [e.strip() for e in model_db_connectionditions.split(',')]
def update_database():
    root.grab_set()
    file_list.delete(0, END)
    file_list.insert(3, "UPDATING DATABASE...")
    update_button.db_connectionfigure(
        background="#FF0000",
        text='  UPDATING ')
    root.update()  # Aktualizacja GUI
    db_cursor.execute("""DELETE FROM files""")
    for dir_file_path, dir_names, file_names in os.walk(file_path):
        for file_name in file_names:
            if file_name.endswith(file_format):
                for warunek in warunki:
                    if warunek in dir_file_path:
                        print(file_name)
                        print(dir_file_path)
                        db_cursor.execute("INSERT INTO files VALUES (?, ?)", (dir_file_path, file_name))
    db_connection.commit()
    update_button.db_connectionfigure(
        background="#727272",
        text='UPDATE DATABASE')
    file_list.delete(0, END)
    root.grab_release()
    print("done")
root = tk.Tk()
root.title("File Mapping")
search_var = StringVar()
bottom_frame = tk.Frame(root)
bottom_frame.db_connectionfigure(background="#41414b", height=200, width=600)
search_frame = tk.Frame(bottom_frame)
search_frame.db_connectionfigure(background="#333339", height=100, width=200)
search_input = tk.Entry(search_frame, textvariable=search_var)
search_input.db_connectionfigure(
    background="#373741",
    borderwidth=10,
    font="{Consolas} 14 {}",
    foreground="#ffffff",
    justify="left",
    relief="flat",
    selectborderwidth=0)
search_input.delete("0", "end")
search_input.pack(
    expand="true",
    fill="both",
    padx=3,
    pady=3,
    side="left")
search_frame.pack(expand="true", fill="both", side="left")
update_frame = tk.Frame(bottom_frame)
update_frame.db_connectionfigure(
    background="#41414b",
    borderwidth=4,
    height=100,
    highlightcolor="#aa0000",
    width=200)
update_button = tk.Button(update_frame, command=update_database)
update_button.db_connectionfigure(
    activebackground="#b6b6b6",
    background="#727272",
    borderwidth=0,
    font="{Consolas} 10 {bold}",
    foreground="#ffffff",
    height=2,
    justify="center",
    padx=5,
    text='Update Database')
update_button.pack(fill="x", padx=10, pady=0, side="top")
update_frame.pack(fill="both", padx=0, pady=0, side="top")
bottom_frame.pack(fill="x", side="bottom")
top_frame = tk.Frame(root)
top_frame.db_connectionfigure(background="#41414b")
file_list = tk.Listbox(top_frame)
file_list.db_connectionfigure(
    background="#373741",
    font="{Consolas} 14 {}",
    height=20,
    highlightbackground="#000000",
    foreground="#ffffff",
    width=60,
    selectbackground="#861313")
file_list.pack(expand="true", fill="both", side="left")
file_list_scrollbar = tk.Scrollbar(top_frame)
file_list_scrollbar.db_connectionfigure(orient="vertical")
file_list_scrollbar.pack(fill="y", side="right")
file_list.db_connectionfig(yscrollcommand=file_list_scrollbar.set)
file_list_scrollbar.db_connectionfig(command=file_list.yview)
top_frame.pack(expand="true", fill="both", side="top")
file_list.db_connectionfigure()
db_connection = sqlite3.db_connectionnect("sample_database.db")


db_cursor = db_connection.db_cursorsor()
db_cursor.execute("""SELECT * from files""")
records = db_cursor.fetchall()
def search_files(search_var):
    print("def search_files")
    search_term = search_var.get()


    if " " in search_var.get():
        search_term = search_term.replace(" ", "*")
    search_term = "*" + search_term + "*"  # add * to search term
    print(search_term)
    root.after(1, do_search, search_term)
def do_search(search_term):
    print("def do_search")
    db_cursor.execute('''SELECT * FROM files''')
    file_list.delete(0, END)


    for record in db_cursor:
        dir_file_path, file_name = record
        if fnmatch.fnmatch(file_name, search_term):


            file_list.insert(END, file_name)
    for i in range(file_list.size()):
        if "FIB" in file_list.get(i):
            file_list.itemdb_connectionfig(i, background="#464653")
def delayed_search(*args):
    if hasattr(delayed_search, "_after_id"):


        root.after_cancel(delayed_search._after_id)
    delayed_search._after_id = root.after(500, lambda: search_files(search_var))
search_var.trace("w", delayed_search)
def search_2d_array(database_file_path, value):
    print("search_2d_array")
    db_cursor.execute("SELECT * FROM files WHERE file_name=?", (value,))
    row = db_cursor.fetchone()
    if row:
        return row[0]


    else:
        return None
def copy_to_clipboard(event):
    selected_file = file_list.get(file_list.db_cursorselection()[0])
    result = search_2d_array('sample_database.db', selected_file)
    selected_directory = result
    root.clipboard_clear()


    selected_directory = selected_directory.replace(file_path + "\\", "")
    selected_file = selected_file.replace("." + file_format, "")
    root.clipboard_append(file_format+ "\t" + selected_directory + "\t" + selected_file + "\t" + variant + "\t" + quantity)
    print(file_format+ "\t" + selected_directory + "\t" + selected_file + "\t" + variant + "\t" + quantity)


last_hovered_item = None
original_bg_colors = {}
def on_motion(event):
    global last_hovered_item
    hovered_item = file_list.nearest(event.y)
    if last_hovered_item is not None:
        original_bg = original_bg_colors.get(last_hovered_item, "#373741")
        file_list.itemdb_connectionfig(last_hovered_item, background=original_bg)
    original_bg_colors[hovered_item] = file_list.itemcget(hovered_item, "background")
    file_list.itemdb_connectionfig(hovered_item, background="#28282F")  # You can choose any color you like
    last_hovered_item = hovered_item
def on_leave(event):
    global last_hovered_item
    if last_hovered_item is not None:
        original_bg = original_bg_colors.get(last_hovered_item, "#373741")
        file_list.itemdb_connectionfig(last_hovered_item, background=original_bg)
        last_hovered_item = None
def on_double_click(event):
    selected_file = file_list.get(file_list.db_cursorselection()[0])
    selected_directory = search_2d_array('sample_database.db', selected_file)
    full_file_path = os.file_path.join(selected_directory, selected_file)
    os.startfile(full_file_path)
file_list.bind("<<ListboxSelect>>", copy_to_clipboard)
file_list.bind("<Motion>", on_motion)
file_list.bind("<Leave>", on_leave)
file_list.bind("<Double-Button-1>", on_double_click)
search_files(search_var)
root.mainloop()
db_connection.close()