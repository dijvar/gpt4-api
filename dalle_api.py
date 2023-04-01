import openai
import requests
import os
from PIL import Image

class DalleApi:
    def __init__(self, api_key, image_dir="images", default_size="1024x1024", default_n=1, max_n=5, max_prompt_length=1000):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.image_dir = image_dir
        self.default_size = default_size
        self.default_n = default_n
        self.max_n = max_n
        self.max_prompt_length = max_prompt_length

        if not os.path.isdir(self.image_dir):
            os.mkdir(self.image_dir)

    def create_image(self, prompt, n=None, size=None):
        if n is None:
            n = self.default_n
        if size is None:
            size = self.default_size

        if len(prompt) > self.max_prompt_length:
            return {"error": "Prompt exceeds the maximum allowed length."}

        if n > self.max_n:
            return {"error": "Number of images exceeds the maximum allowed value."}

        response = openai.Image.create(
            prompt=prompt,
            n=n,
            size=size,
            response_format="url",
        )
        return response

    def save_image(self, image_url, file_name):
        file_path = os.path.join(self.image_dir, file_name)
        image_content = requests.get(image_url).content

        with open(file_path, "wb") as image_file:
            image_file.write(image_content)
        return file_path

    def create_variation(self, image, n=None, size=None):
        if n is None:
            n = self.default_n
        if size is None:
            size = self.default_size

        if n > self.max_n:
            return {"error": "Number of variations exceeds the maximum allowed value."}

        response = openai.Image.create_variation(
            image=image,
            n=n,
            size=size,
            response_format="url",
        )
        return response

    def create_edit(self, image, prompt, n=None, size=None, mask_area='bottom_half'):
        if n is None:
            n = self.default_n
        if size is None:
            size = self.default_size

        if len(prompt) > self.max_prompt_length:
            return {"error": "Prompt exceeds the maximum allowed length."}

        if n > self.max_n:
            return {"error": "Number of edits exceeds the maximum allowed value."}

        mask_path = self.create_mask(size, mask_area)

        response = openai.Image.create_edit(
            image=image,
            mask=open(mask_path, "rb"),
            prompt=prompt,
            n=n,
            size=size,
            response_format="url",
        )
        return response

    def create_mask(self, size, mask_area):
        width, height = tuple(map(int, size.split("x")))
        mask = Image.new("RGBA", (width, height), (0, 0, 0, 1))

        if mask_area == 'bottom_half':
            for x in range(width):
                for y in range(height // 2, height):
                    alpha = 0
                    mask.putpixel((x, y), (0, 0, 0, alpha))

        mask_name = "mask.png"
        mask_filepath = os.path.join(self.image_dir, mask_name)
        mask.save(mask_filepath)

        return mask_filepath
    
    

    def resize_image(self, input_image_path, output_size="1024x1024"):
        img = Image.open(input_image_path)
        width, height = tuple(map(int, output_size.split("x")))
        img_resized = img.resize((width, height), Image.ANTIALIAS)

        # Save the resized image as a PNG
        resized_image_path = os.path.join(self.image_dir, "resized_image.png")
        img_resized.save(resized_image_path, "PNG")


        return resized_image_path


