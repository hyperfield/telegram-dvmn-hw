#!/usr/bin/env python3

from dotenv import load_dotenv
from os import getenv
import requests
import telegram
from urllib.parse import urljoin


def send_telegram_message(telegram_bot, telegram_chat_id, work_title,
                          lesson_url, message_is_negative):
    neg_message = "К сожалению, в работе нашлись ошибки."
    pos_message = \
        "Преподавателю всё понравилось, можно приступать к следующему уроку!"
    success_fail_message = pos_message if message_is_negative else neg_message
    telegram_message = f"""У вас проверили работу "{work_title}".\n
        {success_fail_message}\n\n{lesson_url}"""
    telegram_bot.send_message(text=telegram_message, chat_id=telegram_chat_id)


def get_homeworks_status_updates(telegram_bot, telegram_chat_id, headers,
                                 timestamp=None):
    api_url = "https://dvmn.org/api/long_polling/"
    try:
        params = {"timestamp": timestamp} if timestamp else None
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        response_content = response.json()
        if response_content["status"] == "found":
            timestamp = response_content['last_attempt_timestamp']
            work_title = response_content['new_attempts'][0]['lesson_title']
            lesson_url = \
                urljoin("https://dvmn.org",
                        response_content['new_attempts'][0]['lesson_url'])
            message_is_negative = \
                response_content['new_attempts'][0]['is_negative']
            send_telegram_message(telegram_bot, telegram_chat_id, work_title,
                                  lesson_url, message_is_negative)
        else:
            timestamp = response_content['timestamp_to_request']

        return timestamp
    except requests.exceptions.ReadTimeout:
        return None
    except ConnectionError:
        print("No internet connection")
        return None


def main():
    load_dotenv()
    telegram_token = getenv("TELEGRAM_TOKEN")
    telegram_bot = telegram.Bot(token=telegram_token)
    telegram_chat_id = getenv("TELEGRAM_CHAT_ID")
    dvmn_token = getenv("DVMN_API_TOKEN")
    headers = {"Authorization": dvmn_token}

    timestamp = None
    while True:
        timestamp = get_homeworks_status_updates(telegram_bot,
                                                 telegram_chat_id,
                                                 headers, timestamp)


if __name__ == '__main__':
    main()
