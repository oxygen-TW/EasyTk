import logging
import csv
import tkinter as tk
from tkinter import ttk
from typing import Any, Literal, Optional

import pandas as pd
from natsort import natsort_keygen, ns

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# Visual constants
COLOR_PLACEHOLDER = "gray"
COLOR_TEXT = "black"
COLOR_FOCUS_BORDER = "#007acc"
COLOR_IDLE_BORDER = "#cccccc"


class HyperlinkLabel(tk.Label):
    """Label that behaves like a hyperlink."""

    def __init__(self, parent: tk.Widget, text: str, url: str, underscore: bool = True, **kwargs: Any) -> None:
        if underscore:
            font = kwargs.get("font", ("Arial", 10))
            kwargs["font"] = (font[0], font[1], "underline")

        super().__init__(parent, text=text, **kwargs)
        self.url = url
        self.bind("<Button-1>", self._open_hyperlink)

    def _open_hyperlink(self, event: tk.Event) -> None:
        import webbrowser
        webbrowser.open_new(self.url)


class BetterEntry(tk.Entry):
    """Entry widget with placeholder text and focus styling."""

    def __init__(self, parent: tk.Widget, **kwargs: Any) -> None:
        # Custom kwarg
        raw_placeholder = kwargs.pop("placeholder", "")
        self.placeholder_text = "" if raw_placeholder is None else str(raw_placeholder)

        super().__init__(parent, **kwargs)

        self._initialize_placeholder()
        self._bind_events()

    # ----------------------------
    # Initialization helpers
    # ----------------------------
    def _initialize_placeholder(self) -> None:
        """Set initial placeholder text and style if configured."""
        if not self.placeholder_text:
            return
        self.insert(0, self.placeholder_text)
        self.config(fg=COLOR_PLACEHOLDER, highlightbackground=COLOR_IDLE_BORDER)

    def _bind_events(self) -> None:
        """Bind widget events."""
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    # ----------------------------
    # Event handlers
    # ----------------------------
    def _on_focus_in(self, event: tk.Event) -> None:
        """Clear placeholder and apply active style on focus."""
        if self._is_showing_placeholder():
            self.delete(0, tk.END)
        self.config(fg=COLOR_TEXT, highlightbackground=COLOR_FOCUS_BORDER)

    def _on_focus_out(self, event: tk.Event) -> None:
        """Restore placeholder if empty, then apply idle style."""
        if not self.get().strip() and self.placeholder_text:
            self.delete(0, tk.END)
            self.insert(0, self.placeholder_text)
            self.config(fg=COLOR_PLACEHOLDER)
        self.config(highlightbackground=COLOR_IDLE_BORDER)

    # ----------------------------
    # Internal state helpers
    # ----------------------------
    def _is_showing_placeholder(self) -> bool:
        return (
            bool(self.placeholder_text)
            and self.get() == self.placeholder_text
            and self.cget("fg") == COLOR_PLACEHOLDER
        )

