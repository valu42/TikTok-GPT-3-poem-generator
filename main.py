import os
import openai
import sys
from PIL import Image, ImageDraw, ImageFont
from mutagen.mp3 import MP3
import random
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# The video splitting command: ffmpeg -i input.mp4 -c copy -map 0 -segment_time 00:20:00 -f segment output%03d.mp4


def generate_text():
    
    prompt = f"Write me a poem that rhymes about {topic}."
    model = "text-davinci-003"
    response = openai.Completion.create(model=model, prompt=prompt, temperature=0.7, max_tokens=400)
    starting_paragraph = f"""A poem about \n{topic}\nwritten by GPT-3.\n\n"""
    response = starting_paragraph + response.choices[0].text

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
        os.system(f'python3 text_to_speech.py -v en_us_001 -f "{input_file}" -n "{output_path}" --session {session_key}')

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
        img.save(f"{image_path}/{filename.split('.')[0]}.png")

def calculate_length():
    # Calculates the length of the sound files in seconds
    length = 0
    for filename in os.listdir(sound_path):
        audio = MP3(f"{sound_path}/{filename}")
        length += audio.info.length + 1
    return length

def random_asset():
    video = mp.VideoFileClip(f"{assets_path}/{random.choice(os.listdir(assets_path))}")
    length = calculate_length()
    snipped_video = video.subclip(0, length)
    return snipped_video

def create_video(mode):
    assert(os.path.exists(sound_path))
    assert(not os.path.exists(video_path))
    print(video_path)

    video = random_asset()
    width, height = video.size
    starting_point = 0
    if mode == "portrait":
        right_width = height * (1080 / 1920)
        video = video.crop(x1 = (width - right_width) / 2, y1 = 0, x2 = (width + right_width) / 2, y2 = height)
        width = right_width

    # Add the images of the text to the video clip
    for filenumber in range(len(os.listdir(sound_path))):
        audio = mp.AudioFileClip(f"{sound_path}/{filenumber}.mp3")
        
        if mode == "portrait":
            text_width = int(width - 30)
        else:
            text_height = int(height / 4)

        image = Image.open(f"{image_path}/{filenumber}.png")
        if mode == "portrait":
            image_video = mp.ImageClip(f"{image_path}/{filenumber}.png").set_duration(audio.duration).set_audio(audio).set_start(starting_point).resize(width=text_width)
            image_video = image_video.set_pos(((width - image.width) // 2, 30))
        else:
            image_video = mp.ImageClip(f"{image_path}/{filenumber}.png").set_duration(audio.duration).set_audio(audio).set_start(starting_point).resize(height=text_height)
            image_video = image_video.set_pos((30, (height - image.height) // 2))
        print("image_video width:", image_video.w, "height:", image_video.h)
        starting_point += audio.duration + 1
        video = mp.CompositeVideoClip([video, image_video])

    video.write_videofile(f"{video_path}.mp4", fps=24, codec="libx264", audio_codec="aac")

def video_from_files(mode):
    assert(os.path.exists(image_path))
    assert(os.path.exists(sound_path))
    create_video(mode)

def video_from_topic():
    generate_text()
    generate_speech()
    generate_image()
    create_video(mode)

topic = sys.argv[1]
filename = ""
number_of_topics = 0
if topic == "file":
    filename = sys.argv[2]
    number_of_topics = int(sys.argv[3])

    topics = []
    with open(filename, "r") as f:
        counter = 0
        for line in f.readlines():
            counter += 1
            if counter >= number_of_topics:
                break 
            topics.append(line.strip())
else:
    topics = [topic]

mode = "landscape"

for topic in topics:
    text_path = f"texts/{''.join([word.capitalize() for word in topic.split()])}"
    sound_path = f"sounds/{''.join([word.capitalize() for word in topic.split()])}"
    image_path = f"images/{''.join([word.capitalize() for word in topic.split()])}"
    assets_path = f"assets/"
    video_path = f"videos/{''.join([word.capitalize() for word in topic.split()])}"

    if os.path.exists(image_path) and os.path.exists(sound_path):
        video_from_files(mode)
    else:
        video_from_topic(mode)
