import math
import os

from flask import Flask, Response, request
import requests
import http.client
from urllib.request import urlretrieve
import webbrowser


app = Flask(__name__)

TOKEN = '5767542973:AAFFdd3BBNJodwNUwJGKJ_AyuvI_mTis8f8'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://4c72-93-173-125-118.eu.ngrok.io/sendAudio'.format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)
querystring = {"key": "834f306bed0e4f2da7bb335b01b0bde6"}#key of record API


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/')
def p(): return "Server is running"


@app.route('/sendAudio', methods=["POST"])
def handle_message():
    chat = request.get_json()
    chat_id = chat['message']['chat']['id']
    text = chat['message']['text']
    print(chat)

    filename = 'speech.wav'

    url = "https://voicerss-text-to-speech.p.rapidapi.com/"

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "5991e19cd9msh6ba7b3e15ad8bafp162e99jsn85520f9f925c",
        "X-RapidAPI-Host": "voicerss-text-to-speech.p.rapidapi.com"
    }

    urlretrieve("http://api.voicerss.org/?key=834f306bed0e4f2da7bb335b01b0bde6&hl=en-us&c=MP3&f=16khz_16bit_stereo&src=Hello,world!",filename)

    os.startfile(filename)  # play the file using default application
    with open('speech.wav', 'rb') as audio:
        payload = {
            'chat_id': chat_id,
            'title': 'file.wav',
            'parse_mode': 'HTML'
        }

        files = {
            'audio' : open('speech.wav','rb')
        }
        resp = requests.post(
            "https://api.telegram.org/bot{token}/sendAudio".format(token=TOKEN),
            data=payload,files=files)
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
