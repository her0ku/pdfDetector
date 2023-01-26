import os
import telebot
import sys
import re

import creds
import check_module


bot = telebot.TeleBot(creds.api_key, parse_mode=None)

sys.getdefaultencoding()
@bot.message_handler(commands=['start'])
def send_intro(message):
	bot.reply_to(message, "Бот готов к работе, загружай pdf и погнали!))))0)" + "\n есть навигация /navigation")

@bot.message_handler(commands=['navigation'])
def send_intro(message):
    bot.reply_to(message, "/start - поднимает бота)" + "\n/policy - это политика конфеденциальности, что документы отправленные в чат, остаются только в чате"
    + '\n/help - что делает бот')

@bot.message_handler(commands=['policy'])
def send_intro(message):
    bot.send_document(message.chat.id, open(r'politika.pdf', 'rb'))


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Бот проверяет .pdf файлы на различные JS уязвимости' + '\nМетаданные - это поле отвечает за то,'+ 
    'что приложение не было написано в одном из поплуряных pdf хакер-мейкеров\n' + 'js_exploit - это тот вредоносный код, который находится в pdf файле'
    + '\nЕсли везде статусы ОК - все круто, не ОК лучше файл не открывать, четсно говорю не надо братан!')


@bot.message_handler(content_types=['document'])
def pdf(message):
    file_info = bot.get_file(message.document.file_id)
    if '.pdf' in message.document.file_name:
        downloaded_file = bot.download_file(file_info.file_path)
        if os.path.exists(os.path.dirname(__file__) + '/uploads/'):
            src = os.path.dirname(__file__) + '/uploads/' + message.document.file_name
        else:
            os.mkdir(os.path.dirname(__file__) + '/uploads/')
            src = os.path.dirname(__file__) + '/uploads/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        meta, js_dump = check_module.pdf_analyzer(src)
        file_name = str(message.document.file_name).replace('.pdf', '').replace(' ', '_').replace('-', '_').replace('.','')
        bot.send_message(message.chat.id, 'File name: ' + '#' + file_name + '\nPDF ANALYZER:\n' + 'Metadata: ' + meta + '\nJs_exploit: ' + js_dump)


bot.polling(True)