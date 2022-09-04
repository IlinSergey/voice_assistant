import bs4, requests
import speech_recognition as sr
import pyttsx3
import random
import datetime
import pywhatkit
import pyowm
import config


engine = pyttsx3.init()
voices = engine.getProperty('voices')      # Получаем список имеющихся голосов
engine.setProperty('voice', voices[0].id)  # Выбираем голос для озвучки

listener = sr.Recognizer()

flag = True

with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source) # Слушаем в течении 1 секунды для получения фонового шума

def talk(text):         # Функция talk для озвучки текста
    print(text)
    engine.say(text)
    engine.runAndWait() # Запускаем озвучку текста

def lissen():
    with sr.Microphone() as source:  # Создаем переменную для микрофона source
        print('Слушаем...')  # Выводим сообщение о готовности слушать
        voice = listener.listen(source)  # Слушаем звук с микрофона в переменную voice
        command = listener.recognize_google(voice, language='ru-RU')  # Распознаем через google голосовую команду
        command = command.lower()
    return command

def take_command():      # Функция для получения текстовых команд
    try:
        command = lissen()
        for name in config.names:
            if name in command:
                talk('Слушаю...')  # Выводим сообщение о готовности слушать
                command = lissen()
                print(f'Вы сказали:  {command}')
                return command
    except:
        pass
    return ''


def get_anekdot():
    joke_text = requests.get('https://www.anekdot.ru/random/anekdot/')  # Получаем текст HTML страницы сайта с анекдотами
    soup = bs4.BeautifulSoup(joke_text.text, 'html.parser')      # Инициализируем HTML парсер
    jokes = soup.select('div.text')                    # Парсим страницу по тегу
    index = random.randrange(len(jokes))               # Выбераем индекс случайного анекдота на странице
    joke_text = jokes[index].getText().strip()         # Получаем текст анекдота
    return joke_text

def tell_joke():
    talk('Внимание, Анектод!')
    joke = get_anekdot()
    talk(joke)

def tell_date():
    day = int(datetime.datetime.now().strftime('%d'))
    month = int(datetime.datetime.now().strftime('%m'))
    talk(f'Сегодня {day} {config.months[month - 1]}')

def tell_time():
    time = datetime.datetime.now().strftime('%I:%M')
    talk(f'Сейчас {time}')

def play_youtube(video):           # Подключаем модуль для работы с YouTube
    talk(f'Включаю {video}...')
    pywhatkit.playonyt(video)      # Запускаем на YouTube первое видео по запросу

def search_google(request):
    talk(f'Ищу {request}')
    pywhatkit.search(request)

def tell_weather():
    own = pyowm.OWM(config.weather_token)
    mgr = own.weather_manager()
    observation = mgr.weather_at_place('Vyborg')
    weather = observation.weather

    temp = round(weather.temperature('celsius')['temp'])
    talk(f'На улице {temp} градусов')

def run():
    command = take_command()
    if 'привет' in command:
        talk('Привет, хозяин!')
        print('Привет, хозяин!')
    elif 'анекдот' in command:
        tell_joke()
    elif 'время' in command or 'час' in command:
        tell_time()
    elif 'число' in command or 'дата' in command:
        tell_date()
    elif 'включи' in command:
        video = command.replace('включи','') # Убираем слово 'включи' из команды
        play_youtube(video)
    elif 'найди' in command:
        request = command.replace('найди','')
        search_google(request)
    elif 'погода' in command:
        tell_weather()
    elif 'пока' in command:
        talk('До свидания!')
        global flag
        flag = False


while flag:
    run()