class ScrollableTextArea(tk.Text):
    def __init__(self, parent, orient: Literal["vertical", "horizontal", "both"] = "vertical", **kwargs):
        orient = orient.lower()
        if orient not in ["vertical", "horizontal", "both"]:
            raise ValueError("orient must be 'vertical', 'horizontal', or 'both'")

        if orient in ["horizontal", "both"] and kwargs.get("wrap", tk.CHAR) != tk.NONE:
            logging.warning("Horizontal scrolling requires wrap=tk.NONE. Auto-setting wrap=tk.NONE.")
            kwargs["wrap"] = tk.NONE
        
        super().__init__(parent, **kwargs)
        
        # Create scrollbars based on orient
        if orient in ["vertical", "both"]:
            self.y_scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
            self.configure(yscrollcommand=self.y_scrollbar.set)
            self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if orient in ["horizontal", "both"]:
            self.x_scrollbar = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)
            self.configure(xscrollcommand=self.x_scrollbar.set)
            self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_state(self, state):
        self.configure(state=state)

    def clear(self):
        self.configure(state=tk.NORMAL)
        self.delete("1.0", tk.END)

    def insert_text(self, text, state_after=None):
        current_state = self["state"]
        self.configure(state=tk.NORMAL)

        self.insert(tk.END, text)
        self.configure(state=state_after if state_after is not None else current_state)

    def get_text(self):
        return self.get("1.0", tk.END)
    
    def set_text(self, text, state_after=None, text_color: str | None = None):
        current_state = self["state"]
        self.configure(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        self.insert(tk.END, text)

        if text_color:
            tag_name = f"all_text_{text_color}".replace(" ", "_")
            self.tag_configure(tag_name, foreground=text_color)
            self.tag_add(tag_name, "1.0", tk.END)

        self.configure(state=state_after if state_after is not None else current_state)

class ScrollableTreeView(ttk.Treeview):
    
    def __init__(self, parent, orient: Literal["vertical", "horizontal", "both"] = "vertical", **kwargs):
        orient = orient.lower()

        super().__init__(parent, **kwargs)
        self.configure(show="headings")
        
        if orient not in ["vertical", "horizontal", "both"]:
            raise ValueError("orient must be 'vertical', 'horizontal', or 'both'")
        
        if orient in ["vertical", "both"]:
            self.v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
            self.configure(yscrollcommand=self.v_scrollbar.set)
            self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        if orient in ["horizontal", "both"]:
            self.h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)
            self.configure(xscrollcommand=self.h_scrollbar.set)
            self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_header(self, header: list):
        self["columns"] = header
        for col in header:
            self.heading(col, text=col)

    def load_csv(self, csv_file: str) -> None:
        with open(csv_file, "r") as f:
            table = csv.reader(f)
            #Extract first row as header
            header = next(table, None)
            if header:
                self.set_header(header)

            for row in table:
                if not row:
                    continue
                self.insert("", "end", values=row)

    def insert_row(self, values: list, font: Any = None, **tag_conf) -> None:
        if not self["columns"]:
            raise ValueError("Table columns not set. Call set_header() first.")
        if len(values) != len(self["columns"]):
            raise ValueError(f"Expected {len(self['columns'])} values, got {len(values)}")

        tags = ()
        if font:
            tag_name = f"font_{len(self.get_children())}"
            if isinstance(font, dict):
                font_value = (
                    font.get("family", "Arial"),
                    font.get("size", 10),
                    font.get("weight", "normal"),
                )
            else:
                font_value = font
            self.tag_configure(tag_name, font=font_value, **tag_conf)
            tags = (tag_name,)

        self.insert("", "end", values=values, tags=tags)
                
