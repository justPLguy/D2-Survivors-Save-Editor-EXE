import base64
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zlib
import webbrowser

PREFIX = "D2S1:"

DISPLAY_NAMES = {
    "life": "Life",
    "mana": "Mana",
    "energy": "Energy",
    "strength": "Strength",
    "dexterity": "Dexterity",
    "vitality": "Vitality",
    "enhancedDefense": "Enhanced Defense (%)",
    "enhancedDamage": "Enhanced Damage (%)",
    "fireResist": "Fire Resist (%)",
    "coldResist": "Cold Resist (%)",
    "lightningResist": "Lightning Resist (%)",
    "poisonResist": "Poison Resist (%)",
    "attackRating": "Attack Rating",
    "magicFind": "Magic Find (%)",
    "fasterCastRate": "Faster Cast Rate (%)",
    "fasterRunWalk": "Faster Run/Walk (%)",
    "damageReduced": "Damage Reduced (%)",
}


def decode_save(save_code):
    save_code = save_code.strip()
    if not save_code.startswith(PREFIX):
        raise ValueError("The save code must start with D2S1:")
    encoded = save_code[len(PREFIX):]
    encoded += "=" * (-len(encoded) % 4)
    raw = zlib.decompress(base64.urlsafe_b64decode(encoded))
    return json.loads(raw.decode("utf-8"))


def encode_save(data):
    raw = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    encoded = base64.urlsafe_b64encode(zlib.compress(raw, level=9)).decode("ascii").rstrip("=")
    return PREFIX + encoded


def walk_items(node, path=()):
    found = []
    if isinstance(node, dict):
        if isinstance(node.get("mods"), list) and (
            "base" in node or "name" in node or "type" in node
        ):
            found.append((path, node))
        for key, value in node.items():
            found.extend(walk_items(value, path + (key,)))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(walk_items(value, path + (index,)))
    return found


def class_entries(data):
    root = data.get("equippedByClass")
    return root if isinstance(root, dict) else {}


def equipped_items_for_class(data, class_key):
    # Regular character equipment
    if not str(class_key).startswith("__merc__|"):
        root = class_entries(data).get(class_key)
        if root is None:
            return []
        return walk_items(root, ("equippedByClass", class_key))

    # Mercenary equipment is stored separately under mercs -> owner class -> hired -> merc type -> worn.
    _, owner_class, merc_type = str(class_key).split("|", 2)
    merc_root = (
        data.get("mercs", {})
            .get(owner_class, {})
            .get("hired", {})
            .get(merc_type, {})
            .get("worn", {})
    )
    return walk_items(merc_root, ("mercs", owner_class, "hired", merc_type, "worn"))


def class_display_name(data, class_key):
    if str(class_key).startswith("__merc__|"):
        _, owner_class, merc_type = str(class_key).split("|", 2)
        merc = data.get("mercs", {}).get(owner_class, {}).get("hired", {}).get(merc_type, {})
        merc_name = merc.get("name", merc_type)
        return f"{pretty_class(owner_class)} — Mercenary ({merc_type.title()}, {merc_name})"
    return pretty_class(class_key)


def pretty_stat(stat):
    return DISPLAY_NAMES.get(str(stat), str(stat))


def get_item_name(item):
    return str(item.get("name") or item.get("base") or item.get("type") or "Unknown item")


def pretty_class(class_key):
    return str(class_key).replace("_", " ").replace("-", " ").title()


class SaveEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("D2 Survivors Save Editor v6.3 — Mercenary Equipment")
        self.geometry("1080x820")
        self.minsize(900, 760)
        self.data = None
        self.class_keys = []
        self.current_class_key = None
        self.items = []
        self.selected_item_index = None
        self.modifier_vars = []
        self.output_code = None
        self._build_ui()

    def _build_ui(self):
        root = ttk.Frame(self, padding=14)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="D2 Survivors Save Editor", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            root,
            text="Edit gold, character equipment, and mercenary equipment modifiers.",
            foreground="#555"
        ).pack(anchor="w", pady=(2, 12))

        save_frame = ttk.LabelFrame(root, text="1. Save code", padding=10)
        save_frame.pack(fill="x", pady=(0, 10))
        self.save_text = tk.Text(save_frame, height=4, wrap="word", undo=True)
        self.save_text.pack(side="left", fill="both", expand=True)
        save_scroll = ttk.Scrollbar(save_frame, orient="vertical", command=self.save_text.yview)
        save_scroll.pack(side="right", fill="y")
        self.save_text.configure(yscrollcommand=save_scroll.set)

        button_row = ttk.Frame(root)
        button_row.pack(fill="x", pady=(0, 10))
        ttk.Button(button_row, text="Load Save Code", command=self.load_save).pack(side="left")
        ttk.Button(button_row, text="Paste from Clipboard", command=self.paste_clipboard).pack(side="left", padx=6)
        ttk.Button(button_row, text="Clear", command=self.clear_all).pack(side="left")
        self.gold_var = tk.StringVar()
        ttk.Label(button_row, text="Gold:").pack(side="left", padx=(20, 5))
        ttk.Entry(button_row, textvariable=self.gold_var, width=14).pack(side="left")
        ttk.Label(
            button_row,
            text="(shared across all character classes)",
            foreground="#555"
        ).pack(side="left", padx=(6, 0))

        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 12))

        selectors_frame = ttk.Frame(left_frame)
        selectors_frame.pack(fill="x", pady=(0, 10))

        class_frame = ttk.LabelFrame(selectors_frame, text="2. Character", padding=6)
        class_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.class_list = tk.Listbox(class_frame, width=19, height=6, exportselection=False)
        self.class_list.pack(fill="both", expand=True)
        self.class_list.bind("<<ListboxSelect>>", self.on_class_select)

        merc_frame = ttk.LabelFrame(selectors_frame, text="3. Assigned mercenary", padding=6)
        merc_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.merc_list = tk.Listbox(merc_frame, width=23, height=6, exportselection=False)
        self.merc_list.pack(fill="both", expand=True)
        self.merc_list.bind("<<ListboxSelect>>", self.on_merc_select)

        item_frame = ttk.LabelFrame(left_frame, text="4. Equipped items", padding=8)
        item_frame.pack(fill="both", expand=True)
        self.item_list = tk.Listbox(item_frame, width=35, height=16, exportselection=False)
        self.item_list.pack(side="left", fill="both", expand=True)
        self.item_list.bind("<<ListboxSelect>>", self.on_item_select)
        item_scroll = ttk.Scrollbar(item_frame, orient="vertical", command=self.item_list.yview)
        item_scroll.pack(side="right", fill="y")
        self.item_list.configure(yscrollcommand=item_scroll.set)

        mod_frame = ttk.LabelFrame(main_frame, text="5. Selected item modifiers", padding=10)
        mod_frame.pack(side="left", fill="both", expand=True)
        self.mod_canvas = tk.Canvas(mod_frame, highlightthickness=0)
        self.mod_scroll = ttk.Scrollbar(mod_frame, orient="vertical", command=self.mod_canvas.yview)
        self.mod_inner = ttk.Frame(self.mod_canvas)
        self.mod_inner.bind("<Configure>", lambda e: self.mod_canvas.configure(scrollregion=self.mod_canvas.bbox("all")))
        self.mod_canvas_window = self.mod_canvas.create_window((0, 0), window=self.mod_inner, anchor="nw")
        self.mod_canvas.bind("<Configure>", lambda e: self.mod_canvas.itemconfigure(self.mod_canvas_window, width=e.width))
        self.mod_canvas.configure(yscrollcommand=self.mod_scroll.set)
        self.mod_canvas.pack(side="left", fill="both", expand=True)
        self.mod_scroll.pack(side="right", fill="y")

        bottom = ttk.Frame(root)
        bottom.pack(fill="x", pady=(12, 0))
        ttk.Button(bottom, text="Generate Modified Save", command=self.generate_save).pack(side="left")
        ttk.Button(bottom, text="Save Output to File...", command=self.save_output).pack(side="left", padx=8)
        self.status_var = tk.StringVar(value="Paste a save code, then click Load Save Code.")
        ttk.Label(bottom, textvariable=self.status_var).pack(side="left", padx=10)

        footer = ttk.Frame(root)
        footer.pack(fill="x", pady=(8, 0))

        footer_left = ttk.Frame(footer)
        footer_left.pack(side="left", anchor="w")

        ttk.Label(
            footer_left,
            text="Created by Just a Polish Guy",
            foreground="#555"
        ).pack(side="left")

        ttk.Label(footer_left, text=" | ", foreground="#888").pack(side="left")
        self._add_link(footer_left, "GitHub", "https://github.com/justPLguy/D2-Survivors-Save-Editor")
        ttk.Label(footer_left, text=" | ", foreground="#888").pack(side="left")
        self._add_link(footer_left, "YouTube", "https://www.youtube.com/@justPLguy")

        ttk.Label(
            footer,
            text="More tools, updates and tutorials",
            foreground="#555"
        ).pack(side="right", anchor="e")

    def _add_link(self, parent, label, url):
        link = tk.Label(parent, text=label, fg="#0969DA", cursor="hand2", font=("Segoe UI", 9, "underline"))
        link.pack(side="left")
        link.bind("<Button-1>", lambda event: webbrowser.open(url))

    def paste_clipboard(self):
        try:
            content = self.clipboard_get()
            self.save_text.delete("1.0", "end")
            self.save_text.insert("1.0", content.strip())
            self.status_var.set("Clipboard pasted. Click Load Save Code.")
        except tk.TclError:
            messagebox.showerror("Clipboard error", "No text could be read from the clipboard.")

    def clear_all(self):
        self.save_text.delete("1.0", "end")
        self.class_list.delete(0, "end")
        self.merc_list.delete(0, "end")
        self.item_list.delete(0, "end")
        for child in self.mod_inner.winfo_children():
            child.destroy()
        self.data = None
        self.class_keys = []
        self.current_class_key = None
        self.items = []
        self.selected_item_index = None
        self.modifier_vars = []
        self.gold_var.set("")
        self.output_code = None
        self.status_var.set("Cleared. Paste a save code to begin.")

    def load_save(self):
        code = self.save_text.get("1.0", "end").strip()
        try:
            self.data = decode_save(code)
        except Exception as exc:
            messagebox.showerror("Could not load save", f"Check that the complete D2S1 code was pasted.\n\nDetails: {exc}")
            return

        root = class_entries(self.data)
        self.class_keys = list(root.keys())

        # Character classes stay in their own list. Mercenaries are selected
        # in a separate adjacent list, filtered to the selected owner class.
        self.class_list.delete(0, "end")
        for key in self.class_keys:
            self.class_list.insert("end", pretty_class(key))
        self.gold_var.set(str(self.data.get("gold", "")))
        self.merc_list.delete(0, "end")
        self.items = []
        self.selected_item_index = None
        self.modifier_vars = []
        self.item_list.delete(0, "end")
        for child in self.mod_inner.winfo_children():
            child.destroy()
        self.status_var.set(f"Loaded successfully: {len(self.class_keys)} character/equipment section(s) found.")
        if self.class_keys:
            self.class_list.selection_set(0)
            self.class_list.activate(0)
            self.current_class_key = self.class_keys[0]
            self.refresh_merc_list()
            self.refresh_items()

    def on_class_select(self, event=None):
        selection = self.class_list.curselection()
        if not selection or self.data is None:
            return
        # Save the previous item's pending edits before switching class.
        if self.selected_item_index is not None and not self.save_current_item_changes(show_message=False):
            self.class_list.selection_clear(0, "end")
            if self.current_class_key in self.class_keys:
                self.class_list.selection_set(self.class_keys.index(self.current_class_key))
            return
        self.current_class_key = self.class_keys[selection[0]]
        self.refresh_merc_list()
        self.refresh_items()

    def refresh_merc_list(self):
        self.merc_list.delete(0, "end")
        if self.data is None or not self.current_class_key:
            return
        owner_data = self.data.get("mercs", {}).get(self.current_class_key, {})
        hired = owner_data.get("hired", {}) if isinstance(owner_data, dict) else {}
        if not isinstance(hired, dict) or not hired:
            self.merc_list.insert("end", "(No mercenary)")
            return
        for merc_type, merc_data in hired.items():
            merc_name = merc_data.get("name", merc_type) if isinstance(merc_data, dict) else merc_type
            self.merc_list.insert("end", f"{merc_type.title()} — {merc_name}")
        self.merc_list.selection_set(0)
        self.merc_list.activate(0)

    def on_merc_select(self, event=None):
        selection = self.merc_list.curselection()
        if not selection or self.data is None or not self.current_class_key:
            return
        merc_type = list(self.data.get("mercs", {}).get(self.current_class_key, {}).get("hired", {}).keys())
        if not merc_type:
            return
        index = selection[0]
        if index >= len(merc_type):
            return
        merc_key = f"__merc__|{self.current_class_key}|{merc_type[index]}"
        if self.selected_item_index is not None and not self.save_current_item_changes(show_message=False):
            self.merc_list.selection_clear(0, "end")
            self.merc_list.selection_set(index)
            return
        self.current_class_key = merc_key
        self.refresh_items()

    def refresh_items(self):
        self.items = equipped_items_for_class(self.data, self.current_class_key)
        self.item_list.delete(0, "end")
        for _, item in self.items:
            self.item_list.insert("end", f"{get_item_name(item)}  ({len(item.get('mods', []))} mods)")
        for child in self.mod_inner.winfo_children():
            child.destroy()
        self.modifier_vars = []
        self.selected_item_index = None
        if self.items:
            self.item_list.selection_set(0)
            self.item_list.activate(0)
            self.on_item_select()
        self.status_var.set(
            f"{class_display_name(self.data, self.current_class_key)}: {len(self.items)} item(s) found."
        )

    def on_item_select(self, event=None):
        selection = self.item_list.curselection()
        if not selection or self.data is None:
            return
        new_index = selection[0]
        # Commit pending edits for the previously selected item before switching.
        if self.selected_item_index is not None and new_index != self.selected_item_index:
            if not self.save_current_item_changes(show_message=False):
                self.item_list.selection_clear(0, "end")
                self.item_list.selection_set(self.selected_item_index)
                return
        self.selected_item_index = new_index
        item = self.items[new_index][1]

        for child in self.mod_inner.winfo_children():
            child.destroy()
        self.modifier_vars = []

        ttk.Label(self.mod_inner, text=get_item_name(item), font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 10)
        )
        ttk.Label(self.mod_inner, text="Stat").grid(row=1, column=0, sticky="w", padx=(0, 10))
        ttk.Label(self.mod_inner, text="Current value").grid(row=1, column=1, sticky="w", padx=(0, 10))
        ttk.Label(self.mod_inner, text="New value").grid(row=1, column=2, sticky="w")

        mods = item.get("mods", [])
        for row, mod in enumerate(mods, start=2):
            stat = mod.get("stat", "unknown")
            value = mod.get("value", "")
            ttk.Label(self.mod_inner, text=f"{pretty_stat(stat)} ({stat})").grid(
                row=row, column=0, sticky="w", padx=(0, 10), pady=3
            )
            ttk.Label(self.mod_inner, text=str(value)).grid(row=row, column=1, sticky="w", padx=(0, 10), pady=3)
            var = tk.StringVar(value=str(value))
            entry = ttk.Entry(self.mod_inner, textvariable=var, width=14)
            entry.grid(row=row, column=2, sticky="w", pady=3)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                entry.configure(state="disabled")
            self.modifier_vars.append((mod, var, value))

        action_row = ttk.Frame(self.mod_inner)
        action_row.grid(row=len(mods) + 2, column=0, columnspan=3, sticky="w", pady=(12, 0))
        ttk.Button(action_row, text="Save Item Changes", command=self.save_current_item_changes).pack(side="left")
        ttk.Label(action_row, text="Changes are kept when switching items/classes.",
                  foreground="#555").pack(side="left", padx=(10, 0))

    def save_current_item_changes(self, show_message=True):
        if self.data is None or self.selected_item_index is None or not self.items:
            return True
        try:
            item = self.items[self.selected_item_index][1]
            for mod, var, original_value in self.modifier_vars:
                if not isinstance(original_value, (int, float)) or isinstance(original_value, bool):
                    continue
                text_value = var.get().strip()
                if not text_value:
                    raise ValueError(f"Value for {mod.get('stat')} cannot be blank.")
                mod["value"] = int(text_value)
            self.modifier_vars = [(mod, var, mod.get("value")) for mod, var, _ in self.modifier_vars]
            self.status_var.set(f"Changes saved for {get_item_name(item)}.")
            if show_message:
                messagebox.showinfo("Item saved", "Changes to this item have been saved in the editor.")
            return True
        except Exception as exc:
            messagebox.showerror("Invalid value", str(exc))
            return False

    def generate_save(self):
        if self.data is None:
            messagebox.showwarning("No save loaded", "Paste a save code and click Load Save Code first.")
            return
        if self.selected_item_index is not None:
            if not self.save_current_item_changes(show_message=False):
                return
        try:
            gold_text = self.gold_var.get().strip()
            if gold_text:
                gold = int(gold_text)
                if gold < 0:
                    raise ValueError("Gold cannot be negative.")
                self.data["gold"] = gold
            self.output_code = encode_save(self.data)
            self.status_var.set("Modified save generated.")
            self.show_output(self.output_code)
        except Exception as exc:
            messagebox.showerror("Invalid value", str(exc))

    def show_output(self, output_code):
        win = tk.Toplevel(self)
        win.title("Generated Save Code")
        win.geometry("850x350")
        ttk.Label(win, text="Copy this complete code into the game's SAVES menu:").pack(anchor="w", padx=10, pady=(10, 4))
        text = tk.Text(win, wrap="word", height=10)
        text.pack(fill="both", expand=True, padx=10, pady=4)
        text.insert("1.0", output_code)
        row = ttk.Frame(win)
        row.pack(fill="x", padx=10, pady=10)

        def copy_code():
            self.clipboard_clear()
            self.clipboard_append(output_code)
            self.update()
            messagebox.showinfo("Copied", "Save code copied to clipboard.", parent=win)

        ttk.Button(row, text="Copy Code", command=copy_code).pack(side="left")
        ttk.Button(row, text="Save to File...", command=lambda: self.save_output(output_code)).pack(side="left", padx=8)
        ttk.Button(row, text="Close", command=win.destroy).pack(side="right")

    def save_output(self, code=None):
        if code is None:
            code = self.output_code
        if not code:
            messagebox.showwarning("No output yet", "Click Generate Modified Save first.")
            return
        path = filedialog.asksaveasfilename(
            title="Save modified save code",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(code + "\n")
            self.status_var.set(f"Output saved to {path}")
            messagebox.showinfo("Saved", f"Modified save saved to:\n{path}")
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc))


if __name__ == "__main__":
    app = SaveEditor()
    app.mainloop()
