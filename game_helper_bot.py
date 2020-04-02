from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
import random

from data import TOKEN

start_keyboard = ReplyKeyboardMarkup([['/dice', '/timer']], one_time_keyboard=True)
dice_keyboard = ReplyKeyboardMarkup([['Кинуть один шестигранный кубик'],
                                     ['Кинуть два шестигранных кубика'],
                                     ['Кинуть 20-гранный кубик'],
                                     ['Вернуться назад']], one_time_keyboard=False)
timer_keyboard = ReplyKeyboardMarkup([['30 секунд'],
                                      ['1 минута'],
                                      ['5 минут'],
                                      ['Вернуться назад']], one_time_keyboard=True)
reset_keyboard = ReplyKeyboardMarkup([['/close']], one_time_keyboard=True)

times = {
    '30 секунд': 30,
    '1 минута': 60,
    '5 минут': 300
}
time = None


def start(update, context):
    update.message.reply_text('Выберите действие:', reply_markup=start_keyboard)


def dice(update, context):
    update.message.reply_text('Выберите опцию:', reply_markup=dice_keyboard)


def timer(update, context):
    update.message.reply_text('Выберите время:', reply_markup=timer_keyboard)


def text_message(update, context):
    global time
    text = update.message.text
    if text == 'Вернуться назад':
        update.message.reply_text('Выбрите действие:', reply_markup=start_keyboard)
    elif text == 'Кинуть один шестигранный кубик':
        update.message.reply_text(f'Вам выпало число {random.randint(1, 6)}')
    elif text == 'Кинуть два шестигранных кубика':
        update.message.reply_text(f'Вам выпали числа {random.randint(1, 6)} и {random.randint(1, 6)}')
    elif text == 'Кинуть 20-гранный кубик':
        update.message.reply_text(f'Вам выпало число {random.randint(1, 20)}')
    elif text in times:
        chat_id = update.message.chat_id
        due = times[text]
        time = text
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(task, due, context=chat_id)
        context.chat_data['job'] = new_job
        update.message.reply_text(f'Засёк время {text}', reply_markup=reset_keyboard)


def task(context):
    job = context.job
    context.bot.send_message(job.context, text=f'Время {time} истекло', reply_markup=timer_keyboard)


def close(update, context):
    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']
    update.message.reply_text('Таймер сброшен', reply_markup=timer_keyboard)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('dice', dice))
    dp.add_handler(CommandHandler('timer', timer))
    dp.add_handler(CommandHandler('close', close))
    dp.add_handler(MessageHandler(Filters.text, text_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
