from coinbase.wallet.client import Client
from dotenv import load_dotenv
import sched, time
import datetime
import requests
import json
import os

load_dotenv()

API= os.getenv("API")
APIsecrect= os.getenv("APIsecrect")
TEXT_API= os.getenv("TEXT_API")

DesireAmount = float( os.getenv("DesireAmount"))
DesireAmount_LOW = float(os.getenv("DesireAmount_LOW"))
scheduler = sched.scheduler(time.time, time.sleep)
isAnni = False
isNotify = False

def checkPrice():
    client = Client( API, APIsecrect)

    data = client.get_sell_price(currency_pair = 'ETH-USD')
    return data

def sendNoti(message, phone):
    req = requests.post('https://textbelt.com/text', {
      'phone': phone,
      'message':  message,
      'key': TEXT_API,})
    return req.json()



def checkQuotaCount():
    req = requests.post('https://textbelt.com/text', {
        'phone': '6263213319',
        'message': 'testing',
        'key': TEXT_API + '_test', })
    status = req.json()
    if status['quotaRemaining'] < 10:
        requests.post('https://textbelt.com/text', {
            'phone': '6263213319',
            'message': 'Remaining Quota is less than 10. Go to textbelt.com and Refill it',
            'key': TEXT_API , })




while True:
    time.sleep(20)
    checkQuotaCount()
    ethData = checkPrice();
    ethamount = float( ethData['amount'])
    print('Current Amount'+str(ethamount)+ ', Desired Amount '+str( DesireAmount))
    message_high = "ETH-USD value is supress "+ str(DesireAmount)+ '$.'
    message_low = "ETH-USD value is drop to "+ str(DesireAmount)+'$.'

    status = ""
    if ethamount > DesireAmount:
        status=sendNoti(message_high,'6263213319')
        print(status)
        time.sleep(120)
    if ethamount <= DesireAmount_LOW:
        status=sendNoti(message_low,'6263213319')
        time.sleep(120)
        print(status.json())




