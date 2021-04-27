from coinbase.wallet.client import Client
from dotenv import load_dotenv
import sched, time
import datetime
import requests
import json

load_dotenv()


DesireAmount = 2400
DesireAmount_LOW = 2100
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
      'key': TEXT_API+'_test',})
    return req.json()


def aniversaryDate():
    now = datetime.datetime.now()
    aniversary = '{"vday":14, "vmonth":2, "bday":6, "bmonth":8}'
    aniversary = json.loads(aniversary)
    if not isAnni:
        if now.day == aniversary['vday'] and now.month == aniversary['vmonth']:
            year = now.year - 2018
            sendNoti("宝贝！祝你第"+str(year)+"年的情人节快乐呀！爱你么么哒", '6265544721')
        if now.day == aniversary['bday'] and now.month == aniversary['bmonth']:
            year = now.year - 1993
            sendNoti("宝贝！祝你第"+str(year)+"岁的生日快乐！爱你么么哒", '6265544721')



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
    aniversaryDate()
    ethData = checkPrice();
    ethamount = float( ethData['amount'])
    message_high = "ETH-USD value is supress "+ str(DesireAmount)+ '$.'
    message_low = "ETH-USD value is drop to "+ str(DesireAmount)+'$.'

    status = ""
    if not isNotify:
        if ethamount > DesireAmount:
            status=sendNoti(message_high,'6263213319')
            time.sleep(120)
        if ethamount <= DesireAmount_LOW:
            status=sendNoti(message_low,'6263213319')
            time.sleep(120)




