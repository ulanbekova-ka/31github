import os
import cv2
from deepface import DeepFace
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, ConversationHandler

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = DeepFace.build_model("Emotion")
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hello, {user.mention_markdown_v2()}\! I am a bot for recommendations of all kinds of media based on your current mood and tastes\. Let\'s start with a small questionnaire to know you better\.',
        reply_markup=None
    )
    await ask_questions(update, context)


async def ask_questions(update: Update, context: CallbackContext) -> None:
    questions = [
        "What's your favorite character?",
        "What is your favorite color?",
        "What is your favorite book?"
    ]

    for question in questions:
        await update.message.reply_text(question)
        # You can store the user's answers in context.user_data

    await update.message.reply_text("Thank you! Now I need a photo of your face to detect the current emotion")


async def handle_images(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file = await context.bot.get_file(file_id)

        photo_path = 'received_image.jpg'
        await file.download_to_drive(photo_path)

        image = cv2.imread(photo_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) == 1:
            emotion = ""
            for (x, y, w, h) in faces:
                face_roi = gray[y:y + h, x:x + w]
                resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)
                normalized_face = resized_face / 255.0
                reshaped_face = normalized_face.reshape(1, 48, 48, 1)
                preds = model.predict(reshaped_face)[0]
                emotion_idx = preds.argmax()
                emotion = emotion_labels[emotion_idx]
            await update.message.reply_text(f'Emotion detected: {emotion}')

            await show_media_options(update)

        else:
            await update.message.reply_text('I need a photo of your face. Make sure there is exactly one face in the photo.')

    else:
        await update.message.reply_text('Please send an image.')


async def show_media_options(update: Update) -> None:
    # Show media options as buttons
    keyboard = [
        [InlineKeyboardButton("/anime", callback_data='anime')],
        [InlineKeyboardButton("/book", callback_data='book')],
        [InlineKeyboardButton("/movie", callback_data='movie')],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Choose a media:', reply_markup=reply_markup)


def main() -> None:
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_images))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
