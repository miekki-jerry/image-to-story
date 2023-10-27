import requests
import os
import replicate
import tempfile

from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
#from langchain import LLMChain, OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain


# Load environment variables
load_dotenv(find_dotenv())
api_token = os.getenv('REPLICATE_API_TOKEN')

# img2text using Hugging Face API
def img2text_hf(image):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    text = image_to_text(image)[0]["generated_text"]
    print(text)
    return text

# img2text using llava-13b replicate API
def img2text_llava(image, prompt=" "):
    # Create a temporary file to save the image
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        image.save(temp_file.name, 'JPEG')
    
    output = replicate.run(
        "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
        input={
            "image": open(temp_file.name, "rb"),
            "prompt": prompt
        }
    )
    
    # Remove the temporary file
    os.remove(temp_file.name)
    
    generated_text = "".join([item for item in output])
    print(generated_text)
    return generated_text

# Function to switch between Hugging Face and Replicate based on a flag
def img2text(image, use_hf=True):
    if use_hf:
        return img2text_hf(image)
    else:
        return img2text_llava(image)


def generate_story(scenario):
    template = """
    You are a story teller;
    You can generate a short story based on a simple narrative, the story should be no more than 50 words. Be creative;
    CONTEXT: {scenario}
    STORY:
    """
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    
    story_llm = LLMChain(llm=ChatOpenAI(
        model_name="gpt-3.5-turbo", temperature=1), prompt=prompt, verbose=True)
    
    story = story_llm.predict(scenario=scenario)

    print (story) 
    return story

def text2speech(message):
    try:
        API_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}"}

        payloads ={
            "inputs": message
        }

        response = requests.post(API_URL, headers=headers, json=payloads)
        with open('audio.flac', 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print("Exception in text2speech:", e)
        
scenario = img2text("test.png")
story = generate_story(scenario)
text2speech(story)