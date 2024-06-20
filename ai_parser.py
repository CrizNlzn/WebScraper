# AI Parsing Logic 

import openai

openai.api_key = 'your-api-key'

def ai_assist_parsing(raw_data):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Extract an image URL, title, and summary from this text:\n\n{raw_data}",
        max_tokens=100
    )
    return response.choices[0].text.strip()
