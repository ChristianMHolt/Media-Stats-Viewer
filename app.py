import os
import threading
import customtkinter
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from media_library import LibraryScanner, MediaItem

STATUS_RANK = {
    "blue": 1,        # Airing
    "green": 2,       # Great
    "light_green": 3, # Good
    "orange": 4,      # Okay
    "red": 5,         # Bad
    "": 6             # None
}

def sort_helper(items, primary_sort, secondary_sort, value_getter):
    """
    Sorts a list of items based on primary and secondary sort specifications.

    Args:
        items: List of item identifiers.
        primary_sort: Tuple (col_name, reverse_bool) or None.
        secondary_sort: Tuple (col_name, reverse_bool) or None.
        value_getter: Function that takes (item_id, col_name) and returns sortable value.

    Returns:
        Sorted list of items.
    """
    l = list(items)

    # Python's sort is stable. Sort by secondary first, then primary.

    if secondary_sort:
        col, rev = secondary_sort
        l.sort(key=lambda k: value_getter(k, col), reverse=rev)

    if primary_sort:
        col, rev = primary_sort
        l.sort(key=lambda k: value_getter(k, col), reverse=rev)

    return l

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

        # Sort by Status Dropdown
        self.status_sort_var = customtkinter.StringVar(value="Status: Default")
        self.status_combo = customtkinter.CTkComboBox(self.top_frame,
                                                      values=["Status: Default", "Status: Best -> Worst", "Status: Worst -> Best"],
                                                      command=self.on_status_sort_change,
                                                      variable=self.status_sort_var)
        self.status_combo.pack(side="left", padx=10)

        self.status_label = customtkinter.CTkLabel(self.top_frame, text="Ready to scan.")
        self.status_label.pack(side="left", padx=10)

        # Sorting State
        self.primary_sort_col = None
        self.secondary_sort_col = None

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
                        borderwidth=1,
                        relief="solid",
                        rowheight=50,
                        font=("Arial", 20))

        style.map('Treeview', background=[('selected', selected_bg)])

        style.configure("Treeview.Heading",
                        background="#343638",
                        foreground="white",
                        relief="flat",
                        font=("Arial", 11, "bold"))

        style.map("Treeview.Heading",
                  background=[('active', '#404040')])

        self.columns = ("Name", "Season", "Group", "Resolution", "Source", "Video", "Audio", "Avg Size (GB)")
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings",
                                 yscrollcommand=self.scrollbar.set, selectmode="browse")

        # Configure columns
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.on_header_click(c))
            self.tree.column(col, width=120, anchor="w")

        # Bind Right Click for secondary sort
        self.tree.bind("<Button-3>", self.on_header_right_click)

        self.tree.column("Name", width=300)
        self.tree.column("Season", width=100)
        self.tree.pack(side="left", fill="both", expand=True)

        self.scrollbar.configure(command=self.tree.yview)

        # Configure tags for colors
        self.tree.tag_configure("green", background="#2e8b57", foreground="white")
        self.tree.tag_configure("light_green", background="#90ee90", foreground="black")
        self.tree.tag_configure("blue", background="#4682b4", foreground="white")
        self.tree.tag_configure("orange", background="#ffa500", foreground="black")
        self.tree.tag_configure("red", background="#cd5c5c", foreground="white")

    def on_status_sort_change(self, choice):
        if choice == "Status: Best -> Worst":
            self.primary_sort_col = ("Status", False) # False = Ascending rank (1 to 6)
        elif choice == "Status: Worst -> Best":
            self.primary_sort_col = ("Status", True)  # True = Descending rank (6 to 1)
        else:
            # Default: If primary was Status, clear it
            if self.primary_sort_col and self.primary_sort_col[0] == "Status":
                self.primary_sort_col = None

        self.perform_sort()

    def on_header_click(self, col):
        # Determine new reverse state
        reverse = False
        if self.primary_sort_col and self.primary_sort_col[0] == col:
            reverse = not self.primary_sort_col[1]

        self.primary_sort_col = (col, reverse)
        self.perform_sort()

    def on_header_right_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            col_id = self.tree.identify_column(event.x)
            # col_id is like '#1', need to map to column name.
            # tree.column(col_id, option='id') returns the identifier (e.g. "Name")
            col_name = self.tree.column(col_id, "id")

            # Determine reverse
            reverse = False
            if self.secondary_sort_col and self.secondary_sort_col[0] == col_name:
                reverse = not self.secondary_sort_col[1]

            self.secondary_sort_col = (col_name, reverse)
            self.perform_sort()

    def perform_sort(self):
        item_ids = self.tree.get_children('')

        def value_getter(item_id, col_name):
            if col_name == "Status":
                tags = self.tree.item(item_id, "tags")
                tag = tags[0] if tags else ""
                return STATUS_RANK.get(tag, 6)
            elif col_name == "Avg Size (GB)":
                val = self.tree.set(item_id, col_name)
                try:
                    return float(val.replace(" GB", ""))
                except ValueError:
                    return 0.0
            else:
                return self.tree.set(item_id, col_name).lower()

        sorted_ids = sort_helper(item_ids, self.primary_sort_col, self.secondary_sort_col, value_getter)

        for index, item_id in enumerate(sorted_ids):
            self.tree.move(item_id, '', index)

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
            avg_size_str = f"{item.avg_size_gb:6.2f} GB"
            values = (item.name, season_str, item.group, item.resolution, item.source, item.video_codec, item.audio_codec, avg_size_str)
            tag = get_item_tag(item)
            if tag:
                self.tree.insert("", "end", values=values, tags=(tag,))
            else:
                self.tree.insert("", "end", values=values)

        self.status_label.configure(text=f"Scan complete. Found {len(items)} items.")

def get_item_tag(item: MediaItem) -> str:
    if item.is_airing:
        return "blue"

    source_norm = item.source.lower().replace("-", " ")
    video_norm = item.video_codec.lower().replace("-", " ")

    if "web dl" in source_norm:
            return "red"

    if "bd encode" in source_norm:
        if "svt av1" in video_norm:
            return "light_green"
        else:
            return "orange"

    if "bd remux" in source_norm or "dvd" in source_norm:
            if "h.264" in video_norm or "x264" in video_norm or "mpeg2" in video_norm or "mpeg 2" in video_norm:
                return "green"

    return ""

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    app = App()
    app.mainloop()
