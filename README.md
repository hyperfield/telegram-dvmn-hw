# Dvmn homework bot

A simple Python program for long-polling Devman's API to check for submitted homework(s) status(es) and update accordingly via a Telegram bot.

## Installation

Python 3 should already be installed. If not, then please do so. You also need the [Telegram](https://telegram.org) client to receive updates.
And you need an account at [Dvmn](https://dvmn.org/).

Now create a Python virtual environment:

    python3 -m venv .venv

Activate the environment, e.g.:

    source .venv/bin/activate

Install the required libraries:

    pip install -r requirements.txt

Create a Telegram account and then find **@BotFather** and send it the following messages:

    /start
    /newbot

Follow prompts. Next, send

    /start

to your own newly created bot as well, and also to **@userinfobot** to get your *chat id*.

Also get your API key from **Dvmn**. Now you need to set up the program by creating a file named `.env` in the program directory.

> Example of `.env`:

    DVMN_API_TOKEN = "Token 13c2c7d67efa75c44349f314e33aa72e52306a48"
    TELEGRAM_TOKEN = "1963334630:AAB28DCf15DqJE6VCROlwB5dE14TLkuadyl"
    TELEGRAM_CHAT_ID = "135144583"


## Launching the program

If you are in Linux and make the file executable by

    chmod +x main.py

then you can also launch directly, e.g.:

    ./main.py

Keep the program open and do your **Dvmn** work now, submit and receive the status updates in **Telegram** accordingly. You may also want to add the file in your boot autoload settings.