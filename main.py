import os
import sys
import time
import requests
import json

# CONSTANTS
GAME_NAMES = {
    'genshin': 'Genshin Impact',
    'starrail': 'Honkai Star Rail'
}
ACT_ID = {
    'genshin': 'e202102251931481',
    'starrail': 'e202303301540311'
}
URL_GET_STATUS = {
    'genshin': 'https://sg-hk4e-api.hoyolab.com/event/sol/info',
    'starrail': 'https://sg-public-api.hoyolab.com/event/luna/os/info'
}
URL_SIGN = {
    'genshin': 'https://sg-hk4e-api.hoyolab.com/event/sol/sign',
    'starrail': 'https://sg-public-api.hoyolab.com/event/luna/os/sign'
}

# REQUEST HEADER & PARAMS
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json;charset=utf-8',
    'Origin': 'https://webstatic-sea.mihoyo.com',
    'Connection': 'keep-alive',
    'Referer': f'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id={ACT_ID}&lang=en-us',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

class CheckinException(Exception):
    pass

class HoyolabCheckin(object):

    def __init__(self, name: str, cookies: dict[str, str]):
        self.name = name
        self.cookies = cookies

    def get_status(self, game: str):
        params = (
            ('lang', 'en-us'),
            ('act_id', ACT_ID[game])
        )
        response = requests.get(
            URL_GET_STATUS[game],
            headers=headers,
            params=params,
            cookies=self.cookies,
            timeout=10
        )
        data = response.json()

        if 'message' in data and data.get('retcode') != 0:
            raise CheckinException(data['message'])

        return data['data']['is_sign']

    def sign(self, game: str):
        params = (
            ('lang', 'en-us'),
        )
        data = {
            'act_id': ACT_ID[game]
        }
        response = requests.post(
            URL_SIGN[game],
            headers=headers,
            params=params,
            cookies=self.cookies,
            json=data,
            timeout=5
        )
        data = response.json()

        if 'message' in data and data.get('retcode') != 0:
            raise CheckinException(data['message'])

    def process_game(self, game: str):
        name = GAME_NAMES[game]

        try:
            if not self.get_status(game):
                self.sign(game)

                if self.get_status(game):
                    print(f'Daily check-in rewards have been successfully claimed for {self.name} on {name}!')
                    return True
                else:
                    print(f'ERROR: Unable to claim daily check-in rewards for {self.name} on {name}...')
            else:
                print(f'Daily check-in rewards have already been claimed today for {self.name} on {name}!')
                return True
        except CheckinException as e:
            print(f'Failed daily check-in for {self.name} on {name}: {e}')

        return False

    def process(self):
        for game in GAME_NAMES.keys():
            if not self.process_game(game):
                return False

        return True

if __name__ == '__main__':
    with open('config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    success = True

    for account in data['accounts']:
        checkin = HoyolabCheckin(account['name'], account['cookies'])

        if not checkin.process():
            success = False

    healthcheck = data.get('healthcheck')

    if healthcheck:
        if not success:
            healthcheck += '/fail'

        requests.get(healthcheck, timeout=10)