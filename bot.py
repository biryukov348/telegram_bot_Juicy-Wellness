import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Ваш ID пользователя
YOUR_TELEGRAM_ID = 123456789  # Замените на ваш ID

# Словарь для хранения соответствия между сообщениями пользователей и вашими ответами
user_dict = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Тебя приветствует служба заботы Juicy Wellness Club. Расскажи мне, что случилось?')

def handle_user_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user = update.message.from_user

    # Отправляем заглушку пользователю
    update.message.reply_text('Принято! Дай мне немного времени, я разберусь и скоро вернусь! Помнишь, что активность делает наше тело здоровым и классно снимает стресс?) Есть идея скрасить твое ожидание зарядкой:https://vimeo.com/1006569443?share=copy Как насчет того, чтобы размяться?)')

    # Формируем сообщение для вас
    forwarded_message = context.bot.send_message(
        chat_id=YOUR_TELEGRAM_ID,
        text=f"<b>Новое сообщение от {user.first_name} {user.last_name} (@{user.username}):</b>\n\n{user_message}",
        parse_mode=ParseMode.HTML
    )

    # Сохраняем соответствие между ID сообщения вам и ID чата пользователя
    user_dict[forwarded_message.message_id] = user.id

def handle_owner_reply(update: Update, context: CallbackContext):
    # Проверяем, что сообщение от вас и является ответом на сообщение бота
    if update.message.from_user.id == YOUR_TELEGRAM_ID and update.message.reply_to_message:
        original_message_id = update.message.reply_to_message.message_id

        # Получаем ID пользователя, которому нужно отправить ответ
        user_id = user_dict.get(original_message_id)

        if user_id:
            # Отправляем ответ пользователю
            context.bot.send_message(
                chat_id=user_id,
                text=update.message.text
            )
            update.message.reply_text('Ваш ответ отправлен пользователю.')
        else:
            update.message.reply_text('Не удалось определить пользователя для ответа.')
    else:
        update.message.reply_text('Пожалуйста, отвечайте на сообщение, чтобы отправить ответ пользователю.')

def main():
    updater = Updater('YOUR_TELEGRAM_BOT_TOKEN', use_context=True)  # Замените на токен вашего бота
    dp = updater.dispatcher

    # Обработчики команд и сообщений
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.user(user_id=YOUR_TELEGRAM_ID), handle_user_message))
    dp.add_handler(MessageHandler(Filters.text & Filters.user(user_id=YOUR_TELEGRAM_ID), handle_owner_reply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
