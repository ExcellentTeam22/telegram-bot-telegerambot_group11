import math

from flask import Flask, Response, request
import requests

app = Flask(__name__)

TOKEN = '5694196769:AAGwRmFwMp89-0ehKqjXwJMVv9-THuuq_ME'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://23bb-46-31-101-77.eu.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/')
def p(): return "Server is running"


def is_prime(n: int) -> int:
    for i in range(2, n):
        if (n%i) == 0:
            return False
    return True


def is_factorial(n: int) -> int:
    i = 1
    while True:
        if n % i == 0:
            n //= i
        else:
            break

        i += 1;
    if n == 1:
        return True
    else:
        return False


def is_palindrome(s: int) -> int:
    return s == s[::-1]


def keywithmaxval(counter_command:dict) -> str:
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    v = list(counter_command.values())
    k = list(counter_command.keys())
    return k[v.index(max(v))]


@app.route('/message', methods=["POST"])
def handle_message():
    counter_command = {'factorial': 0, 'palindrome': 0, 'sqrt': 0, 'prime': 0}
    chat = request.get_json()
    chat_id = chat['message']['chat']['id']
    text = chat['message']['text']
    print(chat)

    if text == 'hello':
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                           .format(TOKEN, chat_id, "how are you?"))
    if text.startswith("/prime"):
        split_text = text.split()
        if is_prime(int(text.split()[1])):
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                                   .format(TOKEN, chat_id, "is prime"))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                                   .format(TOKEN, chat_id, "not prime"))
        counter_command['prime'] += 1

    if text.startswith("/factorial"):
        split_text = text.split()
        print(split_text)
        if is_factorial(int(text.split()[1])):
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "True"))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "False"))
        counter_command['factorial'] += 1

    if text.startswith("/palindrome"):
        split_text = text.split()
        print(split_text)
        if is_palindrome(text.split()[1]):
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "True"))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "False"))
        counter_command['factorial'] += 1

    if text.startswith("/sqrt"):
        split_text = text.split()
        if math.isqrt(text.split()[1]):
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "True"))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "False"))
        counter_command['sqrt'] += 1

    if text.startswith("/popular"):
        maximum = max(counter_command.values())
        result = filter(lambda x: x[1] == maximum, counter_command.items())

        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id,))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)