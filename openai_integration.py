from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
import os


def generate_gpt_response(prompt: str) -> str:
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a fan of movies and TV Shows(Series) and you always seek to recommend the best shows and movies to your users. You have an excited tone when the movie has a high rating and a regular tone when the movie isn't so good you also show the rating of the movie at the end of your response. Your tone should sound first person (you have watched the movie already). You also recommend similar or better movies in the same category"},
        {"role": "user", "content": prompt},
    ])
    return response.choices[0].message.content.strip()

def generate_condensed_summary(title: str) -> str:
    filename = f"{title.replace(' ', '_')}.txt"
    with open(filename, 'r') as file:
        file_content = file.read()

    openai_response = client.completions.create(engine="gpt-4",
    prompt=file_content,
    max_tokens=250)

    condensed_summary = openai_response.choices[0].text.strip()

    return condensed_summary