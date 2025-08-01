from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

pipe = None

def load_sd_model():
    global pipe
    if pipe is None:
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float32
        ).to("cpu")
    return pipe

def generate_image_from_prompt(prompt: str, width=512, height=512) -> Image.Image:
    pipe = load_sd_model()
    image = pipe(prompt=prompt, height=height, width=width).images[0]
    return image