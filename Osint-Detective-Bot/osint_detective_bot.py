import telebot
import requests
from files import sites

TOKEN = "8301891473:AAGs1DQQb5opIX-tM1yXBriG_pVVnIm12Pk"
bot = telebot.TeleBot(TOKEN)

def split_message(text, max_length=4096):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.reply_to(message, text="🚀 Добро пожаловать в OSINT Detective Bot!\n\n"
                               "Я ваш AI-помощник по поиску общедоступных данных.\n"
                               "Используйте следующие команды, чтобы начать:\n\n"
                               "🔎 Поисковые команды\n"
                               "/username [никнейм] – Найти профили в социальных сетях, на форумах и в играх.\n\n"
                               "📊 Расширенные инструменты\n"
                               "/report – Сгенерировать TXT отчет о ваших находках.\n\n"
                               "⚙️ Утилиты"
                               "/help – Показать это меню.\n"
                               "/legal – Правила конфиденциальности и этичного использования.\n\n"
                               "📌 Пример:\n"
                               "/username john_doe\n\n"
                               "Я соблюдаю законы о конфиденциальности — используйте этично!\n"
                               "Начнем расследование\n")

@bot.message_handler(commands=['username'])
def find_username(message):
    mes = message.text.split()
    if len(mes) < 2:
        bot.reply_to(message, "Ошибка ввода! Пожалуйста, введите полную команду!\n\n"
                              "Пример команды:\n"
                              "/username <имя пользователя>")
    else:
        bot.reply_to(message, f"Бот начал поиск, ожидайте ответ! (среднее время ожидания ответа ")

        nickname = mes[1]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        i = 0
        lst = []
        txt_file = "report.txt"

        for key, value in sites.items():
            i += 1
            try:
                site = f"{value}{nickname}"
                response = requests.get(site, headers=headers, timeout=10)
                if response.status_code == 200:
                    result = f"{i}. {key} - Пользователь найден\nСсылка на профиль:\n{site}\n"
                    lst.append(result)
                    print(result)
                else:
                    result = f"{i}. {key} - Пользователь не найден\n"
                    lst.append(result)
            except requests.exceptions.ConnectionError:
                result = f"{i}. {key}: Ошибка соединения - сайт заблокирован в вашей стране\n"
                lst.append(result)
                print(result)
            except requests.exceptions.ReadTimeout:
                result = f"{i}. {key}: Ошибка задержки - слишком долгое время ожидания\n"
                lst.append(result)
                print(result)
            except requests.exceptions.InvalidURL:
                result = f"{i}. {key}: Ошибка ссылки - url-адрес некорректный\n"
                lst.append(result)
                print(result)

        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("Ответ получен!\nРезультаты:\n\n")
            f.write("\n\n".join(lst))

        print(f"TXT файл создан: {txt_file}")

        text_1 = "Ответ получен!\nРезультаты:\n\n"
        answer = "\n".join(lst)
        final_answer = f"{text_1}{answer}"
        final_answer_1 = split_message(final_answer)

        for f_an in final_answer_1:
            bot.reply_to(message, f_an)

@bot.message_handler(commands=["legal"])
def legal_text(message):
    bot.reply_to(message, "ПРАВИЛА КОНФИДЕНЦИАЛЬНОСТИ В СЕТИ! 🌐\n\n"
                          "1️⃣Береги свои личные данные!\n\n"
                          "Не выкладывай в открытый доступ свой полный адрес, номер телефона, паспортные данные или банковские карты.\n"
                          "Мошенники могут использовать эту информацию! Если сайт требует подтверждения личности — проверь его надёжность.\n\n"
                          "2️⃣Создавай надёжные пароли!\n\n"
                          "Простые пароли вроде «123456» или «password» взламывают за секунды!\n"
                          "Используй комбинации из букв, цифр и спецсимволов.\n"
                          "Включи двухфакторную аутентификацию (2FA) — это добавит защиту.\n\n"
                          "3️⃣Осторожнее с незнакомцами!\n\n"
                          "Если тебе пишет человек, которого ты не знаешь, — не переходи по его ссылкам и не скачивай файлы.\n"
                          "Это может быть вирус или фишинг!\n"
                          "Лучше сразу блокируй подозрительных пользователей.\n\n"
                          "4️⃣Настрой приватность в соцсетях!\n\n"
                          "Ограничь доступ к своим постам и фото только для друзей.\n"
                          "Отключи геолокацию в фотографиях и не отмечай свой дом на картах.\n"
                          "Чем меньше лишней информации в сети — тем безопаснее!\n\n"
                          "5️⃣Обновляй программы и избегай пиратского софта!\n\n"
                          "Вирусы часто прячутся в взломанных программах и устаревших приложениях.\n"
                          "Всегда скачивай софт с официальных сайтов и ставь автоматические обновления.\n")

@bot.message_handler(commands=["report"])
def make_report(message):
    try:
        with open("report.txt", "rb") as file:
            bot.reply_to(message, "Файл отчёта по поиску создан!")
            bot.send_document(message.chat.id, file)
    except FileNotFoundError:
        bot.reply_to(message, "Отчет не найден. Сначала выполните поиск с помощью /username")

bot.polling(none_stop=True)