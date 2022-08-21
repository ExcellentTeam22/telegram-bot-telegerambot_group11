from flask import Flask, json
from flask import request
from flask import Response
import requests

app = Flask(__name__)

TOKEN = '5694196769:AAGwRmFwMp89-0ehKqjXwJMVv9-THuuq_ME'
TELEGRAM_INIT_WEBHOOK_URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://523e-82-80-173-170.eu.ngrok.io'
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


def tel_parse_message(message):
    print("message-->", message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("txt-->", txt)

        return chat_id, txt
    except:
        print("NO text found-->>")


def tel_send_poll(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPoll'
    payload = {
        'chat_id': chat_id,
        "question": "In which direction does the sun rise?",
        "options": json.dumps(["North", "South", "East", "West"]),
        "is_anonymous": False,
        "type": "quiz",
        "correct_option_id": 2
    }

    r = requests.post(url, json=payload)

    return r


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)

    return r


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = tel_parse_message(msg)
            if txt == "hi":
                tel_send_message(chat_id, "Hello, world!")
                tel_send_poll(chat_id)
            elif txt == "poll":
                tel_send_poll(chat_id)

            else:
                tel_send_message(chat_id, 'from webhook')
        except:
            print("from index-->")

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    app.run(port=5002)
