import openai
import os

openai.api_key = os.getenv("OPEN_API_KEY")

def get_llm_response(task, content):
    prompt = create_prompt(task, content)
    model_name = "gpt-3.5-turbo" 
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def create_prompt(task, content):
    if task == "create":
        return f"You are a skilled teacher. Create teaching material based on:\n\n{content}"
    elif task == "feedback":
        return f"You are a skilled teacher. Provide detailed feedback on this student submission:\n\n{content}"
    elif task == "grade":
        return f"You are a skilled teacher. Grade this student submission based on standard rubric:\n\n{content}"
    else:
        return f"Analyze this content:\n\n{content}"
