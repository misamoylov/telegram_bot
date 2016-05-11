# -*- coding: utf-8 -*-
import config
import vk_helpers
import vk_parser
import time
import logging
import telebot

bot = telebot.TeleBot(config.token)


def send_new_posts(messages, last_id):
    chat_ids = []
    with open('chat_ids.txt', 'rt') as file:
        for line in file.readlines():
            if line not in chat_ids:
                chat_ids.append(int(line))
    for message in messages:
        if message['id'] <= last_id:
            break
        else:
            # text = message['text']
            text = "\n".join(message['text'].split("<br>"))
            for chat in chat_ids:
                bot.send_message(chat_id=chat, text=text)
                if message.has_key('attachment') and message['attachment'].has_key('photo'):
                    photo_url = message['attachment']['photo']['src_big']
                    photo = vk_parser.get_repost_photo(photo_url)
                    bot.send_photo(chat_id=chat, photo=photo)
        # Спим секунду, чтобы избежать разного рода ошибок и ограничений (на всякий случай!)
            time.sleep(1)
    return


def check_new_posts_vk():
    # Пишем текущее время начала
    logging.info('[VK] Started scanning for new posts')
    with open(config.FILENAME_VK, 'rt') as file:
        last_id = int(file.read())
        if last_id is None:
            logging.error('Could not read from storage. Skipped iteration.')
            return
        logging.info('Last ID (VK) = {!s}'.format(last_id))
    feed = vk_helpers.get_posts_from_wall()
    if feed is not None:
        entries = feed['response'][1:]
        if entries[0].has_key('is_pinned'):
            send_new_posts(entries[1:], last_id)
            with open(config.FILENAME_VK, 'wt') as file:
                # Записываем новый last_id в файл.
                file.write(str(entries[1]['id']))
                logging.info('New last_id (VK) is {!s}'.format((entries[1]['id'])))
        else:
            send_new_posts(entries, last_id)
            with open(config.FILENAME_VK, 'wt') as file:
                file.write(str(entries[0]['id']))
                logging.info('New last_id (VK) is {!s}'.format((entries[0]['id'])))
    # try:
    #     feed = vk_helpers.get_posts_from_wall()
    #     # Если ранее случился таймаут, пропускаем итерацию. Если всё нормально - парсим посты.
    #     if feed is not None:
    #         entries = feed['response'][1:]
    #         try:
    #             # Если пост был закреплен, пропускаем его
    #             tmp = entries[0]['is_pinned']
    #             # И запускаем отправку сообщений
    #             send_new_posts(entries[1:], last_id)
    #         except KeyError:
    #             send_new_posts(entries, last_id)
    #         # Записываем новый last_id в файл.
    #         with open(config.FILENAME_VK, 'wt') as file:
    #             try:
    #                 tmp = entries[0]['is_pinned']
    #                 # Если первый пост - закрепленный, то сохраняем ID второго
    #                 file.write(str(entries[1]['id']))
    #                 logging.info('New last_id (VK) is {!s}'.format((entries[1]['id'])))
    #             except KeyError:
    #                 file.write(str(entries[0]['id']))
    #                 logging.info('New last_id (VK) is {!s}'.format((entries[0]['id'])))
    # except Exception as ex:
    #     logging.error('Exception of type {!s} in check_new_post(): {!s}'.format(type(ex).__name__, str(ex)))
    #     pass
    logging.info('[VK] Finished scanning')
    return

if __name__ == '__main__':
    # Избавляемся от спама в логах от библиотеки requests
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    # Настраиваем наш логгер
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')

    while True:
        check_new_posts_vk()
        # Пауза в 4 минуты перед повторной проверкой
        logging.info('[App] Script went to sleep.')
        time.sleep(10)
#    time.sleep(60 * 4)
        logging.info('[App] Script exited.\n')
