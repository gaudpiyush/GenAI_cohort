from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI()

text = "dog chases cat"

response = client.embeddings.create(
    model = "text-embedding-3-small", 
    input=text
)

print(response)