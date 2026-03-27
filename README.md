# EasyTk 使用說明 / Usage Guide

[中文](#中文) | [English](#english)

---

## 中文

### EasyTk 使用說明

Tkinter是Python內建GUI套件，其具有高可移植性與相容性的特色，能安裝Python 的電腦幾乎都可順利執行，然而Tkinter本身十分簡潔，許多GUI常用功能需開發者自行實作。

EasyTk 是一個基於 Tkinter 的延伸套件，封裝常用功能，使得利用Tkinter開發更為簡單、快速。

### 開發狀態
✅ BetterEntry     
✅ ScrollableTexrArea     
✅ HyperlinkLabel     
▶️ ScrollableTreeView    
❌ ExtendedTable    
❌ on_click decorator   

## 目錄

- [元件總覽](#元件總覽)
- [快速開始](#快速開始)
- [BetterEntry](#betterentry)
- [ScrollableTextArea](#scrollabletextarea)
- [HyperlinkLabel](#hyperlinklabel)
- [on_click 裝飾器](#on_click-裝飾器)
- [進階元件（widget.py 內）](#進階元件widgetpy-內)
- [注意事項](#注意事項)

## 元件總覽

`__init__.py` 目前對外匯出的 API：

- `BetterEntry`
- `ScrollableTextArea`
- `HyperlinkLabel`
- `on_click`

可直接使用：

```python
from EasyTk import BetterEntry, ScrollableTextArea, HyperlinkLabel, on_click
```

---

## 快速開始

```python
import tkinter as tk
from EasyTk import BetterEntry, ScrollableTextArea, HyperlinkLabel, on_click

root = tk.Tk()
root.geometry("500x300")

entry = BetterEntry(root, placeholder="請輸入關鍵字")
entry.pack(fill="x", padx=10, pady=8)

text = ScrollableTextArea(root, orient="both", wrap=tk.NONE, height=8)
text.pack(fill="both", expand=True, padx=10, pady=8)
text.set_text("初始化完成")

link = HyperlinkLabel(root, text="Open Docs", url="https://www.python.org", fg="blue", cursor="hand2")
link.pack(pady=6)

btn = tk.Button(root, text="送出")
btn.pack(pady=6)

@on_click(btn)
def submit(_event=None):
    text.insert_text("\nclicked")

root.mainloop()
```

---

## BetterEntry

`BetterEntry` 是加強版 `tk.Entry`，支援 placeholder 與 focus 樣式。

### 特色

- `placeholder` 參數：輸入框為空時顯示提示字
- Focus in 時自動清除 placeholder
- Focus out 若無輸入，自動恢復 placeholder

### 範例

```python
entry = BetterEntry(root, placeholder="請輸入帳號")
entry.pack()
```

---

## ScrollableTextArea

`ScrollableTextArea` 是 `tk.Text` 的擴充，內建捲軸，支援垂直/水平/雙向。

### 參數

- `orient`: `"vertical" | "horizontal" | "both"`
- 其餘 `tk.Text` 原生參數可直接傳入

### 常用方法

- `set_state(state)`
- `clear()`
- `insert_text(text, state_after=None)`
- `get_text()`
- `set_text(text, state_after=None, text_color=None)`

### 範例

```python
text = ScrollableTextArea(root, orient="both", wrap=tk.NONE)
text.pack(fill="both", expand=True)
text.set_text("Hello", text_color="green")
```

---

## HyperlinkLabel

`HyperlinkLabel` 是可點擊連結的 `tk.Label`。

### 參數

- `text`: 顯示文字
- `url`: 點擊後開啟網址
- `underscore`: 是否自動加底線（預設 `True`）

### 範例

```python
link = HyperlinkLabel(root, text="GitHub", url="https://github.com", fg="blue", cursor="hand2")
link.pack()
```

---

## on_click 裝飾器

`on_click(widget, *args)` 可把函式直接綁到 `<Button-1>`。

### 行為

- 無參數函式：直接呼叫
- 有提供 `*args`：以 `args` 呼叫函式
- 無 `*args` 且函式需參數：傳入 event

### 範例

```python
btn = tk.Button(root, text="Click")
btn.pack()

@on_click(btn)
def handle_click(event):
    print("clicked", event)
```

---

## 進階元件（widget.py 內）

以下類別目前在 `widget.py` 中可用，但未在 `__init__.py` 對外匯出：

- `ScrollableTreeView`
- `ExtendedTable`（以 pandas DataFrame 載入/顯示）

若要使用可直接 import：

```python
from EasyTk.widget import ScrollableTreeView, ExtendedTable
```

### ScrollableTreeView 簡例

```python
tree = ScrollableTreeView(root, orient="both")
tree.pack(fill="both", expand=True)
tree.set_header(["Name", "Age", "City"])
tree.insert_row(["Alice", "30", "New York"], font={"family": "Arial", "size": 12, "weight": "bold"})
```

### ExtendedTable 簡例

```python
table = ExtendedTable(root, data_file="output.json", orient="both")
table.pack(fill="both", expand=True)
```

---

### 注意事項

1. `ScrollableTextArea` 使用水平捲軸時，建議設定 `wrap=tk.NONE`（元件內也會自動修正）。
2. `ScrollableTreeView` 請先呼叫 `set_header()` 再插入資料。
3. 使用 `ttk.Treeview` 類元件時，請記得 `pack()` / `grid()` / `place()`，否則不會顯示。
4. `ExtendedTable` 依賴 `pandas`。

---

## English

### EasyTk Usage Guide

Tkinter is Python's built-in GUI toolkit. It is highly portable and compatible, and can run on almost any computer with Python installed. However, Tkinter itself is minimal, and many commonly used GUI features must be implemented manually.

EasyTk is an extension package built on top of Tkinter. It encapsulates common features to make Tkinter development simpler and faster.

### Development Status

✅ BetterEntry     
✅ ScrollableTexrArea     
✅ HyperlinkLabel     
▶️ ScrollableTreeView    
❌ ExtendedTable    
❌ on_click decorator   

### Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [BetterEntry](#betterentry)
- [ScrollableTextArea](#scrollabletextarea)
- [HyperlinkLabel](#hyperlinklabel)
- [on_click Decorator](#on_click-decorator)
- [Advanced Widgets (inside widget.py)](#advanced-widgets-inside-widgetpy)
- [Notes](#notes)

### Overview

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

### Quick Start

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

### BetterEntry

`BetterEntry` is an enhanced `tk.Entry` with placeholder text and focus styling.

#### Features

- `placeholder` argument for hint text
- Clears placeholder on focus in
- Restores placeholder on focus out if input is empty

#### Example

```python
entry = BetterEntry(root, placeholder="Enter account")
entry.pack()
```

---

### ScrollableTextArea

`ScrollableTextArea` extends `tk.Text` with built-in scrollbars, supporting vertical/horizontal/both.

#### Parameters

- `orient`: `"vertical" | "horizontal" | "both"`
- Other native `tk.Text` parameters are supported

#### Common Methods

- `set_state(state)`
- `clear()`
- `insert_text(text, state_after=None)`
- `get_text()`
- `set_text(text, state_after=None, text_color=None)`

#### Example

```python
text = ScrollableTextArea(root, orient="both", wrap=tk.NONE)
text.pack(fill="both", expand=True)
text.set_text("Hello", text_color="green")
```

---

### HyperlinkLabel

`HyperlinkLabel` is a clickable `tk.Label` that opens a URL.

#### Parameters

- `text`: display text
- `url`: URL to open on click
- `underscore`: whether to underline text (default `True`)

#### Example

```python
link = HyperlinkLabel(root, text="GitHub", url="https://github.com", fg="blue", cursor="hand2")
link.pack()
```

---

### on_click Decorator

`on_click(widget, *args)` binds a function to `<Button-1>`.

#### Behavior

- Function with no parameters: called directly
- If `*args` is provided: function is called with those arguments
- If no `*args` and function expects parameters: event is passed in

#### Example

```python
btn = tk.Button(root, text="Click")
btn.pack()

@on_click(btn)
def handle_click(event):
    print("clicked", event)
```

---

### Advanced Widgets (inside widget.py)

The following classes are available in `widget.py` but are not exported in `__init__.py`:

- `ScrollableTreeView`
- `ExtendedTable` (DataFrame-based table with pandas)

Import them directly:

```python
from EasyTk.widget import ScrollableTreeView, ExtendedTable
```

#### ScrollableTreeView Example

```python
tree = ScrollableTreeView(root, orient="both")
tree.pack(fill="both", expand=True)
tree.set_header(["Name", "Age", "City"])
tree.insert_row(["Alice", "30", "New York"], font={"family": "Arial", "size": 12, "weight": "bold"})
```

#### ExtendedTable Example

```python
table = ExtendedTable(root, data_file="output.json", orient="both")
table.pack(fill="both", expand=True)
```

---

### Notes

1. For horizontal scrolling in `ScrollableTextArea`, use `wrap=tk.NONE` (the widget also auto-adjusts this).
2. For `ScrollableTreeView`, call `set_header()` before inserting rows.
3. For all Treeview-based widgets, remember to call `pack()` / `grid()` / `place()`.
4. `ExtendedTable` requires `pandas`.
