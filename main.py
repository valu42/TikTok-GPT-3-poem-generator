import os
import openai
import sys
from PIL import Image, ImageDraw, ImageFont
from mutagen.mp3 import MP3
import random
import moviepy.editor as mp

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
topic = sys.argv[1]

text_path = f"texts/{''.join([word.capitalize() for word in topic.split()])}"
sound_path = f"sounds/{''.join([word.capitalize() for word in topic.split()])}"
image_path = f"images/{''.join([word.capitalize() for word in topic.split()])}"
assets_path = f"assets/{''.join([word.capitalize() for word in topic.split()])}"

def generate_text():
    
    prompt = f"Write me a poem that rhymes about {topic}."
    model = "text-davinci-003"
    response = openai.Completion.create(model=model, prompt=prompt, temperature=0.7, max_tokens=200)
    response = response.choices[0].text

    rows = response.split("\n")
    paragraphs_array = [[]]
    for row in rows:
        if row == '':
            paragraphs_array.append([])
        else:
            paragraphs_array[-1].append(row)

    paragraphs = [".\n".join(paragraph) for paragraph in paragraphs_array if len(paragraph) != 0]

    assert(not os.path.exists(text_path))

    os.mkdir(text_path)

    for idx, paragraph in enumerate(paragraphs):
        with open(f"{text_path}/{idx}.txt", "w") as f:
            f.write(paragraph)

def generate_speech():

    session_key = os.getenv("TIKTOK_TTS_KEY")

    assert(os.path.exists(text_path))

    if os.path.exists(sound_path):
        assert(len(os.listdir(sound_path)) == 0)

    os.mkdir(sound_path)

    for filename in os.listdir(text_path):
        input_file = f"{text_path}/{filename}"
        output_path = f"{sound_path}/{filename.split('.')[0]}.mp3"
        os.system(f'python text_to_speech.py -v en_us_001 -f "{input_file}" -n "{output_path}" --session {session_key}')

def generate_image_from_text(text):

    width = 1024
    height = 1024
    
    img = Image.new('RGB', (width, height), color="white")
    font = ImageFont.truetype("arial.ttf", 20)
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(text, font=font)
    widthBuffer, heightBuffer = 20, 40
    left, top, right, bottom = 0, 0, textWidth + 2*widthBuffer, textHeight + 2*heightBuffer
    imgDraw.text((widthBuffer,heightBuffer), text, font=font, fill="black")
    img = img.crop((left, top, right, bottom))

    return img

def generate_image():

    assert(os.path.exists(text_path))
    assert(not os.path.exists(image_path))

    os.mkdir(image_path)
    
    for filename in os.listdir(text_path):
        with open(f"{text_path}/{filename}", "r") as f:
            text = f.read()
            text = text.replace(".", "")

        img = generate_image_from_text(text)
        print(f"{image_path}/{filename.split('.')[0]}.png")
        img.save(f"{image_path}/{filename.split('.')[0]}.png")

def calculate_length():
    # Calculates the length of the sound files in seconds
    length = 0
    for filename in os.listdir(sound_path):
        audio = MP3(f"{sound_path}/{filename}")
        length += audio.info.length
    return length

def random_asset():
    video = mp.VideoFileClip(random.choice(os.listdir(assets_path)))
    
    return video



generate_text()
generate_speech()
generate_image()
