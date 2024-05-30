import tkinter as tk
from tkinter import ttk
import sqlite3

try:
    conn = sqlite3.connect('studentDB')
    cur = conn.cursor()

except sqlite3.Error as e:
    print(f"database connect error: {e}")
    exit()

#테이블 생성
try:
    cur.execute("CREATE TABLE IF NOT EXISTS studentTable (chair_number int PRIMARY KEY, student_number int, name char(15))")

except sqlite3.Error as e:
    print(f"database connect error: {e}")
    pass
    # exit()

def insert_data(chair_number, student_number, name, tree):
    """
    Inserts data into the database table.

    Args:
        chair_number (int): chair number
        student_number (int): student number
        name (str): student name
    """
    try:
        # Remove any existing highlight
        for item in tree.get_children():
            tree.item(item, tags='')  # Clear any existing highlight tag

        # ... rest of the highlight_row function logic ...
    except tk.TclError:
        pass  # Ignore the error if no highlight tag exists
    
    try:
        cur.execute("INSERT INTO studentTable (chair_number, student_number, name) VALUES (?, ?, ?)",
                    (chair_number, student_number, name))
        conn.commit()
        print("Data inserted successfully!")
        # Insert the newly added row directly into the treeview
        tree.insert('', 'end', values=(chair_number, student_number, name))
    except sqlite3.Error as err:
        print("Error:", err)


def highlight_row(tree, chair_number, student_number, name):
    """
    Highlights the row in the Treeview that matches the given information.

    Args:
        tree (ttk.Treeview): The Treeview widget
        
        chair_number (int): The chair number to search for
        student_number (int): The stuent number to search for
        name (str): The student name to search for
    """
    try:
        # Remove any existing highlight
        for item in tree.get_children():
            tree.item(item, tags='')  # Clear any existing highlight tag

        # ... rest of the highlight_row function logic ...
    except tk.TclError:
        pass  # Ignore the error if no highlight tag exists
    

    try:
        cur.execute("SELECT * FROM studentTable WHERE chair_number = ? AND student_number = ? AND name = ? ", (chair_number,student_number,name))
        result = cur.fetchone()
        if result:
            # Found a matching row
            for item in tree.get_children():
                print("1")
                if tree.item(item, 'values')[0] == chair_number:  # Check if User ID matches
                    tree.see(item)  # Scroll to the highlighted row
                    tree.item(item, tags='highlight')
                    return
        else:
            print("No matching row found in the database!")
    except sqlite3.Error as err:
        print("Error:", err)

def show_data_in_table(cur,tree):
    # 데이터 조회
    try:
        cur.execute("SELECT * FROM studentTable")
        results = cur.fetchall()
    except sqlite3.Error as err:
        print("serch error: ",err)

    try:
        # 데이터 삽입
        for row in results:
            tree.insert('', 'end', values=row)
    except sqlite3.Error as err:
        print("serch error2: ",err)
    

def call_procedure(window_title, columns):
    """
    Opens a search window with input fields, buttons, and a Treeview.

    Args:
        window_title (str): Title for the search window
        columns (list of tuples): List of tuples defining Treeview columns (name, width)
    """
    search_window = tk.Tk()
    search_window.title(window_title)
    search_window.geometry("900x350")
    
    # 결과 처리 및 표시
    tree = ttk.Treeview(search_window, columns=[col[0] for col in columns], show="headings")
    show_data_in_table(cur,tree)

    # Input entry fields
    input_name_entry1 = tk.Entry(search_window)
    input_name_entry1.place(x=95, y=10)
    label1=tk.Label(search_window,text="Chair Number")
    label1.place(x=10, y=10)

    input_name_entry2 = tk.Entry(search_window)
    input_name_entry2.place(x=355, y=10) #160
    label1=tk.Label(search_window,text="Student Number")
    label1.place(x=255, y=10)

    input_name_entry3 = tk.Entry(search_window)
    input_name_entry3.place(x=600, y=10)
    label1=tk.Label(search_window,text="Student Name")
    label1.place(x=515, y=10)
    
    # Input button
    call_input_button = tk.Button(
        search_window,
        text="Input",
        command=lambda: [
            insert_data(
                input_name_entry1.get(), 
                input_name_entry2.get(), 
                input_name_entry3.get(), 
                tree
            ),
            # show_data_in_table(cur,tree),
            input_name_entry1.delete(0, tk.END),
            input_name_entry2.delete(0, tk.END),
            input_name_entry3.delete(0, tk.END),
        ],
    )
    call_input_button.place(x=760, y=10)


    call_search_button = tk.Button(
        search_window,
        text="Search",
        command=lambda: [
            highlight_row(
                tree,
                input_name_entry1.get(),
                input_name_entry2.get(),
                input_name_entry3.get()
            ),
            input_name_entry1.delete(0, tk.END),
            input_name_entry2.delete(0, tk.END),
            input_name_entry3.delete(0, tk.END)
        ],
    )
    call_search_button.place(x=820, y=10)

    # Add styling for highlighted row (optional)
    tree.tag_configure('highlight', background='lightblue')
    tree.place(x=10, y=70)
    for col, width in columns:
        tree.column(col, width=width)
        tree.heading(col, text=col)
    
    search_window.mainloop()


# Replace with actual column names for your table
columns = [("chair number", 200), ("student number", 200), ("student name", 200)]

call_procedure("Student attendance", columns)  # Replace