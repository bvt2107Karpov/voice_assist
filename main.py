
# Голосовой ассистент КЕША 1.0 BETA
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import random
import webbrowser
import pyautogui
import mouse
import keyboard
from random import randint
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# настройки
opts = {
    "alias": ('кеша'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты', 'шутка', 'прикол'),
        "startWatch": ('запусти секундомер', 'включи секундомер', 'засеки время'),
        "stopWatch": ('выключи секундомер', 'останови секундомер', 'останови секундомер', 'стоп', 'stop'),
        "thanks": (
        'ты молодец', 'умница', 'молодец', 'ты умница', 'ты умничка', 'умница', 'гений', 'ты гений', 'браво',
        'отлично', 'отличная работа', 'хорошая работа'),
        "vk": ('вк', 'вконтакте'),
        "yandex": ("браузер"),
        'mute': ('убери звук', 'выключи звук'),
        'unmute': ('включи звук', 'верни звук'),
        'volume_up': ('повысь громкость', 'прибавь громкость'),
        'volume_down': ('понизь громкость', 'убавь громкость'),
        'youtube': ('ютуб', 'ютаб', 'ютабчик', 'youtube'),
        'browse': ('загугли'),
        'ali': ('али', 'ali', 'aliexpress', 'алиэспресс'),
        'wiki': ('вики', 'wiki'),
        'mail': ('почта', 'mail', 'яндекс почта', 'email'),
        'wb': ('wildberries', 'wb', 'вб')
    }
}


jokes = [
    'Блин! - сказал слон, наступив на колобка.',
    'Почему зекам нельзя уступать место в общественном транспорте? Свое уже отсидели',
    'На приеме у врача. Доктор, а я жить буду? Будешь, но не захочешь.',
    'Едут в лифте два японца, грузин, армянин и азербайджанец. Тут один японец говорит другому: «Эти русские все на одно лицо».',
    'Кто изобpел полупpоводники? Не знаю, но пеpвым полупpоводником был Иван Сусанин.'
]




end_jokes = [
    'Надеюсь вам было смешно ха ха ха',
    'Вам понравилось?',
    'Ха Ха Ха Ха Ха',
    'Вам смешно? И мне не смешно',
    'Посмейтесь пожалуйста'
]


wait = [
    'Будет сделано',
    'Секундочку',
    'Будет исполнено',
    'Практически закончил',
    'Почти сделано',
    'Конечно',
    'Исполняю',
    'Готово'
]


gratitude = [
    'Спасибо',
    'Благодарю вас',
    'Всегда пожалуйста',
    'Пустяки',
    'Вы тоже молодец!'
]
# функции

def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def request1(recognizer, audio):
    try:
        voice_1 = recognizer.recognize_google(audio, language="ru-RU").lower()
        return voice_1
    
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        speak(waited)
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'stupid1':
        speak(waited)
        start_anekdot()


    elif cmd == 'startWatch':
        startWatch()

    elif cmd == 'stopWatch':
        stopWatch()
    
    elif cmd == 'mute':
        volume.SetMasterVolumeLevelScalar(0, None)
    
    elif cmd == 'unmute':
        volume.SetMasterVolumeLevelScalar(1, None)

    elif cmd == 'volume_up':
        volume.SetMasterVolumeLevelScalar(volume.GetMasterVolumeLevelScalar() + 0.1, None)

    elif cmd == 'volume_down':
        volume.SetMasterVolumeLevelScalar(volume.GetMasterVolumeLevelScalar() - 0.1, None)

    elif cmd == 'thanks':
        thank = random.choice(gratitude)
        speak(thank)

    elif cmd == "vk":
        speak(waited)
        webbrowser.open('https://vk.com', new=2)

    elif cmd == "browse":
        speak(waited)
        req = request1(r, audio)[13:]
        webbrowser.open('https://yandex.ru/search/?clid=2456107&text=яндекс&l10n=ru&lr=213', new=2)
        pyautogui.moveTo(411, 50)
        mouse.click('left')
        keyboard.write(req)
        keyboard.send('enter')

    
    elif cmd == "yandex":
        speak(waited)
        webbrowser.open('https://yandex.ru/search/?clid=2456107&text=яндекс&l10n=ru&lr=213', new=2)

    elif cmd == 'youtube':
        speak(waited)
        webbrowser.open('https://www.youtube.com', new=2)

    elif cmd == 'ali':
        speak(waited)
        webbrowser.open('https://aliexpress.ru', new=2)

    elif cmd == 'wiki':
        speak(waited)
        webbrowser.open('https://ru.wikipedia.org', new=2)

    elif cmd == 'wb':
        speak(waited)
        webbrowser.open('https://www.wildberries.ru', new=2)

    elif cmd == 'mail':
        speak(waited)
        webbrowser.open('https://mail.yandex.ru/?uid=1053847637#inbox', new=2)

    else:
        print('Команда не распознана, повторите!')


waited = random.choice(wait)


anekdot = True


def start_anekdot():
    global anekdot
    while anekdot:
        speak("Я знаю пару анекдотов")
        speak('Только сильно не смейтесь.. ха ха ха')
        anekdot = False
    joke = random.choice(jokes)
    speak(joke)
    end_joke = random.choice(end_jokes)
    speak(end_joke)


isRunning = False
startTime = 0

def startWatch():
    global isRunning, startTime
    if isRunning:
        speak("Секундомер уже запущен")
    else:
        speak("Секундомер запущен")
        startTime = time.time()
        isRunning = True




def stopWatch():
    global isRunning, startTime
    if isRunning:
        Time = time.time() - startTime
        speak(f"Прошло {round(Time // 3600)} часов {round(Time // 60)} минут {round(Time % 60, 2)} секунд")
        isRunning = False
    else:
        speak("Секундомер не запущен")


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=4)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()


ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
speak_engine.setProperty('voice', ru_voice_id)
speak_engine.setProperty("rate", 250)
speak_engine.setProperty("volume", 0.7)

NOW = datetime.datetime.now()

if NOW.hour >= 3 and NOW.hour < 12:
    speak("Доброе утро!")
    speak("Я вас слушаю")
elif NOW.hour >= 12 and NOW.hour < 18:
    speak("Добрый день!")
    speak("Я вас слушаю")
elif NOW.hour >= 18 and NOW.hour < 3:
    speak("Добрый вечер!")
    speak("Я вас слушаю")
else:
    speak("Доброй ночи!")
    speak("Я вас слушаю")

while True:
    with m as source:
        audio = r.listen(source)
    callback(r, audio)