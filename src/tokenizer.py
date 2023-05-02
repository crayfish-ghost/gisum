import tiktoken
from tiktoken.core import Encoding
from .read_config import config
encoding: Encoding = tiktoken.encoding_for_model(config.get('gpt','model'))

def get_token_num(text):
    return len( encoding.encode(text) )
