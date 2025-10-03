import tkinter as tk
from tkinter import ttk, messagebox
from models.sentiment_model import SentimentModel
from models.text_to_image_model import TextToImageModel
from gui.components import ScrollableTextDisplay, LabeledText, ImagePreview
from utils.decorators import log_execution, timing

# ===== OOP Concepts Demonstrated =====

class BaseModel:
    def run(self, input_data):
        raise NotImplementedError

class SentimentHandler(BaseModel):
    def __init__(self):
        self.model = SentimentModel()

    @log_execution
    @timing
    def run(self, text: str):
        return self.model.predict(text)

class TextToImageHandler(BaseModel):
    def __init__(self):
        self.model = TextToImageModel()

    @log_execution
    @timing
    def run(self, prompt: str):
        return self.model.generate(prompt)

# Multiple Inheritance
class InfoProvider:
    def get_sentiment_info(self):
        return (
            "Model Name: distilbert-base-uncased-finetuned-sst-2-english\n"
            "Category: Text Classification\n"
            "Task: Sentiment Analysis (Positive/Negative)\n"
            "Size: ~250MB (lightweight)"
        )

    def get_text_to_image_info(self):
        return (
            "Model Name: stabilityai/stable-diffusion-2-1\n"
            "Category: Text-to-Image Generation\n"
            "Task: Generate 512x512 pixel images from text prompts\n"
            "Size: ~4GB (requires diffusers + transformers + accelerate)"
        )

class OOPExplain:
    def get_oop_explanation(self):
        return (
            "• Multiple Inheritance:\n"
            "  MainApp inherits from tk.Tk, InfoProvider, and OOPExplain.\n\n"
            "• Encapsulation:\n"
            "  Model logic is hidden inside SentimentModel and TextToImageModel.\n\n"
            "• Polymorphism & Method Overriding:\n"
            "  Both handlers inherit from BaseModel and override 'run()'.\n\n"
            "• Multiple Decorators:\n"
            "  @log_execution and @timing applied to 'run()' methods."
        )

class MainApp(tk.Tk, InfoProvider, OOPExplain):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("HIT137 Assignment 3 - AI Models GUI")
        self.geometry("900x800")

        self.sentiment_handler = SentimentHandler()
        self.text_to_image_handler = TextToImageHandler()

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

    def create_widgets(self):
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # Input Section
        input_frame = ttk.LabelFrame(main, text="User Input")
        input_frame.pack(fill="x", pady=(0, 10))

        self.input_area = LabeledText(input_frame, "Enter your text below:", height=6)
        self.input_area.pack(fill="x")

        # Output Section
        output_frame = ttk.LabelFrame(main, text="Model Output")
        output_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Text output area
        self.output_display = ScrollableTextDisplay(output_frame, height=4)
        self.output_display.pack(fill="x", pady=(0, 5))

        # Image preview area
        self.image_preview = ImagePreview(output_frame)
        self.image_preview.pack(pady=5)

        # Buttons: Run Model 1, Run Model 2, Clear
        btn_frame = ttk.Frame(output_frame)
        btn_frame.pack(fill="x", pady=5)

        ttk.Button(btn_frame, text="Run Model 1 (Sentiment)", command=self.run_model1).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Run Model 2 (Text-to-Image)", command=self.run_model2).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_all).pack(side="left", padx=5)

        # Model Info & OOP Explanation
        info_frame = ttk.LabelFrame(main, text="Model Info & OOP Explanation")
        info_frame.pack(fill="both", expand=True)

        left = ttk.Frame(info_frame)
        left.pack(side="left", fill="both", expand=True, padx=5)
        right = ttk.Frame(info_frame)
        right.pack(side="left", fill="both", expand=True, padx=5)

        ttk.Label(left, text="Model 1 Info (Sentiment):").pack(anchor="w")
        info1 = tk.Text(left, height=5, wrap="word")
        info1.insert(tk.END, self.get_sentiment_info())
        info1.config(state="disabled")
        info1.pack(fill="both", expand=True)

        ttk.Label(left, text="Model 2 Info (Text-to-Image):").pack(anchor="w", pady=(10,0))
        info2 = tk.Text(left, height=5, wrap="word")
        info2.insert(tk.END, self.get_text_to_image_info())
        info2.config(state="disabled")
        info2.pack(fill="both", expand=True)

        ttk.Label(right, text="OOP Concepts Explanation:").pack(anchor="w")
        oop_text = tk.Text(right, wrap="word")
        oop_text.insert(tk.END, self.get_oop_explanation())
        oop_text.config(state="disabled")
        oop_text.pack(fill="both", expand=True)

    def run_model1(self):
        text = self.input_area.get_text()
        if not text:
            messagebox.showwarning("Input Required", "Please enter some text.")
            return
        try:
            result = self.sentiment_handler.run(text)
            output = f"[Sentiment Analysis]\nLabel: {result['label']}\nConfidence: {result['confidence']}"
            self.output_display.update_text(output)
            self.image_preview.config(image=None)  # Clear image
        except Exception as e:
            messagebox.showerror("Error", f"Model 1 failed: {str(e)}")

    def run_model2(self):
        prompt = self.input_area.get_text()
        if not prompt:
            messagebox.showwarning("Input Required", "Please enter a text prompt.")
            return
        try:
            # Show loading message
            self.output_display.update_text("[Generating image... Please wait 1-5 minutes on CPU]")
            image = self.text_to_image_handler.run(prompt)
            self.image_preview.set_image(image)
            self.output_display.update_text(f"[Text-to-Image Generated]\nPrompt: {prompt}")
        except Exception as e:
            messagebox.showerror("Error", f"Model 2 failed: {str(e)}")

    def clear_all(self):
        self.input_area.set_text("")
        self.output_display.update_text("")
        self.image_preview.config(image=None)