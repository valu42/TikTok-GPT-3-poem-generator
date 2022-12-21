import os
import openai
import sys

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
texts_folder = "texts"



topic = sys.argv[1]
prompt = f"Write me a rhyming poem about {topic}."
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

paragraphs = ["\n".join(paragraph) for paragraph in paragraphs_array if len(paragraph) != 0]

topic_path = f"{texts_folder}/{topic}"
assert(not os.path.exists(topic_path))

os.mkdir(topic_path)

for idx, paragraph in enumerate(paragraphs):
    with open(f"{topic_path}/{idx}.txt", "w") as filu:
        filu.write(paragraph)