class EnhancedTableView(ttk.Treeview):
    """
    For now, read-only
    """

    def __init__(self, parent, data_file: Optional[str] = None, orient: Literal["vertical", "horizontal", "both"] = "vertical", **kwargs):
        orient = orient.lower()

        super().__init__(parent, **kwargs)

        self.natsort_key = natsort_keygen(alg=ns.IGNORECASE | ns.LOWERCASEFIRST | ns.GROUPLETTERS | ns.NANLAST)

        if orient not in ["vertical", "horizontal", "both"]:
            raise ValueError(
                "orient must be 'vertical', 'horizontal', or 'both'")

        if orient in ["vertical", "both"]:
            self.v_scrollbar = ttk.Scrollbar(
                parent, orient=tk.VERTICAL, command=self.yview)
            self.configure(yscrollcommand=self.v_scrollbar.set)
            self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        if orient in ["horizontal", "both"]:
            self.h_scrollbar = ttk.Scrollbar(
                parent, orient=tk.HORIZONTAL, command=self.xview)
            self.configure(xscrollcommand=self.h_scrollbar.set)
            self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.df = pd.DataFrame()
        self._row_id_col = "__etk_row_id__"
        self._row_tags_col = "__etk_row_tags__"
        self._next_row_id = 0
        self._sort_state: dict[str, bool] = {}

        if data_file:
            self.data_file = data_file
            self.df = pd.read_json(data_file)
            print(self.df)
            self.apply_dataframe()

    def _display_columns(self) -> list:
        return [
            col for col in self.df.columns
            if col not in (self._row_id_col, self._row_tags_col)
        ]

    def _ensure_internal_columns(self) -> None:
        if self._row_id_col not in self.df.columns:
            start_id = self._next_row_id
            self.df[self._row_id_col] = list(range(start_id, start_id + len(self.df)))
            self._next_row_id = start_id + len(self.df)
        else:
            max_id = pd.to_numeric(self.df[self._row_id_col], errors="coerce").max()
            if pd.isna(max_id):
                self._next_row_id = 0
            else:
                self._next_row_id = int(max_id) + 1

        if self._row_tags_col not in self.df.columns:
            self.df[self._row_tags_col] = [() for _ in range(len(self.df))]
        else:
            self.df[self._row_tags_col] = self.df[self._row_tags_col].apply(
                lambda t: tuple(t) if isinstance(t, (list, tuple)) else ()
            )

    def apply_dataframe(self) -> None:
        self._ensure_internal_columns()
        self._clear_dataframe()
        display_cols = self._display_columns()
        self["columns"] = display_cols
        for col in display_cols:
            self.heading(col, text=col, command=lambda c=col: self._sort_table(c))

        for _, row in self.df.iterrows():
            self.insert(
                "",
                "end",
                iid=str(row[self._row_id_col]),
                values=[row[col] for col in display_cols],
                tags=tuple(row[self._row_tags_col]),
            )

    def _clear_dataframe(self) -> None:
        for item in self.get_children():
            self.delete(item)

    def _sort_table(self, col: str) -> None:
        print("Sort triggered", col)

        if col not in self.df.columns or self.df.empty:
            return

        self._ensure_internal_columns()

        # Toggle sort direction per column. First click -> ascending.
        last_ascending = self._sort_state.get(col)
        new_ascending = True if last_ascending is None else not last_ascending

        # Sort DataFrame (stable sort keeps relative order of equal values)
        self.df.sort_values(by=col, ascending=new_ascending, inplace=True, key=self.natsort_key, kind="mergesort")
        self._sort_state[col] = new_ascending
        print("asc" if new_ascending else "desc")
        self.apply_dataframe()

    def set_header(self, header: list):
        self["columns"] = header
        for col in header:
            self.heading(col, text=col)

        # update df display columns while preserving internal metadata columns
        self._ensure_internal_columns()
        self.df = pd.DataFrame(columns=[*header, self._row_id_col, self._row_tags_col])
        self._sort_state.clear()

    def insert_row(self, values: list, font: Any = None, **tag_conf) -> None:
        if not self["columns"]:
            raise ValueError("Table columns not set. Call set_header() first.")
        if len(values) != len(self["columns"]):
            raise ValueError(f"Expected {len(self['columns'])} values, got {len(values)}")

        tags = ()
        if font:
            tag_name = f"font_{len(self.get_children())}"
            if isinstance(font, dict):
                font_value = (
                    font.get("family", "Arial"),
                    font.get("size", 10),
                    font.get("weight", "normal"),
                )
            else:
                font_value = font
            self.tag_configure(tag_name, font=font_value, **tag_conf)
            tags = (tag_name,)

        self._ensure_internal_columns()
        row_id = self._next_row_id
        self._next_row_id += 1

        row_data = dict(zip(self["columns"], values))
        row_data[self._row_id_col] = row_id
        row_data[self._row_tags_col] = tags

        df_row = pd.DataFrame([row_data])
        self.df = pd.concat([self.df, df_row], ignore_index=True)

        self.insert("", "end", iid=str(row_id), values=values, tags=tags)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Better Entry Demo")
    root.geometry("400x400")

    #Test EnhancedTableView
    tree = EnhancedTableView(root, orient="both", show="headings")
    tree.pack(expand=True, fill=tk.BOTH)

    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [30, 25, 35],
        "City": ["New York", "Los Angeles", "Chicago"]
    })
    tree.df = df
    tree.apply_dataframe()
    tree.insert_row(["David", 28, "San Francisco"], font={"family": "Arial", "size": 10, "weight": "bold"}, foreground="blue")

    root.mainloop() 