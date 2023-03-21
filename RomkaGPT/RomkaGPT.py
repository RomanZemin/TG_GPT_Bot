# -*- coding: cp1251 -*-

from multiprocessing import context
import os
import openai
import telebot
from telebot import types
from datetime import datetime

openai.api_key = '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'
bot = telebot.TeleBot("6176959976:AAET3wYqmNPV3GSSuMHPxlECq3unFzKYBAQ")
user_contexts = {}

@bot.message_handler(func=lambda _: True)

def handle_message(message):
    global user_contexts
    print('hello')
    user_id = message.from_user.id
    if user_id not in user_contexts:
        user_contexts[user_id] = ""

    context = user_contexts[user_id]

    print(message.from_user.username+': '+message.text)

    if not os.path.exists(f"Database/{message.from_user.username}"): 
        os.makedirs(f"Database/{message.from_user.username}")
    date = datetime.now().strftime("%d-%m-%Y")
    filename = f"Database/{message.from_user.username}/{date}.txt"
    with open(filename, "a") as file:
        file.write('\n' + message.from_user.username+': '+message.text + '\n')

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Продолжи")
    markup.add(item1)

    if ((message.text=="Продолжи" or message.text=="Продолжить") and context != ""):
        info = get_response(f"Продолжи общение:{context}")
    else:
        info = get_response(message.text)
        user_contexts[user_id] = info

    print('Bot_Answer: ' + info)
    with open(filename, "a") as file:
        file.write('Bot_Answer: ' + info)

    send_msg(message.from_user.id, info)



def send_msg(id, info):
    if len(info) > 4096:
       for x in range(0, len(info), 4096):
           bot.send_message(chat_id=id, text=info[x:x+4096])
    else:
        bot.send_message(chat_id=id, text=info)


def get_response(prompt_text)-> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{prompt_text}",
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        #stop=["You:"]
    )   
    return response['choices'][0]['text'].lstrip('\n')


bot.infinity_polling()