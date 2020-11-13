#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
from datetime import datetime
import random
import time
import requests
import json

# Токены:
token = 'Токен ВК здесь'

vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def search(sea):
    send_message(vk_session, 'user_id', event.user_id, message='🎓 Пожалуйста подождите, я ищу информацию в сети интернет 🌎')

    url = ("https://google-search3.p.rapidapi.com/api/v1/search/q=" + sea)

    headers = {
        'x-rapidapi-key': "Токен от Google-Search",
        'x-rapidapi-host': "google-search3.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    js = response.json()
    title1 = []
    description1 = []
    link1 = []
    title1 = js.get('results')[0].get('title')
    description1 = js.get('results')[0].get('description')
    link1 = js.get('results')[0].get('link')

    title2 = []
    description2 = []
    link2 = []
    title2 = js.get('results')[1].get('title')
    description2 = js.get('results')[1].get('description')
    link2 = js.get('results')[1].get('link')

    title3 = []
    description3 = []
    link3 = []
    title3 = js.get('results')[2].get('title')
    description3 = js.get('results')[2].get('description')
    link3 = js.get('results')[2].get('link')

    # print(f'Название: {title}\nОписание:\n{description}')

    send_message(vk_session, 'user_id', event.user_id, message=f'🔥 Название: \n{title1}\nОписание:\n{description1}\n'\
                                                               f'🔗 ссылка на источник: {link1}\n{"-" * 30}')
    send_message(vk_session, 'user_id', event.user_id, message=f'🔥 Название: \n{title2}\nОписание:\n{description2}\n' \
                                                               f'🔗 ссылка на источник: {link2}\n{"-" * 30}')
    send_message(vk_session, 'user_id', event.user_id, message=f'🔥 Название: \n{title3}\nОписание:\n{description3}\n' \
                                                               f'🔗 ссылка на источник: {link3}')


def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)

    if response == 'меню':
        keyboard.add_button('Инструкция', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line() # Разделитель
        keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line() # Разделитель
        keyboard.add_button('Закрыть', color=VkKeyboardColor.NEGATIVE)

    elif response == 'начать':
        keyboard.add_button('Разработчик', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Меню', color=VkKeyboardColor.POSITIVE)

    elif response == 'привет':
        keyboard.add_button('Меню', color=VkKeyboardColor.POSITIVE)

    elif response == 'поиск':
        keyboard.add_button('поиск', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line() # Разделитель
        keyboard.add_button('Меню', color=VkKeyboardColor.POSITIVE)

    elif response == 'закрыть':
        print('закрываем клаву')
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard


def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), "attachment": attachment, 'keyboard': keyboard})

rule_list = '''
👋🏻 Привет, данный бот поможет тебе найти любой контент со всего мира
Просто введи на клавиатуре, или воспользуйся кнопками активности, чтобы взаимодействовать с ботом.
Если пропала клавиатура, напиши мне "Привет", тогда все снова заработает
'''

waiting_place_users = set()


def input_search():
    send_message(vk_session, 'user_id', event.user_id, message="Что вы хотите найти?",
                 keyboard=keyboard)
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        waiting_place_users.add(event.user_id)

# Загрузка картинки в ВК
def upload_photo():
    uploader = vk_api.upload.VkUpload(vk_session)
    img = uploader.photo_messages("img/pony.png") # Место откуда загружать фото
    media_id = str(img[0]['id'])
    owner_id = str(img[0]['owner_id'])
    print("photo" + owner_id + "_" + media_id)
    print(img)

# Раскомментируй вызов функции что ниже, чтобы загрузить картинку
# upload_photo()

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
            print('Текст сообщения: ' + str(event.text))
            print(f"Пользовательский ID: {event.user_id}")
            print('-'*50)
            response = event.text.lower()
            keyboard = create_keyboard(response)

            if event.from_user and not event.from_me:
                if event.type == VkEventType.MESSAGE_NEW and event.user_id in waiting_place_users and event.text:
                    waiting_place_users.remove(event.user_id)
                    try:
                        search(event.text)
                    except:
                        if event.text.lower() == 'меню' or event.text.lower() == 'поиск':
                            break;
                        else:
                            send_message(vk_session, 'user_id', event.user_id, message="Город не найден, проверьте правильность ввода и повторите попытку")

                elif response == "поиск":
                    input_search()
                elif response == "привет":
                    send_message(vk_session, 'user_id', event.user_id, message='И тебе привет 👋🏻\nЧтобы воспользоваться моим функционалом откройте меню',keyboard=keyboard)
                elif response == "меню":
                    send_message(vk_session, 'user_id', event.user_id, message='Хе-хей, ты решил зайти в меню?\nЧем я могу тебе помочь?',keyboard=keyboard)
                elif response== 'начать':
                    send_message(vk_session, 'user_id', event.user_id, message=f'{rule_list}',keyboard=keyboard)
                elif response == 'инструкция':
                    send_message(vk_session, 'user_id', event.user_id, message=f'{rule_list}')
                elif response=='разработчик':
                    send_message(vk_session, 'user_id', event.user_id, message='Мой разработчик пока-что студент, зовут его @id186019886 (Сергей)')
                elif response=='закрыть':
                    send_message(vk_session, 'user_id', event.user_id, message='Меню закрыто, чтобы вернуть кнопки, напиши "Меню"',keyboard=keyboard)

                else:
                    send_message(vk_session, 'user_id', event.user_id, message='Неизвестная команда, или сообщение, человек я тебя не понимаю, так как понимают тебя другие люди =(', attachment="photo-199806584_457239036")