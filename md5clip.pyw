import hashlib
import tkinter as tk
from tkinter import ttk


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
        self.title("md5clip")
        w, h = 400, 100
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.WM_DELETE_WINDOW)

    def config_label(self):
        px, py = 10, 10
        text = "input text:"
        self.label = ttk.Label(self)
        self.label.pack(ipadx=px, ipady=py, fill=tk.X)
        self.label.config(text=text, anchor=tk.S)

    def config_entry(self):
        px, py = 10, 10
        show = '*'
        self.entry = ttk.Entry(self)
        self.entry.pack(padx=px, pady=py, fill=tk.X)
        self.entry.config(show=show)
        self.entry.bind('<Return>', self.entry_Return)
        self.entry.focus_set()

    def entry_Return(self, event):
        timeout = 10
        self.entry.config(state='readonly')
        hash = self.digest(self.entry.get())
        self.clipboard_clear()
        self.clipboard_append(hash)
        self.is_countdown = True
        self.sec = timeout
        self.timer()

    def timer(self):
        text = "hash copied to clipboard. clipboard will be cleared when after %dsec." % (self.sec)
        self.label.config(text=text)
        self.sec = self.sec - 1
        if self.sec < 0:
            self.WM_DELETE_WINDOW()
        else:
            self.after(1000, self.timer)

    def WM_DELETE_WINDOW(self):
        print("close window")
        if self.is_countdown:
            self.clipboard_clear()
        self.destroy()

    def digest(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def test(self):
        self.test_digest()

    def test_digest(self):
        validation_text = '123'
        validation_hash = '202cb962ac59075b964b07152d234b70'
        calculated_hash = self.digest(validation_text)
        if not calculated_hash == validation_hash:
            raise ValueError(calculated_hash)


md5clip()