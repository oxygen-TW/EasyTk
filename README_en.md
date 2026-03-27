# EasyTk Usage Guide

Tkinter is Python's built-in GUI toolkit. It is highly portable and compatible, and can run on almost any computer with Python installed. However, Tkinter itself is minimal, and many commonly used GUI features must be implemented manually.

EasyTk is an extension package built on top of Tkinter. It encapsulates common features to make Tkinter development simpler and faster.

## Table of Contents

- [EasyTk Usage Guide](#easytk-usage-guide)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Development Status](#development-status)
  - [Quick Start](#quick-start)
  - [BetterEntry](#betterentry)
    - [Features](#features)
    - [Example](#example)
  - [ScrollableTextArea](#scrollabletextarea)
    - [Parameters](#parameters)
    - [Common Methods](#common-methods)
    - [Example](#example-1)
  - [HyperlinkLabel](#hyperlinklabel)
    - [Parameters](#parameters-1)
    - [Example](#example-2)
  - [on\_click Decorator](#on_click-decorator)
    - [Behavior](#behavior)
    - [Example](#example-3)
  - [Advanced Widgets (inside widget.py)](#advanced-widgets-inside-widgetpy)
    - [ScrollableTreeView Example](#scrollabletreeview-example)
    - [ExtendedTable Example](#extendedtable-example)
  - [Notes](#notes)

## Overview

Public API exported by `__init__.py`:

- `BetterEntry`
- `ScrollableTextArea`
- `HyperlinkLabel`
- `on_click`

Import directly with:

```python
from EasyTk import BetterEntry, ScrollableTextArea, HyperlinkLabel, on_click
```

---

### Development Status
✅ BetterEntry     
✅ ScrollableTexrArea     
✅ HyperlinkLabel     
▶️ ScrollableTreeView    
❌ ExtendedTable    
❌ on_click decorator   

---
## Quick Start

```python
import tkinter as tk
from EasyTk import BetterEntry, ScrollableTextArea, HyperlinkLabel, on_click

root = tk.Tk()
root.geometry("500x300")

entry = BetterEntry(root, placeholder="Type keywords here")
entry.pack(fill="x", padx=10, pady=8)

text = ScrollableTextArea(root, orient="both", wrap=tk.NONE, height=8)
text.pack(fill="both", expand=True, padx=10, pady=8)
text.set_text("Initialized")

link = HyperlinkLabel(root, text="Open Docs", url="https://www.python.org", fg="blue", cursor="hand2")
link.pack(pady=6)

btn = tk.Button(root, text="Submit")
btn.pack(pady=6)

@on_click(btn)
def submit(_event=None):
    text.insert_text("\nclicked")

root.mainloop()
```

---

## BetterEntry

`BetterEntry` is an enhanced `tk.Entry` with placeholder text and focus styling.

### Features

- `placeholder` argument for hint text
- Clears placeholder on focus in
- Restores placeholder on focus out if input is empty

### Example

```python
entry = BetterEntry(root, placeholder="Enter account")
entry.pack()
```

---

## ScrollableTextArea

`ScrollableTextArea` extends `tk.Text` with built-in scrollbars, supporting vertical/horizontal/both.

### Parameters

- `orient`: `"vertical" | "horizontal" | "both"`
- Other native `tk.Text` parameters are supported

### Common Methods

- `set_state(state)`
- `clear()`
- `insert_text(text, state_after=None)`
- `get_text()`
- `set_text(text, state_after=None, text_color=None)`

### Example

```python
text = ScrollableTextArea(root, orient="both", wrap=tk.NONE)
text.pack(fill="both", expand=True)
text.set_text("Hello", text_color="green")
```

---

## HyperlinkLabel

`HyperlinkLabel` is a clickable `tk.Label` that opens a URL.

### Parameters

- `text`: display text
- `url`: URL to open on click
- `underscore`: whether to underline text (default `True`)

### Example

```python
link = HyperlinkLabel(root, text="GitHub", url="https://github.com", fg="blue", cursor="hand2")
link.pack()
```

---

## on_click Decorator

`on_click(widget, *args)` binds a function to `<Button-1>`.

### Behavior

- Function with no parameters: called directly
- If `*args` is provided: function is called with those arguments
- If no `*args` and function expects parameters: event is passed in

### Example

```python
btn = tk.Button(root, text="Click")
btn.pack()

@on_click(btn)
def handle_click(event):
    print("clicked", event)
```

---

## Advanced Widgets (inside widget.py)

The following classes are available in `widget.py` but are not exported in `__init__.py`:

- `ScrollableTreeView`
- `ExtendedTable` (DataFrame-based table with pandas)

Import them directly:

```python
from EasyTk.widget import ScrollableTreeView, ExtendedTable
```

### ScrollableTreeView Example

```python
tree = ScrollableTreeView(root, orient="both")
tree.pack(fill="both", expand=True)
tree.set_header(["Name", "Age", "City"])
tree.insert_row(["Alice", "30", "New York"], font={"family": "Arial", "size": 12, "weight": "bold"})
```

### ExtendedTable Example

```python
table = ExtendedTable(root, data_file="output.json", orient="both")
table.pack(fill="both", expand=True)
```

---

## Notes

1. For horizontal scrolling in `ScrollableTextArea`, use `wrap=tk.NONE` (the widget also auto-adjusts this).
2. For `ScrollableTreeView`, call `set_header()` before inserting rows.
3. For all Treeview-based widgets, remember to call `pack()` / `grid()` / `place()`.
4. `ExtendedTable` requires `pandas`.
