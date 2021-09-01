import random
import json
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


#this is my path to the config file
with open('/home/artiom/Рабочий стол/BOT_CONFIG.json', 'r') as f:
    BOT_CONFIG = json.load(f)

x = []
y = []

for intent in BOT_CONFIG['intents'].keys():
    try:
        if intent != 'other':
            for example in BOT_CONFIG['intents'][intent]['examples']:
                x.append(example)
                y.append(intent)
    except:
        pass


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42)


vectorizer = CountVectorizer(ngram_range=(2, 4), analyzer='char')
x_train_vectorized = vectorizer.fit_transform(x_train)
x_test_vectorized = vectorizer.transform(x_test)
len(vectorizer.get_feature_names())

print('обучаюсь, это займет немного времени')

clf = LogisticRegression().fit(x_train_vectorized, y_train)

clf.score(x_train_vectorized, y_train)
# 0.8422174840085288 LogReg_base

clf.score(x_test_vectorized, y_test)

print(clf.predict(vectorizer.transform(['откуда ты?'])))

print('я обучился и готов работать')


def get_intent_by_model(text):
    return clf.predict(vectorizer.transform([text]))[0]


# Call_Bot

def bot(input_text):
    intent = get_intent_by_model(input_text)
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(bot(update.message.text))


def main() -> None:
    print('телеграм бот запущен')
    """Start the bot."""
    # Create the Updater and pass it your bot's token.

    updater = Updater("Your token")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
