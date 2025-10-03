from diffusers import StableDiffusionPipeline
from PIL import Image
import torch

class TextToImageModel:
    def __init__(self):
        # Load model on CPU
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1",
            torch_dtype=torch.float32,  # CPU-friendly
            revision="fp16"
        )
        self.pipe.to("cpu")  # Force CPU
        self.pipe.safety_checker = None  # Optional: Disable safety checker for faster CPU inference

    def generate(self, prompt: str, num_inference_steps=20) -> Image.Image:
        # Generate image
        image = self.pipe(prompt, num_inference_steps=num_inference_steps).images[0]
        return image

    def get_image_bytes(self, image: Image.Image) -> bytes:
        from io import BytesIO
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()