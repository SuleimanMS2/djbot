import time

from django.conf import settings
from telegram_bot_pagination import InlineKeyboardPaginator
import random
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from ..models import Test

bot = Bot(token='5256793942:AAH6mZk1YuyWEUWJs2OM-lEi09puAmAk4ec')

hostname = f'{settings.HOST}'
bot.set_webhook(hostname)

dispatcher = Dispatcher(bot, None)

list = {}
global_page = {}
question_id = {}
stop_time = {}
fan_nomi = {}


def start(update, context):
    update.message.reply_text(f'Hello {update.effective_user.first_name}\n'
                              f'Testni boshalsh uchun \'/bowlash\' ni boshing.')


def bowlash(update, context):
    userid = update.effective_user.id
    keyboard = [
        [KeyboardButton('Test'), KeyboardButton('Bioloyiya')],
        [KeyboardButton('Matematika')],
        [KeyboardButton('Ingliz tili'), KeyboardButton('Tarix')],
    ]
    update.message.reply_text(text='Bizda mavjud testlar',
                              reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))

    # list[userid] = {}


def begin(update, context):
    userid = update.effective_user.id
    course = update.message.text
    if course == 'Test' or course == 'Tarix' or course == 'Ingliz tili' or course == 'Matematika' or course == 'Bioloyiya':
        fan_nomi[userid] = course
        keyboard = [
            [KeyboardButton(text='Bowlash')],
            [KeyboardButton(text='Orqaga')]
        ]
        update.message.reply_text(text=f'Ism: {update.effective_user.first_name}\n'
                                       f'Fan: {course}\n'
                                       f'Vaqt: 30 minut',
                                  reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                                                                   one_time_keyboard=True))

        random_base = [i for i in eval(fan_nomi[userid]).objects.all().values()]
        question_id[userid] = random.sample(random_base, 5)
        stop_time[userid] = None

        for x in range(1, 6):
            question_id[userid][x - 1].setdefault("nomer", x)

        return middle_handler(update, context)
    else:
        return middle_handler(update, context)


def middle_handler(update, context):
    course = update.message.text
    if course == 'Bowlash' or course == 'Orqaga':
        if course == 'Bowlash':
            return test_begin(update, context)
        elif course == 'Orqaga':
            return bowlash(update, context)
    else:
        pass


def test_begin(update, context):
    userid = update.effective_user.id

    list[userid] = {}
    global_page[userid] = 1

    paginator = InlineKeyboardPaginator(
        len(question_id[userid]),
    )

    random_answer = ['a', 'b', 'c', 'd']
    selected_random_answer = random.sample(random_answer, 4)
    paginator.add_before(
        InlineKeyboardButton(text=question_id[userid][0][selected_random_answer[0]],
                             callback_data=selected_random_answer[0]))
    paginator.add_before(
        InlineKeyboardButton(text=question_id[userid][0][selected_random_answer[1]],
                             callback_data=selected_random_answer[1]))
    paginator.add_before(
        InlineKeyboardButton(text=question_id[userid][0][selected_random_answer[2]],
                             callback_data=selected_random_answer[2]))
    paginator.add_before(
        InlineKeyboardButton(text=question_id[userid][0][selected_random_answer[3]],
                             callback_data=selected_random_answer[3]))

    update.message.reply_text(
        text=f"№ {question_id[userid][0]['nomer']}\n{question_id[userid][0]['question']}",
        reply_markup=paginator.markup,
    )


