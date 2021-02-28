import tkinter as tk
from tkinter import ttk
from hashlib import md5
from base64 import b64encode

import resource


class md5clip(tk.Tk):
    def __init__(self):
        super().__init__()
        self.test()
        self.setup()
        self.mainloop()

    def setup(self):
        self.is_countdown = False
        self.config_window()
        self.config_label()
        self.config_entry()

    def config_window(self):
        w, h = 400, 100
        title = "md5clip"
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(0,0)
        icon = resource.icon()
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(data=icon))
        self.title(title)
        self.protocol('WM_DELETE_WINDOW', self.delete_window)

    def config_label(self):
        px, py = 10, 10
        text = "input text:"
        self.label = ttk.Label(self)
        self.label.pack(ipadx=px, ipady=py, fill=tk.X)
        self.label.config(text=text, anchor=tk.S)

    def config_entry(self):
        px, py = 10, 10
        mask = "*"
        self.entry = ttk.Entry(self)
        self.entry.pack(padx=px, pady=py, fill=tk.X)
        self.entry.config(show=mask)
        self.entry.bind('<Return>', self.entry_return)
        self.entry.focus_set()

    def entry_return(self, event):
        timeout = 10
        self.entry.config(state='readonly')
        hash = self.hash(self.entry.get())
        code = self.code(hash)
        self.clipboard_clear()
        self.clipboard_append(code)
        self.is_countdown = True
        self.timelimit = timeout
        self.timer()

    def timer(self):
        wait = 1000
        text = "code copied to clipboard. " \
               "clipboard will be cleared when after %dsec." % (self.timelimit)
        self.label.config(text=text)
        self.timelimit = self.timelimit - 1
        if self.timelimit < 0:
            self.delete_window()
        else:
            self.after(wait, self.timer)

    def delete_window(self):
        if self.is_countdown:
            self.clipboard_clear()
            self.clipboard_append('')
        self.destroy()

    def hash(self, text):
        if not isinstance(text, str):
            raise TypeError("hash() require str.")
        text = text.encode('utf-8')
        return md5(text).hexdigest()

    def code(self, text):
        if not isinstance(text, str):
            raise TypeError("code() require str.")
        text = text.encode('utf-8')
        return b64encode(text).decode()

    def test(self):
        self.test_hash()
        self.test_code()

    def test_hash(self):
        validation_text = '123'
        validation_hash = '202cb962ac59075b964b07152d234b70'
        validation_code = 'MjAyY2I5NjJhYzU5MDc1Yjk2NGIwNzE1MmQyMzRiNzA='
        calculated_hash = self.hash(validation_text)
        if not calculated_hash == validation_hash:
            raise ValueError("test_hash fail.")

    def test_code(self):
        validation_text = '123'
        validation_hash = '202cb962ac59075b964b07152d234b70'
        validation_code = 'MjAyY2I5NjJhYzU5MDc1Yjk2NGIwNzE1MmQyMzRiNzA='
        calculated_code = self.code(validation_hash)
        if not calculated_code == validation_code:
            raise ValueError("test_code fail.")


md5clip()