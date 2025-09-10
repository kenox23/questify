import tkinter as tk
from tkinter import simpledialog, messagebox

class DragSortListbox(tk.Listbox):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("selectmode", tk.SINGLE)
        super().__init__(master, **kwargs)

        self.bind("<Button-1>", self.on_button1)
        self.bind("<B1-Motion>", self.on_motion)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Double-Button-1>", self.on_double_click)

        self._drag_start_index = None
        self._drag_current_index = None

    def on_button1(self, event):
        # Record the index where drag started
        idx = self.nearest(event.y)
        if idx >= 0:
            self._drag_start_index = idx
            self.selection_clear(0, tk.END)
            self.selection_set(idx)
            self._drag_current_index = idx

    def on_motion(self, event):
        if self._drag_start_index is None:
            return
        # Determine index under pointer
        idx = self.nearest(event.y)
        if idx < 0:
            return

        # If pointer moved to a different index, visually move item
        if idx != self._drag_current_index:
            self._swap_items(self._drag_current_index, idx)
            self._drag_current_index = idx
            # keep selection on dragged item
            self.selection_clear(0, tk.END)
            self.selection_set(idx)
            # Ensure dragged-to index is visible
            self.see(idx)

    def on_release(self, event):
        # End drag
        self._drag_start_index = None
        self._drag_current_index = None

    def _swap_items(self, i, j):
        # Swap items at positions i and j
        if i == j:
            return
        text_i = self.get(i)
        text_j = self.get(j)
        self.delete(i)
        # After deleting i, indices shift; compute correct insertion
        if i < j:
            # removed earlier item so j becomes j-1
            self.delete(j - 1)
            self.insert(i, text_j)
            self.insert(j, text_i)
        else:
            # i > j
            self.delete(j)
            self.insert(j, text_i)
            self.insert(i, text_j)

    def on_double_click(self, event):
        # Edit item text on double-click
        idx = self.nearest(event.y)
        if idx < 0:
            return
        current = self.get(idx)
        new = simpledialog.askstring("Edit item", "Edit item:", initialvalue=current, parent=self)
        if new is not None:
            self.delete(idx)
            self.insert(idx, new)
            self.selection_clear(0, tk.END)
            self.selection_set(idx)

    # helper to get all items as a list
    def items(self):
        return list(self.get(0, tk.END))

    # helper to replace contents with a list
    def replace_items(self, items):
        self.delete(0, tk.END)
        for it in items:
            self.insert(tk.END, it)

def main():
    root = tk.Tk()
    root.title("Drag & Sort List - Test")

    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill="both", expand=True)

    lbl = tk.Label(frame, text="Tasks (drag to reorder, double-click to edit):")
    lbl.pack(anchor="w")

    listbox = DragSortListbox(frame, height=10, width=40)
    listbox.pack(fill="both", expand=True, pady=(6, 6))

    # sample items
    sample_tasks = [
        "Buy groceries",
        "Write report",
        "Call Alice",
        "Fix bug #123",
        "Plan weekend trip",
    ]
    listbox.replace_items(sample_tasks)

    btn_frame = tk.Frame(frame)
    btn_frame.pack(fill="x", pady=(0,6))
    
    def add_item():
        txt = simpledialog.askstring("Add item", "New item:", parent=root)
        if txt:
            listbox.insert(tk.END, txt)

    def delete_item():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Delete item", "Select an item first.")
            return
        listbox.delete(sel[0])

    def sort_items():
        items = listbox.items()
        items.sort(key=str.lower)  # case-insensitive
        listbox.replace_items(items)

    add_btn = tk.Button(btn_frame, text="Add", command=add_item)
    del_btn = tk.Button(btn_frame, text="Delete", command=delete_item)
    sort_btn = tk.Button(btn_frame, text="Sort A→Z", command=sort_items)

    add_btn.pack(side="left", padx=4)
    del_btn.pack(side="left", padx=4)
    sort_btn.pack(side="left", padx=4)

    root.mainloop()

if __name__ == "__main__":
    main()
