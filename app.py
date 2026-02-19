import os
import threading
import customtkinter
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from media_library import LibraryScanner, MediaItem

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Media Library Tracker")
        self.geometry("1100x600")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Top Frame ---
        self.top_frame = customtkinter.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.btn_select = customtkinter.CTkButton(self.top_frame, text="Select Library Folder", command=self.select_folder)
        self.btn_select.pack(side="left", padx=10, pady=10)

        self.status_label = customtkinter.CTkLabel(self.top_frame, text="Ready to scan.")
        self.status_label.pack(side="left", padx=10)

        # --- Treeview Frame ---
        self.tree_frame = customtkinter.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Treeview Scrollbar
        self.scrollbar = customtkinter.CTkScrollbar(self.tree_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Treeview
        # We need a style for Treeview to look dark
        style = ttk.Style()
        style.theme_use("clam")

        # Colors matching customtkinter dark theme roughly
        bg_color = "#2b2b2b"
        fg_color = "white"
        selected_bg = "#1f6aa5"

        style.configure("Treeview",
                        background=bg_color,
                        foreground=fg_color,
                        fieldbackground=bg_color,
                        bordercolor=bg_color,
                        borderwidth=0,
                        font=("Arial", 10))

        style.map('Treeview', background=[('selected', selected_bg)])

        style.configure("Treeview.Heading",
                        background="#343638",
                        foreground="white",
                        relief="flat",
                        font=("Arial", 11, "bold"))

        style.map("Treeview.Heading",
                  background=[('active', '#404040')])

        self.columns = ("Name", "Season", "Group", "Resolution", "Source", "Video", "Audio")
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings",
                                 yscrollcommand=self.scrollbar.set, selectmode="browse")

        # Configure columns
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w")

        self.tree.column("Name", width=300)
        self.tree.column("Season", width=100)
        self.tree.pack(side="left", fill="both", expand=True)

        self.scrollbar.configure(command=self.tree.yview)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.status_label.configure(text=f"Scanning: {folder_selected}...")
            # Run scan in background thread
            thread = threading.Thread(target=self.run_scan, args=(folder_selected,))
            thread.start()

    def run_scan(self, path):
        try:
            scanner = LibraryScanner(path)
            items = scanner.scan()
            # Update UI on main thread
            self.after(0, lambda: self.update_table(items))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {e}"))

    def update_table(self, items):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new items
        for item in items:
            season_str = item.season if item.season else ""
            values = (item.name, season_str, item.group, item.resolution, item.source, item.video_codec, item.audio_codec)
            self.tree.insert("", "end", values=values)

        self.status_label.configure(text=f"Scan complete. Found {len(items)} items.")

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    app = App()
    app.mainloop()
