import tkinter as tk
from tkinter import filedialog
import website_processing
from tkinter import messagebox
import sys

# Constants
WEBSITE_LIST_TITLE = "Select Website List File"
KEYWORD_LIST_TITLE = "Select Keyword List File"
OUTPUT_FILE_TITLE = "Select Output File"
TEXT_FILETYPES = [("Text files", "*.txt")]


def browse_file(entry, title):
    file_path = filedialog.askopenfilename(title=title, filetypes=TEXT_FILETYPES)
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


def browse_website_list():
    browse_file(website_list_entry, WEBSITE_LIST_TITLE)


def browse_keyword_list():
    browse_file(keyword_list_entry, KEYWORD_LIST_TITLE)


def browse_output_file():
    output_file_path = filedialog.asksaveasfilename(title=OUTPUT_FILE_TITLE, defaultextension=".txt",
                                                    filetypes=TEXT_FILETYPES)
    if output_file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, output_file_path)


def process_files():
    websites = website_list_entry.get()
    keywords = keyword_list_entry.get()
    output_name = output_file_entry.get()

    err_msg_wrong_path = "Enter valid text file paths for keywords and website list!"
    err_msg_wrong_extension = "Please make sure your output file ends in .xlsx!"
    err_msg_processing_failed = "Website processing has failed! Try again or contact program creator."
    success_msg = "Data has been scraped and prcoessed. See output Excel file!"

    empty_label = tk.Label(root, text="Enter valid text file paths for keywords and website list", fg='red')

    if not websites or not keywords:
        # empty_label.grid(row=3, column=1, columnspan=2)  # Place the label in a visible area
        messagebox.showerror(title="Invalid File Path", message=err_msg_wrong_path)
        return

    if not output_name.lower().endswith(".xlsx"):
        messagebox.showerror(title="Invalid File Extension", message=err_msg_wrong_extension)
        return

    # If we reach this point, valid file paths were entered
    # So, we can remove the error message if it exists
    try:
        empty_label.grid_forget()

    except NameError:
        pass  # empty_label was not defined, so there's no need to remove it

    output_file_name = output_file_entry.get()

    process_result = website_processing.scrape_sites(user_provided_sites=websites, user_provided_keywords=keywords,
                                                     output_file_name=output_file_name.lower())

    if process_result == 1:
        messagebox.showerror(title="An error has occurred!", message=err_msg_processing_failed)

    if process_result == 0:
        messagebox.showinfo(title="Success", message=success_msg)


# Create the main Tkinter window
root = tk.Tk()

img = tk.PhotoImage(file='RPG_Favicon.png')
root.iconphoto(True, img)

root.title("RPG Procurement Web Scraping")

root.geometry("500x200")

root.resizable = (False, False)

# set minimum window size value
root.minsize(500, 200)

# set maximum window size value
root.maxsize(500, 200)

# Create a frame
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Create website list selection
website_list_label = tk.Label(frame, text="Website List:")
website_list_label.grid(row=0, column=0, padx=10, pady=5)
website_list_entry = tk.Entry(frame, width=40)
website_list_entry.grid(row=0, column=1, padx=10, pady=5)
website_list_browse_button = tk.Button(frame, text="Browse", command=browse_website_list)
website_list_browse_button.grid(row=0, column=2, padx=5, pady=5)

# Create keyword list selection
keyword_list_label = tk.Label(frame, text="Keyword List:")
keyword_list_label.grid(row=1, column=0, padx=10, pady=5)
keyword_list_entry = tk.Entry(frame, width=40)
keyword_list_entry.grid(row=1, column=1, padx=10, pady=5)
keyword_list_browse_button = tk.Button(frame, text="Browse", command=browse_keyword_list)
keyword_list_browse_button.grid(row=1, column=2, padx=5, pady=5)

# Create output file selection
output_label = tk.Label(frame, text="Output File Name:")
output_label.grid(row=2, column=0, padx=10, pady=5)
output_file_entry = tk.Entry(frame, width=40)
output_file_entry.grid(row=2, column=1, padx=10, pady=5)
output_file_entry.insert(tk.END, "example.xlsx")
# output_browse_button = tk.Button(frame, text="Browse", command=browse_output_file)
# output_browse_button.grid(row=2, column=2, padx=5, pady=5)

# Create button to process files
process_button = tk.Button(frame, text="Process Files", command=process_files)

process_button.grid(row=3, column=1, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
