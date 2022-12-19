import os
import openai

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
texts_folder = "texts"


topic = "The Great Gatsby"
prompt = f"Write me a rhyming poem about {topic}."
model = "text-davinci-003"
#response = openai.Completion.create(model=model, prompt=prompt, temperature=0.7, max_tokens=200)
response = """Fitzgerald’s Gatsby is truly great,
His parties and loves make us elate.
His riches, his charm, and his swagger,
We’ll never forget such a grandiose figure.

His mansion is grand and his car is a sight,
His guests come from near and far in the night.
His wealth and his style, can’t be denied,
His dreams are so big, one can’t help but abide.

His love for Daisy is strong and true,
Though in the end, it won’t do.
His dream to be part of a better class,
Shows what a great figure Gatsby was.
"""

rows = response.split("\n")
paragraphs_array = [[]]
for row in rows:
    if row == '':
        paragraphs_array.append([])
    else:
        paragraphs_array[-1].append(row)

paragraphs = ["\n".join(paragraph) for paragraph in paragraphs_array if len(paragraph) != 0]

topic_path = f"{texts_folder}/{''.join(topic.split())}"
assert(not os.path.exists(topic_path))

os.mkdir(topic_path)

for idx, paragraph in enumerate(paragraphs):
    with open(f"{topic_path}/{idx}.txt", "w") as filu:
        filu.write(paragraph)

