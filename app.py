import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer")
        self.root.geometry("1000x600")
        
        # Add padding around the window
        self.root.config(padx=10, pady=10)

        # Frame for the buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10, fill=tk.X)

        # Button to load CSV
        self.load_button = tk.Button(self.button_frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Button to load multiple CSVs
        self.load_multiple_button = tk.Button(self.button_frame, text="Load Multiple CSVs", command=self.load_multiple_csv)
        self.load_multiple_button.pack(side=tk.LEFT, padx=5)

        # Label to display current file path
        self.file_label = tk.Label(root, text="No file loaded", anchor=tk.W)
        self.file_label.pack(fill=tk.X, padx=5, pady=5)

        # Create a Treeview widget to display CSV data
        self.tree = ttk.Treeview(root)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Create vertical and horizontal scrollbars linked to the Treeview
        self.v_scroll = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.v_scroll.set)

        self.h_scroll = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=self.h_scroll.set)

    def load_csv(self):
        # Open file dialog and get the file path
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")],
            title="Select a CSV file"
        )
        if file_path:
            self._load_file(file_path)

    def load_multiple_csv(self):
        # Open file dialog and get multiple file paths
        file_paths = filedialog.askopenfilenames(
            filetypes=[("CSV Files", "*.csv")],
            title="Select CSV files"
        )
        if file_paths:
            for file_path in file_paths:
                self._load_file(file_path)

    def _load_file(self, file_path):
        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Update the file label with the current file path
            self.file_label.config(text=f"Loaded file: {file_path}")

            # Clear existing columns
            self.tree["columns"] = []
            self.tree["show"] = "headings"

            # Add columns to Treeview
            self.tree["columns"] = list(df.columns)
            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.W)

            # Add rows to Treeview
            for index, row in df.iterrows():
                self.tree.insert("", tk.END, values=list(row))
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()
