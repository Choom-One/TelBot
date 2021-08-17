import random
import nltk
import json
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split


with open('/home/artiom/Рабочий стол/BOT_CONFIG.json', 'r') as f:
    BOT_CONFIG = json.load(f)

# BOT_CONFIG = {
#     'intents': {
#         'hello': {
#             'examples': ['Привет!', 'Хай', 'Хэллоу'],
#             'responces': ['Здравствуйте!', 'Приветствую', 'Доброго времени суток']
#         },
#         'bye': {
#             'examples': ['Пока', 'Увидимся', 'До свиданья'],
#             'responces': ['Приходите еще', 'Рад был познакомиться', 'Покеда']
#         },
#         'howdoyoudo': {
#             'examples': ['Как дела?', 'Как поживаешь?', 'Чем живешь?'],
#             'responces': ['Неплохо', 'Не жалуюсь', 'А тебе какое дело?']
#         },
#         'whoareyou': {
#             'examples': ['Кто ты?', 'Что ты делаешь?', 'Что умеешь?'],
#             'responce': ['Я просто бот', 'Я еще в разработке', 'Мой создатель меня доделывает']
#         },
#         'god': {
#             'examples': ['Кто тебя сделал?', 'Кто твой создатель?'],
#             'responce': ['Это информация засекречена)', 'Я не могу вам это сказать', 'Если я скажу, то мне придется\n'
#                                                                                      'вас убить']
#         }
#     }
# }


def clean(text):
    output_text = ''
    for char in text.lower():
        if char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            output_text = output_text + char
    return output_text


def get_intent(text):
    for intent in BOT_CONFIG['intents'].keys():
        for example in BOT_CONFIG['intents'][intent]['examples']:
            text1 = clean(example)
            text2 = clean(text)
            if len(text1) != 0 and len(text2) != 0:
                if nltk.edit_distance(text1, text2) / max(len(text1), len(text2)) < 0.4:
                    return intent
    return 'Не удалось определить интент'


def get_intent_by_model(text):
    return clf.predict(vectorizer.transform([text]))[0]


def bot(input_text):
    intent = get_intent_by_model(input_text)
    return random.choice(BOT_CONFIG['intents'][intent]['responces'])


x = []
y = []

for intent in BOT_CONFIG['intents'].keys():
    try:
        if intent != 'other':
            for example in BOT_CONFIG['intents'][intent]['examples']:
                x.append(example)
                y.append(intent)
    except:
        print(BOT_CONFIG['intents'][intent])


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42)

vectorizer = CountVectorizer(ngram_range=(2, 4), analyzer='char')
x_train_vectorized = vectorizer.fit_transform(x_train)
x_test_vectorized = vectorizer.transform(x_test)
len(vectorizer.get_feature_names())


clf = LogisticRegression().fit(x_train_vectorized, y_train)


def get_intent_by_model(text):
    return clf.predict(vectorizer.transform([text]))[0]


def bot(input_text):
    intent = get_intent_by_model(input_text)
    return random.choice(BOT_CONFIG['intents'][intent]['responces'])


# clf.score(x_train_vectorized, y_train)
# clf.score(x_test_vectorized, y_test)


input_text = ''
while input_text != 'Завершить работу':
    input_text = input()
    print(bot(input_text))
