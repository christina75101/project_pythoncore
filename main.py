#!/usr/bin/python3
import logging
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot_parser import Site
import bot_parser
from telegram import ParseMode
import ssl


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = {}


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def start(bot, update):
    """Main configuration settings"""
    # query = update.callback_query
    print(update.message.chat_id)
    print(update.message.message_id)
    global config

    config = {update.message.chat_id: {Site.BASH_ORG: True,
                                       Site.ZADOLBALI: True,
                                       Site.KILL_ME_PLS: True}
              }

    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())


def main_menu(bot, update):
    """Method which calls the main menu of the bot"""
    query = update.callback_query
    # print(query.message.chat_id)
    # print(query.message.message_id)
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=main_menu_message(),
                          reply_markup=main_menu_keyboard())


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Update', callback_data='upd')],
                [InlineKeyboardButton('Channels', callback_data='chnl')]]
    return InlineKeyboardMarkup(keyboard)


def main_menu_message():
    return 'Choose the option in main menu:'


def update_menu(bot, update):
    """Method creates a menu depends on on/off buttons"""

    query = update.callback_query
    message = 'You choose channels you want to follow in Channels menu:'

    dynamic_keyboard = []

    if config[query.message.chat_id][Site.BASH_ORG] is True:
        dynamic_keyboard.append([InlineKeyboardButton('Bash', callback_data='b_upd')])
    if config[query.message.chat_id][Site.ZADOLBALI] is True:
        dynamic_keyboard.append([InlineKeyboardButton('Zadolbali', callback_data='z_upd')])
    if config[query.message.chat_id][Site.KILL_ME_PLS] is True:
        dynamic_keyboard.append([InlineKeyboardButton('KillMePls', callback_data='k_upd')])
    dynamic_keyboard.append([InlineKeyboardButton('Main menu', callback_data='main')])

    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=message,
                          reply_markup=InlineKeyboardMarkup(dynamic_keyboard))


def bashorg_update(bot, update):
    """Method gets data from bash.im"""
    query = update.callback_query
    feed_item = bot_parser.get_preformatted_text(site=Site.BASH_ORG)
    bot.send_message(query.message.chat.id, feed_item, parse_mode=ParseMode.HTML)


def kmp_update(bot, update):
    """Method gets data from killpls.me"""
    query = update.callback_query
    feed_item = bot_parser.get_preformatted_text(site=Site.KILL_ME_PLS)
    bot.send_message(query.message.chat.id, feed_item, parse_mode=ParseMode.HTML)


def zadolbali_update(bot, update):
    """Method gets data from zadolba.li"""
    query = update.callback_query
    feed_item = bot_parser.get_preformatted_text(site=Site.ZADOLBALI)
    bot.send_message(query.message.chat.id, feed_item, parse_mode=ParseMode.HTML)


def channels_menu(bot, update):
    """Method which creates the channels keyboard"""

    query = update.callback_query
    message = 'Choose channels you want to follow:'
    B_on, B_off = ('! ON', 'OFF') if config[query.message.chat_id][Site.BASH_ORG] is True else ('ON', '! OFF')
    Z_on, Z_off = ('! ON', 'OFF') if config[query.message.chat_id][Site.ZADOLBALI] is True else ('ON', '! OFF')
    K_on, K_off = ('! ON', 'OFF') if config[query.message.chat_id][Site.KILL_ME_PLS] is True else ('ON', '! OFF')
    keyboard = [[InlineKeyboardButton('BASH', url='https://bash.im/'),
                 InlineKeyboardButton(B_on, callback_data='b_on'),
                 InlineKeyboardButton(B_off, callback_data='b_off')],

                [InlineKeyboardButton('ZADOLBALI', url='https://bash.im/'),
                 InlineKeyboardButton(Z_on, callback_data='z_on'),
                 InlineKeyboardButton(Z_off, callback_data='z_off')],

                [InlineKeyboardButton('KMP', url='https://bash.im/'),
                 InlineKeyboardButton(K_on, callback_data='k_on'),
                 InlineKeyboardButton(K_off, callback_data='k_off')],

                [InlineKeyboardButton('Main menu', callback_data='main')]]

    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=message,
                          reply_markup=InlineKeyboardMarkup(keyboard))


def on_off_switch(bot, update):
    """Method controls on/off buttons, which filter channels"""

    query = update.callback_query
    print(query.message.chat_id)
    print(query.message.message_id)
    global config

    if query.data == 'b_on':
        config[query.message.chat_id][Site.BASH_ORG] = True
    elif query.data == 'b_off':
        config[query.message.chat_id][Site.BASH_ORG] = False

    if query.data == 'z_on':
        config[query.message.chat_id][Site.ZADOLBALI] = True
    elif query.data == 'z_off':
        config[query.message.chat_id][Site.ZADOLBALI] = False

    if query.data == 'k_on':
        config[query.message.chat_id][Site.KILL_ME_PLS] = True
    elif query.data == 'k_off':
        config[query.message.chat_id][Site.KILL_ME_PLS] = False

    channels_menu(bot, update)


def help(bot, update):
    """Method responds to the command help"""
    update.message.reply_text("Use /start to test this bot. \n"
                              "Use Channels to choose which channels you want to read \n"
                              "Use Update/Channel button to get the last post from the site")

def repeat_messages(bot, update):
    update.message.reply_text("Write a command: /help to get information or call the menu by command /start")



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    updater = Updater(token='680590827:AAH5HD1cCt_RxQhy8i2vbt4q6yzNpRYlcBE')

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, repeat_messages))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(update_menu, pattern='upd'))
    updater.dispatcher.add_handler(CallbackQueryHandler(channels_menu, pattern='chnl'))
    updater.dispatcher.add_handler(CallbackQueryHandler(bashorg_update, pattern='b_upd'))
    updater.dispatcher.add_handler(CallbackQueryHandler(zadolbali_update, pattern='z_upd'))
    updater.dispatcher.add_handler(CallbackQueryHandler(kmp_update, pattern='k_upd'))
    updater.dispatcher.add_handler(CallbackQueryHandler(on_off_switch))
    updater.dispatcher.add_error_handler(error)
    
    updater.start_polling()
