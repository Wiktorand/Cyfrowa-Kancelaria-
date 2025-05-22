import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Cześć, czy działa API?"}]
)
print(response.choices[0].message.content)
