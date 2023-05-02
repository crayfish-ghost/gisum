import os, openai
import requests
from .read_config import config

def create_gpt_message (prompt):
    message = [
        {"role": "system", "content": config.get('gpt','system_prompt') },
        {"role": "user", "content": prompt }
    ]
    return message

def get_response(prompt):
    response = openai.ChatCompletion.create(
        model       = config.get('gpt','model'),
        temperature = config.getfloat('gpt','temperature') ,
        messages    =  create_gpt_message(prompt) ,
        timeout     = config.getint('gpt','timeout')
    )
    return response['choices'][0]['message']['content']
