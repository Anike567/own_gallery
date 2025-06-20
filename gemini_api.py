

from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyATQ05oQeJmV17uAEsUsFlJenz-p5unjEU")


def get_response(prompt):
    
    response = client.models.generate_content(
     model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) 
        ),
    )
    print(response.text)

prompt = ""
while(True):
    prompt = input("Hi how can  i help you , press 0 to exit")

    if prompt == 0 :
        break

    get_response(prompt)