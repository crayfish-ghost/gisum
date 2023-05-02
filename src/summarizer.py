import os, openai
import requests
import tiktoken
from tiktoken.core import Encoding
from .read_config import config
from . import chatgpt

encoding: Encoding = tiktoken.encoding_for_model(config.get('gpt','model'))

OUTPUT_FORMAT = """
Output should follow the format below.

議論のテーマ:{subject}
ステータス:{state}
内容:{summary}
"""


def get_gpt_response(text, tpr):
    message = create_gpt_message(text)
    response = openai.ChatCompletion.create(
        model       = config.get('gpt','model'),
        temperature = config.getfloat('gpt','temperature'),
        messages    = message,
        timeout     = config.getint('gpt','timeout')
    )
    return response['choices'][0]['message']['content']

def get_token_num(text):
    return len( encoding.encode(text) )

def get_prompt_text(comments, inter_summary):
    result = inter_summary
    while get_token_num(result) + get_token_num(comments[0]) < 3000:
        result += comments.pop(0)
        if len(comments) == 0:
            break

    return result

def create_prompt(text, is_last, has_summary):
    prompt = config.get('prompt','header')
    if has_summary:
        prompt +=  "Summary of the discussion so far:" + text + "\n==\n\n" + config.get('prompt','has_summary')
    else:
        prompt += text + config.get('prompt','comment_only')

    if is_last:
        # 最終的に表示する要約
        prompt += config.get('prompt','do_summarize').format(WORD_NUM=config.get('other','summary_word_num'), LANG=config.get('other','summary_language')) + config.get('prompt','make_easy') + OUTPUT_FORMAT
    else:
        # 部分的な要約
        prompt += config.get('prompt','do_summarize').format(WORD_NUM=config.get('other','inter_summary_word_num'), LANG=config.get('other','inter_summary_language'))

    return prompt

def get_summary(text, is_last, has_summary):
    prompt = create_prompt(text, is_last, has_summary)
    return chatgpt.get_response(prompt)
    
def summarize(issue_comments):
    inter_summary = ""
    has_summary = False
    while len(issue_comments) > 0:
        next_prompt_text = get_prompt_text(issue_comments
                                       ,inter_summary)

        is_last = len(issue_comments) == 0
        inter_summary = get_summary(next_prompt_text, is_last, has_summary)
        inter_summary += "\n\n"
        has_summary = True
        
    return inter_summary
