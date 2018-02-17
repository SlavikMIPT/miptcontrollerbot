# -*- coding: utf-8 -*-
import config
import telebot
import os
import chat_settings
import re
# from urllib.parse import urlparse
import logging
from configparser import SafeConfigParser
from telebot import types
from time import sleep
from time import time
import shutil
from threading import Thread

# from threading import Lock

bot = telebot.TeleBot(config.token)

PATH_HOME = os.path.abspath('.')
SETTINGS_FILENAME = 'settings.conf'
SETTINGS_DIRNAME = 'settings'
BASIC_CHAT_NAME = '@mipt_board'
LINK_BASIC_CHAT = 't.me/mipt_board/'
LINK_BASIC_CHAT_MARKDOWN = 't.me/mipt\_board/'
# LINK_BASIC_CHAT = 't.me/detikapitsy/'
# LINK_BASIC_CHAT_MARKDOWN = 't.me/detikapitsy/'
PATH_SETTINGS_DIR = os.path.join(PATH_HOME, SETTINGS_DIRNAME)
PATH_SETTINGS_FILE = os.path.join(PATH_HOME, SETTINGS_FILENAME)
# class ProcessMessage(Thread):
#     def __init__(self, name, message):
#         Thread.__init__(self)
#         self.name = name
#         self.message = message
#
#     def run(self):
#         process_message(self.message)
#         msg = "%s is running" % self.name
#         print(msg)
#
#
# class ProcessCall(Thread):
#     def __init__(self, name, call):
#         Thread.__init__(self)
#         self.name = name
#         self.call = call
#
#     def run(self):
#         callback_button(self.call)
#         msg = "%s is running" % self.name
#         print(msg)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def create_callback_thread(call):
#     name = "Thread #%s" % (call.message.message_id)
#     call_thread = ProcessCall(name, call)
#     call_thread.start()


# def callback_button(call):
#     try:
#         chat_id = call.message.chat.id
#         settings_file_path = PATH_HOME + 'user_settings/id%s.conf' % str(chat_id)
#     except Exception as e:
#         logging.error(str('callback_button:') + str(e))


# @bot.message_handler(commands=['start'])
# def send_startup_message(message):
#     chat_id = message.chat.id
#     settings_file_path = PATH_HOME + 'user_settings/id%s.conf' % str(chat_id)
#     user_settings = SafeConfigParser()
#     try:
#         # with settings_lock:
#         user_settings.read(settings_file_path)
#         if not user_settings.has_section(str(chat_id)):
#             user_settings.add_section(str(chat_id))
#             if not user_settings.has_option(str(chat_id), 'get_video'):
#                 user_settings.set(str(chat_id), 'get_video', 'False')
#             if not user_settings.has_option(str(chat_id), 'bitrate'):
#                 user_settings.set(str(chat_id), 'bitrate', '192k')
#             if not user_settings.has_option(str(chat_id), 'request_n'):
#                 user_settings.set(str(chat_id), 'request_n', '0')
#             settings_fp = open(settings_file_path, 'w')
#             user_settings.write(settings_fp)
#             settings_fp.close()
#         bot.send_message(chat_id,
#                          text='Привет! Отправь мне ссылку на ролик YouTube,\nнапример эту https://youtu.be/9bZkp7q19f0 ',
#                          parse_mode='Markdown', disable_web_page_preview=True)
#     except Exception as e:
#         logging.error(str('send_startup_message:') + str(e))


# @bot.message_handler(content_types=["text"])
# def create_threads(message):
    # name = "Thread #%s" % (message.message_id)
    # my_thread = ProcessMessage(name, message)
    # my_thread.start()
@bot.message_handler(commands=['channels'])
def show_channels(message):
    try:
        chat_id = message.chat.id
        settings = chat_settings.init(chat_id, PATH_SETTINGS_DIR)
        text_to_send = ''
        for section in settings.sections():
            text_to_send += settings.get(section, 'about') + '\n'
            text_to_send += settings.get(section, 'tags') + '\n\n'
        msg_info = bot.send_message(chat_id, text_to_send, disable_web_page_preview=True, disable_notification=True, \
                                                parse_mode='Markdown')
        sleep(60)
        bot.delete_message(msg_info.chat.id,msg_info.message_id)
        bot.delete_message(chat_id,message.message_id)
    except Exception as e:
        logging.error(str('show_channels:') + str(e))


@bot.message_handler(commands=['help'])
def show_channels(message):
    try:

        chat_id = message.chat.id
        text_to_send = u'❗️ ВАЖНОЕ НА ВИДУ. БЕЗ ЗАПРЕТА НА ФЛУД.\n'
        text_to_send += u'🔸Поставьте в начало нужный хэштег, через пробел напишите ваше сообщение.\n'
        text_to_send += u'🔸Бот перешлёт его в нужный канал со ссылками на автора и сообщение в чате.\n'
        text_to_send += u'🔸Для использования markdown поставьте #markdown в конец сообщения.\n'
        text_to_send += u'🔸Новость, объявление, начало обсуждения не потеряются, а подробности останутся в чате.\n'
        text_to_send += u'❕ Каналы и хэштеги: \n/channels'


        msg_info = bot.send_message(chat_id, text_to_send, disable_web_page_preview=True, disable_notification=True, \
                                                parse_mode='Markdown')
        sleep(60)
        bot.delete_message(msg_info.chat.id,msg_info.message_id)
        bot.delete_message(chat_id,message.message_id)
    except Exception as e:
        logging.error(str('show_channels:') + str(e))


