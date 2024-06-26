import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pickle

class CleanupTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Cleanup Tool")

        self.load_last_path()

        self.path_var = tk.StringVar(value=self.last_path if hasattr(self, 'last_path') else "")

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        path_label = tk.Label(frame, text="Path:")
        path_label.grid(row=0, column=0, padx=5, pady=5)

        path_entry = tk.Entry(frame, textvariable=self.path_var, width=50, bg="white", fg="black")
        path_entry.grid(row=0, column=1, padx=5, pady=5)

        browse_button = tk.Button(frame, text="Browse", command=self.browse_folder)
        browse_button.grid(row=0, column=2, padx=5, pady=5)

        delete_button = tk.Button(self.root, text="Delete", command=self.delete_folders)
        delete_button.pack(pady=10, padx=5, anchor='e')

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_var.set(folder_path)

    def delete_folders(self):
        base_path = self.path_var.get()
        if not os.path.isdir(base_path):
            messagebox.showerror("Error", "Invalid directory path")
            return

        self.save_last_path(base_path)

        deleted_folders = []
        for root, dirs, files in os.walk(base_path):
            for dir_name in dirs:
                if dir_name in ('bin', 'obj'):
                    full_path = os.path.join(root, dir_name)
                    try:
                        os.rmdir(full_path)
                        deleted_folders.append(full_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete {full_path}: {e}")

        if deleted_folders:
            messagebox.showinfo("Success", f"Deleted folders: {deleted_folders}")
        else:
            messagebox.showinfo("Info", "No 'bin' or 'obj' folders found")

    def load_last_path(self):
        try:
            with open('last_path.pkl', 'rb') as file:
                self.last_path = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.last_path = ""

    def save_last_path(self, path):
        with open('last_path.pkl', 'wb') as file:
            pickle.dump(path, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = CleanupTool(root)
    root.mainloop()
