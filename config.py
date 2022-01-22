import os
from dotenv import load_dotenv


def get_token():
    load_dotenv()
    token = os.environ.get("TOKEN")
    print(token)
    return token


class Config:
    TOKEN = get_token()
    PREFIX = "!"