def test_query(update, context):
    userid = update.effective_user.id
    query = update.callback_query
    query.answer()
    data = query.data
    if data == 'a' or data == 'b' or data == 'c' or data == 'd':
        list[userid][question_id[userid][global_page[userid] - 1]['id']] = data
        if question_id[userid][-1] == question_id[userid][int(global_page[userid] - 1)]:
            pop = int(global_page[userid] - 1)
            global_page[userid] = pop
            question_id[userid].pop(pop)
            paginator = InlineKeyboardPaginator(
                page_count=len(question_id[userid]),
                current_page=pop,
            )
            response = pop - 1
            random_answer = ['a', 'b', 'c', 'd']
            selected_random_answer = random.sample(random_answer, 4)
            if len(list[userid]) < 5:
                paginator.add_before(
                    InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[0]],
                                         callback_data=selected_random_answer[0]))
                paginator.add_before(
                    InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[1]],
                                         callback_data=selected_random_answer[1]))
                paginator.add_before(
                    InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[2]],
                                         callback_data=selected_random_answer[2]))
                paginator.add_before(
                    InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[3]],
                                         callback_data=selected_random_answer[3]))
                paginator.add_after(
                    InlineKeyboardButton(text='🛑 Testni yakunlash 🛑', callback_data='stop'))

                query.edit_message_text(
                    text=f"№ {question_id[userid][response]['nomer']}\n{question_id[userid][response]['question']}",
                    reply_markup=paginator.markup,
                    parse_mode='Markdown'
                )
            else:
                help(update, context)
        else:
            pop = int(global_page[userid] - 1)
            page_num = int(global_page[userid])
            question_id[userid].pop(pop)

            paginator = InlineKeyboardPaginator(
                page_count=len(question_id[userid]),
                current_page=page_num,
            )
            response = page_num - 1
            random_answer = ['a', 'b', 'c', 'd']
            selected_random_answer = random.sample(random_answer, 4)

            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[0]],
                                     callback_data=selected_random_answer[0]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[1]],
                                     callback_data=selected_random_answer[1]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[2]],
                                     callback_data=selected_random_answer[2]))
            paginator.add_before(
                InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[3]],
                                     callback_data=selected_random_answer[3]))
            paginator.add_after(
                InlineKeyboardButton(text='🛑 Testni yakunlash 🛑', callback_data='stop'))

            query.edit_message_text(
                text=f"№ {question_id[userid][response]['nomer']}\n{question_id[userid][response]['question']}",
                reply_markup=paginator.markup,
                parse_mode='Markdown'
            )
    elif data == 'stop':
        help(update, context)
    elif data == 'Ha':
        error(update, context)
    else:
        int_data = int(data)
        global_page[userid] = int_data
        paginator = InlineKeyboardPaginator(
            page_count=len(question_id[userid]),
            current_page=int_data,
        )

        response = global_page[userid] - 1
        random_answer = ['a', 'b', 'c', 'd']
        selected_random_answer = random.sample(random_answer, 4)

        paginator.add_before(
            InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[0]],
                                 callback_data=selected_random_answer[0]))
        paginator.add_before(
            InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[1]],
                                 callback_data=selected_random_answer[1]))
        paginator.add_before(
            InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[2]],
                                 callback_data=selected_random_answer[2]))
        paginator.add_before(
            InlineKeyboardButton(text=question_id[userid][response][selected_random_answer[3]],
                                 callback_data=selected_random_answer[3]))
        paginator.add_after(
            InlineKeyboardButton(text='🛑 Testni yakunlash 🛑', callback_data='stop'))
        query.edit_message_text(
            text=f"№ {question_id[userid][response]['nomer']}\n{question_id[userid][response]['question']}",
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )


def countdown(update, context):
    # userid = update.effective_user.id
    # time_sec = 20
    # b = update.message.reply_text(text="00:21")
    # test_begin(update, context)
    # while update:
    #     mins, secs = divmod(time_sec, 60)
    #     timeformat = '{:02d}:{:02d}'.format(mins, secs)
    #     context.bot.edit_message_text(text=timeformat, message_id=b.message_id,
    #                                   chat_id=update.message.chat_id)
    #     time.sleep(1)
    #     time_sec -= 1
    #     if time_sec == 0 or len(list[userid]) == 5 or stop_time[userid] == 'stop':
    #         context.bot.delete_message(chat_id=b.chat_id, message_id=b.message_id)
    #         context.bot.delete_message(chat_id=b.chat_id, message_id=b.message_id + 1)
    #         return help(update, context)
    pass


def help(update, context):
    userid = update.effective_user.id
    summa = 0
    for key, value in list.items():
        if key == userid:
            for kalit, qiymat in value.items():
                if qiymat == 'a':
                    summa += 1
    keyboard = [
                   InlineKeyboardButton(text='❌ Xatolarni ko\'rish ❌', callback_data='Ha')
               ],
    try:
        update.callback_query.message.edit_text(text=f'Test Yakunlandi\n\nTo`g`ri javoblar: {summa} ta\n'
                                                     f'Noto`g\'ri javoblar: {len(list[userid]) - summa} ta\n'
                                                     f'Javobsiz testlar: {len(question_id[userid])} ta\n\n'
                                                     f'/bowlash - Boshqa testlarni ishlash uchun',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    except AttributeError:
        pass


def error(update, context):
    userid = update.effective_user.id
    query = update.callback_query
    query.answer()
    for key, value in list.items():
        if key == userid:
            for kalit, qiymat in value.items():
                if qiymat == 'b':
                    sav = Test.objects.get(id=kalit)
                    query.message.reply_text(
                        f"№ {kalit}\n{sav.question}\na) {sav.a}✅\nb) {sav.b}❌\nc) {sav.c}\nd) {sav.d}")
                elif qiymat == 'c':
                    sav = Test.objects.get(id=kalit)
                    query.message.reply_text(
                        f"№ {kalit}\n{sav.question}\na) {sav.a}✅\nb) {sav.b}\nc) {sav.c}❌\nd) {sav.d}")
                elif qiymat == 'd':
                    sav = Test.objects.get(id=kalit)
                    query.message.reply_text(
                        f"№ {kalit}\n{sav.question}\na) {sav.a}✅\nb) {sav.b}\nc) {sav.c}\nd) {sav.d}❌")
    list[userid] = {}


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('bowlash', bowlash))
dispatcher.add_handler(MessageHandler(Filters.text, begin))
dispatcher.add_handler(MessageHandler(Filters.text, middle_handler))
dispatcher.add_handler(CommandHandler('test_begin', test_begin))
dispatcher.add_handler(CallbackQueryHandler(test_query))

dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CallbackQueryHandler(error))

dispatcher.add_handler(CommandHandler('countdown', countdown))
