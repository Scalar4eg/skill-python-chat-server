from flask import Flask, request, abort, render_template

app = Flask(__name__)


@app.route("/")
def index_page():
    return "HELLO"


import time
from datetime import datetime

time_17_00 = datetime.fromisoformat("2021-08-02 17:00:00").timestamp()
time_17_30 = datetime.fromisoformat("2021-08-02 17:30:00").timestamp()

test_message1 = {
    "text": "Hello, Vass",
    "name": "Igort",
    "time": time_17_00,
}

test_message2 = {
    "text": "Hello my dear friend",
    "name": "Mike",
    "time": time_17_00,
}
# key + value, ключ + значение

# Database - база данных с сообщениями чата
# Список сообщений
db = [
    test_message1,
    test_message2
]

@app.route("/form")
def form():
    return render_template("form.html")

# POST - как правило означает изменение данных
# GET - запрос, который ничего не меняет

@app.route("/sendMessage")
def chat():
    name = request.args["name"]
    text = request.args["text"]

    name_len = len(name)  # длина имени
    text_len = len(text)  # длина текста
    
    if name_len > 100 or name_len < 3:
        return "ERROR"  # Невалидный запрос

    if text_len < 1 or text_len > 3000:
        return "ERROR"

    message = {
        "name": name,
        "text": text,
        "time": time.time()  # таймстемп
    }
    db.append(message)  # Добавляем новое сообщение в список
    return "OK"


# Распечатать все сообщения
def print_messages(messages):
    for message in messages:
        name = message["name"]
        text = message["text"]
        message_time = message["time"]
        time_pretty = datetime.fromtimestamp(message_time)

        print(f"[{name}] / {time_pretty}")
        print(text)
        print()


# print_messages(db)

# http://127.0.0.1:5000/messages?after_timestamp=19191
# Собирать все сообщения, после опредленного времени
@app.route("/messages")
def get_messages():
    after_timestamp = float(request.args["after_timestamp"])
    result = []  # Все сообщения, отправленные после after_timestamp
    for message in db:
        if message["time"] > after_timestamp:
            result.append(message)

    return {"messages": result}


# https://docs.python.org/3/

app.run()
