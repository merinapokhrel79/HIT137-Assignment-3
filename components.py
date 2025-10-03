import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ScrollableTextDisplay(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, wrap="word", **kwargs)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.pack(fill="both", expand=True)

    def update_text(self, text: str):
        self.config(state="normal")
        self.delete(1.0, tk.END)
        self.insert(tk.END, text)
        self.config(state="disabled")

class ImagePreview(tk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.image = None

    def set_image(self, pil_image: Image.Image):
        # Resize to fit display area
        max_size = (300, 300)
        pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(pil_image)
        self.config(image=self.image)

class LabeledText(tk.Frame):
    def __init__(self, parent, label_text, height=6, width=50):
        super().__init__(parent)
        self.label = ttk.Label(self, text=label_text)
        self.text = tk.Text(self, height=height, width=width, wrap="word")
        self.label.pack(anchor="w")
        self.text.pack(fill="both", expand=True)

    def get_text(self):
        return self.text.get("1.0", tk.END).strip()

    def set_text(self, text: str):
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, text)
        self.text.config(state="disabled")