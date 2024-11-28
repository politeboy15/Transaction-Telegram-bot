from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['Адрес карты', 'Адрес кошелька']]
    update.message.reply_text(
        'Привет! Я ваш Telegram-бот для транзакций. Выберите способ транзакции:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

# Функция для обработки выбора способа транзакции
def choose_method(update: Update, context: CallbackContext) -> None:
    method = update.message.text
    if method == 'Адрес карты':
        update.message.reply_text('Пожалуйста, введите адрес карты:')
        context.user_data['method'] = 'card'
    elif method == 'Адрес кошелька':
        update.message.reply_text('Пожалуйста, введите адрес кошелька:')
        context.user_data['method'] = 'wallet'

# Функция для обработки ввода адреса карты или кошелька
def process_address(update: Update, context: CallbackContext) -> None:
    address = update.message.text
    method = context.user_data.get('method')
    if method == 'card':
        update.message.reply_text(f'Адрес карты: {address}. Транзакция будет обработана.')
    elif method == 'wallet':
        update.message.reply_text(f'Адрес кошелька: {address}. Транзакция будет обработана.')

def main() -> None:
    updater = Updater("YOUR_TOKEN_HERE")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработчик выбора способа транзакции
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Адрес карты|Адрес кошелька)$'), choose_method))

    # Обработчик ввода адреса карты или кошелька
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_address))

    # Запуск бота
    updater.start_polling()
    
    # Отсановка бота
    updater.idle()
if __name__ == '__main__':
    main()