# @bot.message_handler(commands=['tags'])
# def show_hashtags(message):
#     chat_id = message.chat.id
#     settings = chat_settings.init(chat_id, PATH_SETTINGS_DIR)
#     text_to_send = u'Список хештегов:\n'
#     for section in settings.sections():
#             channel_name = settings.get(section, 'channel_name')
#             hashtag_string = settings.get(section, 'tags')
#             hashtag_split = re.split(r',', hashtag_string)
#             text_to_send += hashtag_string + u'\t-\t' + channel_name + '\n'
#     bot.send_message(chat_id, text_to_send, disable_web_page_preview=True, disable_notification=True)

def format_text_for_channel(msg_id,channel_name,username,hashtag,text,parse,preview):
    #remove hashtag
    text = re.sub(hashtag, '', text, flags=re.UNICODE)
    text_for_channel = text + '\n'
    if parse == 'markdown':
        username = re.sub(r'_', '\_', username, flags=re.UNICODE)
        channel_name = re.sub(r'_', '\_', channel_name, flags=re.UNICODE)
        msg_share_link = str(LINK_BASIC_CHAT_MARKDOWN) + str(msg_id)
        if not preview:
            text_for_channel += msg_share_link + '\n'
        else:
            text_for_channel += 't.me/' + str(channel_name[1:]) + '/' + str(msg_id) + '\n'
        text_for_channel += username + '\n'
        text_for_channel = re.sub(r'#markdown', '', text_for_channel, flags=re.UNICODE)
        text_for_channel += hashtag
    else:
        msg_share_link = str(LINK_BASIC_CHAT) + str(msg_id)
        if not preview:
            text_for_channel += msg_share_link + '\n'
        else:
            text_for_channel += 't.me/' + str(channel_name[1:]) + '/' + str(msg_id) + '\n'
        text_for_channel += username + '\n'
        text_for_channel += hashtag
    return text_for_channel


@bot.message_handler(content_types=["text"])
def process_message(message):  # Название функции не играет никакой роли, в принципе
    chat_id = message.chat.id
    msg_id = message.message_id
    user_name = '@' + message.from_user.username
    settings = chat_settings.init(chat_id, PATH_SETTINGS_DIR)
    text_incoming = message.text
    hashtag_match = re.match(r'#\w+', text_incoming, flags=re.UNICODE)
    hashtag_markdown = re.search(r'#markdown', text_incoming, flags=re.UNICODE)
    hashtag_incoming = hashtag_match.group(0)
    link_to_channel = ''
    if hashtag_incoming == '#remove':
        try:
            message_reply = message.reply_to_message
            user_reply_name = re.search(r'@\w+', message_reply.text, flags=re.UNICODE)
            link_to_channel = re.search(r't\.me/mipt_\D+/\d+', message_reply.text, flags=re.UNICODE)
            link_to_channel = link_to_channel.group(0)
            link_to_channel = re.sub('t\.me/','',link_to_channel, flags=re.UNICODE)
            logging.info(str(link_to_channel))
            if user_reply_name.group(0) == user_name:
                chname, chmessageid = re.split(r'/', link_to_channel, flags=re.UNICODE)
                bot.delete_message(bot.get_chat('@' + chname).id, int(chmessageid))
                bot.delete_message(message_reply.chat.id, message_reply.message_id)
                bot.delete_message(chat_id, msg_id)
        except Exception as e:
            logging.info(e)
    if hashtag_match and chat_id == bot.get_chat(BASIC_CHAT_NAME).id:
        if hashtag_incoming != '#remove':
            for section in settings.sections():
                hashtag_string = settings.get(section, 'tags')
                hashtag_split = re.split(r',', hashtag_string, flags=re.UNICODE)
                for each_tag in hashtag_split:
                    if each_tag == hashtag_incoming:
                        channel_name = settings.get(section, 'channel_name')
                        channel_id = bot.get_chat(channel_name).id
                        if hashtag_markdown:
                            parse = 'markdown'
                        else:
                            parse = None
                        text_for_channel = format_text_for_channel(msg_id,channel_name, user_name, hashtag_incoming,\
                                                                    text_incoming, parse, True)
                        msg_prev = bot.send_message(chat_id,text_for_channel,parse_mode=parse,\
                                                    disable_web_page_preview=True,disable_notification=True)
                        text_for_channel = format_text_for_channel(msg_prev.message_id,channel_name,user_name,\
                                                                    hashtag_incoming,text_incoming,parse,False)
                        msg_chn = bot.send_message(channel_id, text_for_channel, parse_mode=parse,\
                                                    disable_web_page_preview=True, disable_notification=True)
                        text_for_channel = format_text_for_channel(msg_chn.message_id, channel_name, user_name,\
                                                                   hashtag_incoming,\
                                                                   text_incoming, parse, True)
                        bot.edit_message_text(text_for_channel,  msg_prev.chat.id, msg_prev.message_id,\
                                                inline_message_id=None, parse_mode=parse,\
                                                disable_web_page_preview=True)
                        # bot.delete_message(msg_prev.chat.id, msg_prev.message_id)
                        # bot.send_message(chat_id, text_for_channel, parse_mode=parse, \
                        #                  disable_web_page_preview=True, disable_notification=True
                        bot.delete_message(chat_id, msg_id)



if __name__ == '__main__':
    # Избавляемся от спама в логах от библиотеки requests
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    # Настраиваем наш логгер
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO, \
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
    bot.polling(none_stop=True)
