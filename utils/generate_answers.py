from openai import OpenAI
import os

ai_token = os.getenv('OPENAI_API')
client = OpenAI(api_key = ai_token)
def generate_answers(questions):
    # Use the ChatCompletion endpoint for GPT models
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use 'gpt-4' if you have access
        messages=[
            {"role": "system", "content": "Answer all questions by including the questions and their corresponding answers."},
            {"role": "user", "content": questions}
        ]
    )


    return response.choices[0].message.content.strip()