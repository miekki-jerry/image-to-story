#this is testing file for replicate-lava model connection

import requests
import os
import replicate
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Fetch REPLICATE_API_TOKEN from environment variables
api_token = os.getenv('REPLICATE_API_TOKEN')

if api_token is None:
    raise EnvironmentError("REPLICATE_API_TOKEN is not set in the environment.")

# Using llava-13b replicate API
def img2text_lava(image_path, prompt=" "):

    # Ensure the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    output = replicate.run(
        "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
        input={
            "image": open(image_path, "rb"),
            "prompt": prompt
        }
    )

    generated_text = ""
    for item in output:
        print(item, end="")
        generated_text += item

    return generated_text

# Example usage
output_text = img2text_lava("/Users/piter/Documents/programowanko/img_to_story/test.png")
print("Generated Text:", output_text)
