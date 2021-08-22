import pickle
import tkinter as tk
from tkinter import ttk
from hashlib import md5
from base64 import b64encode


import clipboard

import resource


class md5clip(tk.Tk):

    def __init__(self):
        super().__init__()
        self.test()
        self.setup()
        self.mainloop()

    def setup(self):
        self.config_filename = "iterates.txt"
        self.is_countdown = False
        self.config_window()
        self.config_label()
        self.config_spinbox()
        self.config_entry()

    def config_window(self):
        w, h = 480, 120
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
        text = "set stretching iterates and input plain text:"
        self.label = ttk.Label(self)
        self.label.pack(ipadx=px, ipady=py)
        self.label.config(text=text, anchor=tk.S)

    def config_spinbox(self):
        px, py = 10, 10
        self.load_iterates()
        self.spinbox = ttk.Spinbox(self,
            textvariable = self.iterates,
            from_=1, to=1000000000, increment=1000,
            justify='right',
            validate = 'key',
            validatecommand=(self.register(self.key_validation), '%S')
        )
        self.spinbox.pack(padx=px, pady=py, expand=False)

    def key_validation(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def config_entry(self):
        px, py = 10, 10
        mask = "*"
        self.entry = ttk.Entry(self)
        self.entry.pack(padx=px, pady=py, fill=tk.X)
        self.entry.config(show=mask)
        self.entry.bind('<Return>', self.entry_return)
        self.entry.focus_set()

    def entry_return(self, event):
        self.spinbox.config(state='disable')
        self.entry.config(state='disable')
        self.label.config(text="hashing")
        self.after(1, self.calc)

    def calc(self):
        n = int(self.iterates.get())
        hash = self.entry.get()
        for i in range(n):
            hash = self.hash(hash)
        code = self.code(hash)
        clipboard.copy(code)
        timeout = 10
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
            clipboard.copy('')
        self.dump_iterates()
        self.destroy()

    def load_iterates(self):
        try:
            with open(self.config_filename, 'rb') as f:
                self.iterates = tk.StringVar(value=pickle.load(f))
        except:
            initial_value = 100000
            self.iterates = tk.StringVar(value=initial_value)

    def dump_iterates(self):
        try:
            with open(self.config_filename ,'wb') as f:
                pickle.dump(self.iterates.get(), f)
        except:
            pass

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


if __name__ == '__main__':
    md5clip()
