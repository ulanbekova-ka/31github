from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TOKEN = '6668204272:AAEB-jUZuEyDuOnDEjaDRJKzYvryJ6Qjw7E'


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=None
    )


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
