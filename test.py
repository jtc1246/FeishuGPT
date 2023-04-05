from FeishuGPT import gpt_3_5_v2 as gpt
from time import sleep
from FeishuGPT import gpt_4_v2 as gpt4


APP_ID = "cli_xxxxxx"
APP_SECRET = "xxxxxxxxxx"
VERIFICATION_TOKEN = 'xxxxxxxx'
OPENAI_API_KEY = "sk-xxxxxxx"
APP_ID_4 = 'cli_xxxxx'
APP_SECRET_4 = 'xxxxxxxxx'
VERIFICATION_TOKEN_4 = 'xxxxxxxx'

gpt.start_async(APP_ID, APP_SECRET, VERIFICATION_TOKEN, OPENAI_API_KEY, 80)
gpt4.start_async(APP_ID_4, APP_SECRET_4, VERIFICATION_TOKEN_4, OPENAI_API_KEY, 81)
while True:
    sleep(10)
