import os

from dotenv import load_dotenv
load_dotenv()

session_key = os.getenv("TIKTOK_TTS_KEY")
topic = "The Great Gatsby"
topic_path_text = f"texts/{topic}"
topic_path_sound = f"sounds/{topic}"

assert(os.path.exists(topic_path_text))

if os.path.exists(topic_path_sound):
    assert(len(os.listdir(topic_path_sound)))


os.mkdir(topic_path_sound)

# Call the text-to-speech program on command line for each text file in the topic folder and save the output to sounds folder
# The format is "python text_to_speech.py -v en_us 001 -f <input_file> -n <output_path> --session <session_key>". The output is a mp3 file

for filename in os.listdir(topic_path_text):
    input_file = f"{topic_path_text}/{filename}"
    output_path = f"{topic_path_sound}/{filename.split('.')[0]}.mp3"
    os.system(f"python text_to_speech.py -v en_us_001 -f {input_file} -n {output_path} --session {session_key}")