import datetime
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, bot)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PHOTO, LOCATION, BIO = range(3)


def start(update, context):
    update.message.reply_text(
        'Привет,{}\n ,я - бот! Отправляй мне свои мемы!!!'.format(update.message.chat.first_name),
        one_time_keyboard=True)

    return PHOTO


def photo(update, context):
    chat_id = update.message.chat.id
    custom_path = ('/Users/PodrezOff/tgapp/pictures/')
    file = update.message.photo[-1].get_file()
    user = update.message.from_user
    logger.info(datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S") + ' ' + str(user.id))  # потом убрать
    file.download('{:%Y%m%d%H%M%S}'.format(datetime.datetime.now()) + ' ' + str(user.id) + '.jpg')
    update.message.reply_text('Изображение я скачал')
    bot.sendPhoto(update.message.chat_id, photo=
    file, caption="This is the test photo caption")
    update.message.photo(file)
    bot.send_media(update.message.chat_id, photo=file)

    return LOCATION


def skip_photo(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1344832905:AAGk2Uf1TsIhseaKtj-cjiooN11TVwnu1Ro", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

        },
        fallbacks=[CommandHandler('cancel', cancel)]

    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
