import os
import sys
import time
import requests
import json

# CONSTANTS
ACT_ID = 'e202102251931481'
URL_GET_STATUS = 'https://sg-hk4e-api.hoyolab.com/event/sol/info'
URL_SIGN = 'https://sg-hk4e-api.hoyolab.com/event/sol/sign'

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

    def __init__(self, name: str, ltoken: str, ltuid: str):
        self.name = name
        self.ltoken = ltoken
        self.ltuid = ltuid
        self.cookies = {'ltoken': self.ltoken, 'ltuid': self.ltuid}

    def get_status(self):
        params = (
            ('lang', 'en-us'),
            ('act_id', ACT_ID)
        )
        response = requests.get(
            URL_GET_STATUS,
            headers=headers,
            params=params,
            cookies=self.cookies,
            timeout=10
        )
        data = response.json()

        if 'message' in data and data.get('retcode') != 0:
            raise CheckinException(data['message'])

        return data['data']['is_sign']

    def sign(self):
        params = (
            ('lang', 'en-us'),
        )
        data = {
            'act_id': ACT_ID
        }
        response = requests.post(
            URL_SIGN,
            headers=headers,
            params=params,
            cookies=self.cookies,
            json=data,
            timeout=5
        )
        data = response.json()

        if 'message' in data and data.get('retcode') != 0:
            raise CheckinException(data['message'])

    def process(self):
        try:
            if not self.get_status():
                self.sign()

                if self.get_status():
                    print(f'Daily check-in rewards have been successfully claimed for {self.name}!')
                    return True
                else:
                    print(f'ERROR: Unable to claim daily check-in rewards for {self.name}...')
            else:
                print(f'Daily check-in rewards have already been claimed today for {self.name}!')
                return True
        except CheckinException as e:
            print(f'Failed daily check-in for {self.name}: {e}')

        return False

if __name__ == '__main__':
    with open('config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    success = True

    for account in data['accounts']:
        checkin = HoyolabCheckin(account['name'], account['ltoken'], account['ltuid'])

        if not checkin.process():
            success = False

    healthcheck = data.get('healthcheck')

    if healthcheck:
        if not success:
            healthcheck += '/fail'

        requests.get(healthcheck, timeout=10)