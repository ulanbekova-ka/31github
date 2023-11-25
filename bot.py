import cv2
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

TOKEN = '6668204272:AAEB-jUZuEyDuOnDEjaDRJKzYvryJ6Qjw7E'
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=None
    )


async def handle_images(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file = await context.bot.get_file(file_id)

        photo_path = 'received_image.jpg'
        await file.download_to_drive(photo_path)

        image = cv2.imread(photo_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Save the image with rectangles
        output_path = 'image_with_faces.jpg'
        cv2.imwrite(output_path, image)
        with open(output_path, 'rb') as photo:
            await update.message.reply_photo(photo, caption='Faces detected!')

    else:
        await update.message.reply_text('Please send an image.')


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_images))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
