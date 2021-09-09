#!/usr/bin/env python3

from dotenv import load_dotenv
from os import getenv
import logging
import requests
import telegram
import time
from urllib.parse import urljoin


logger = logging.getLogger("Telegram Logger")


def send_telegram_message(telegram_bot, telegram_chat_id, work_title,
                          lesson_url, message_is_negative):
    neg_message = "К сожалению, в работе нашлись ошибки."
    pos_message = \
        "Преподавателю всё понравилось, можно приступать к следующему уроку!"
    success_fail_message = neg_message if message_is_negative else pos_message
    telegram_message = f"""У вас проверили работу "{work_title}".

    {success_fail_message}

    {lesson_url}"""

    telegram_bot.send_message(text=telegram_message, chat_id=telegram_chat_id)


def get_homeworks_status_updates(telegram_bot, telegram_chat_id, headers,
                                 no_connection_count, timestamp=None):
    api_url = "https://dvmn.org/api/long_polling/"
    try:
        params = {"timestamp": timestamp}
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        no_connection_count = 0
        response_content = response.json()
        if response_content["status"] == "found":
            timestamp = response_content['last_attempt_timestamp']
            last_attempt = response_content['new_attempts'][0]
            work_title = last_attempt['lesson_title']
            relative_lesson_url = last_attempt['lesson_url']
            lesson_url = urljoin("https://dvmn.org",
                                 relative_lesson_url)
            message_is_negative = last_attempt['is_negative']
            send_telegram_message(telegram_bot, telegram_chat_id, work_title,
                                  lesson_url, message_is_negative)
        else:
            timestamp = response_content['timestamp_to_request']

        return timestamp
    except requests.exceptions.ReadTimeout:
        return None
    except ConnectionError:
        no_connection_count += 1
        logger.warning("The Dvnn homwork bot has no internet connection")
        if no_connection_count > 5:
            time.sleep(15)
        elif no_connection_count > 10:
            time.sleep(30)
        return None


class LogsHandler(logging.Handler):
    def __init__(self, telegram_chat_id, telegram_token):
        super().__init__()
        self.chat_id = telegram_chat_id
        self.telegram_bot = telegram.Bot(token=telegram_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.telegram_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    telegram_token = getenv("TELEGRAM_TOKEN")
    telegram_chat_id = getenv("TELEGRAM_CHAT_ID")
    telegram_bot = telegram.Bot(token=telegram_token)
    logging.basicConfig(level=logging.INFO,
                        format="%(process)d %(levelname)s %(message)s")
    logs_handler = LogsHandler(telegram_chat_id, telegram_token)
    logger.addHandler(logs_handler)
    dvmn_token = getenv("DVMN_API_TOKEN")
    headers = {"Authorization": dvmn_token}
    timestamp = None
    no_connection_count = 0
    logger.info("The Dvmn homework bot has started")
    while True:
        timestamp = get_homeworks_status_updates(telegram_bot,
                                                 telegram_chat_id,
                                                 headers, no_connection_count,
                                                 timestamp)


if __name__ == '__main__':
    main()
