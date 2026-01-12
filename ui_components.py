# ui_components.py
import tkinter as tk

def build_param_grid(parent, fields, max_fields_per_row=2, label_w=14, entry_w=14, pady=6):
    """
    fields: lista de dicts:
      {"key": "a", "label": "a:", "default": "0"}
    """
    entries = {}

    # cada campo ocupa 2 columnas: label + entry
    cols_per_field = 2
    max_cols = max_fields_per_row * cols_per_field

    for idx, f in enumerate(fields):
        row = (idx * cols_per_field) // max_cols
        col = (idx * cols_per_field) % max_cols

        tk.Label(parent, text=f["label"], width=label_w, anchor="w", bg=parent["bg"]).grid(
            row=row, column=col, padx=(0, 6), pady=pady, sticky="w"
        )

        e = tk.Entry(parent, width=entry_w, relief=tk.SOLID, bd=1)
        e.grid(row=row, column=col + 1, padx=(0, 18), pady=pady, sticky="w")

        if "default" in f:
            e.insert(0, str(f["default"]))

        entries[f["key"]] = e

    for c in range(max_cols):
        parent.grid_columnconfigure(c, weight=0)

    return entries
