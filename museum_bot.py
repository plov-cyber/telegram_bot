from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CommandHandler

from data import TOKEN


def entry(update, context):
    update.message.reply_text('Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!')
    update.message.reply_text('Далее вы можете пройти в зал "Греческая культура" или на выход.',
                              reply_markup=ReplyKeyboardMarkup([['Пройти в первый зал'],
                                                                ['Выход']],
                                                               one_time_keyboard=True))
    return 1


def exit_museum(update, context):
    update.message.reply_text('Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!')
    return ConversationHandler.END


def first_hall(update, context):
    update.message.reply_text('Вы находитесь в зале "Греческая культура".')
    update.message.reply_text('В зале представлены многочисленные хозяйственные принадлежности,\n'
                              'а также орудия труда, использованные в быту у древних греков.')
    update.message.reply_text('Далее вы можете пройти в зал "Итало-Греческая война" или на выход.',
                              reply_markup=ReplyKeyboardMarkup([['Пройти в следующий зал'],
                                                                ['Выход']],
                                                               one_time_keyboard=True))
    return 2


def second_hall(update, context):
    update.message.reply_text('Вы находитесь в зале "Итало-Греческая война".')
    update.message.reply_text('В зале изображены сцены из битв Греческой войны,\n'
                              'начавшей Вторую Мировую Войну на Балканах.')
    update.message.reply_text('Пройдёмте в следующий зал - "Архитектура Древней Греции".',
                              reply_markup=ReplyKeyboardMarkup([['Пройти в третий зал']],
                                                               one_time_keyboard=True))
    return 3


def third_hall(update, context):
    update.message.reply_text('Вы находитесь в зале "Архитектура Древней Греции".')
    update.message.reply_text('Вокруг себя вы можете увидеть множество чертежей, а также набросков\n'
                              'величественных сооружений, построенных много веков назад руками древних греков.')
    update.message.reply_text('Отсюда вы можете пройти в последний зал - "Национальная греческая одежда"\n'
                              'или вернуться в первый.', reply_markup=ReplyKeyboardMarkup(
        [['Пройти в последний зал'], ['Вернуться в первый зал']], one_time_keyboard=True))
    return 4


def fourth_hall(update, context):
    update.message.reply_text('Вы находитесь в зале "Национальная греческая одежда".')
    update.message.reply_text('На экспонатах представлена многочисленная одежда,\n'
                              'широко использовавшаяся в Древней Греции.')
    update.message.reply_text('Это был последний зал. Прошу вас вернуться в зал "Греческая культура".',
                              reply_markup=ReplyKeyboardMarkup([['Вернуться в первый зал']],
                                                               one_time_keyboard=True))


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', entry)],

        states={
            1: [MessageHandler(Filters.text(['Пройти в первый зал', 'Вернуться в первый зал']), first_hall)],
            2: [MessageHandler(Filters.text(['Пройти в следующий зал']), second_hall)],
            3: [MessageHandler(Filters.text(['Пройти в третий зал']), third_hall)],
            4: [MessageHandler(Filters.text(['Пройти в последний зал']), fourth_hall),
                MessageHandler(Filters.text(['Вернуться в первый зал']), first_hall)]
        },

        fallbacks=[MessageHandler(Filters.text(['Выход']), exit_museum)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
