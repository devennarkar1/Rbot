from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
import nest_asyncio  # This is the solution to the event loop issue
import time

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment variable
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("No TOKEN found in .env file")

# Define messages to be sent
FIRST_MESSAGE = (
    "🚨 **Want the link?**\n\n\n\n"
    "🎥 Just watch the video for *90 seconds* ⏱️ And hit the SUBSCRIBE Button 🔔.\n\n\n\n"
    "👇👇👇\n"
    "👉 [Watch here!](https://youtu.be/oeenz5JTaoo) 😎\n\n\n"
    "After that, You Will Get LINK!"
)

SECOND_MESSAGE = "⏳ Click the link to get the link!"
LAST_MESSAGE = (
    "🎯 Ready for the reward?\n"
    "🎁 Here’s your exclusive link:\n\n\n"
    "👉 https://t.me/+z0oxXjImMvg1NmNl\n\n\n"
    "😎 Enjoy!"
)

# Dictionary to track messages by user
message_times = {}

# Function to handle errors
def handle_error(exception, message="An error occurred"):
    print(f"{message}: {exception}")
    # You can also log this to a file if needed

# This function will send the first, second, and third messages
async def start(update: Update, context: CallbackContext):
    try:
        # Send the first message with the link clearly visible
        first_message = await update.message.reply_text(
            FIRST_MESSAGE,
            disable_web_page_preview=True
        )

        # Save the timestamp of when the first message was sent
        message_times[update.message.chat_id] = {
            "messages": [first_message.message_id],
            "user_messages": [update.message.message_id],  # Store the user's first message ID
            "timestamps": {
                first_message.message_id: time.time(),
                update.message.message_id: time.time()
            }
        }

        # Wait 20 seconds before sending the second message
        await asyncio.sleep(20)

        # Send the second message
        second_message = await update.message.reply_text(SECOND_MESSAGE)
        message_times[update.message.chat_id]["messages"].append(second_message.message_id)
        message_times[update.message.chat_id]["timestamps"][second_message.message_id] = time.time()

        # Wait another 20 seconds before sending the last message
        await asyncio.sleep(20)

        # Send the last message (reward link)
        last_message = await update.message.reply_text(LAST_MESSAGE)
        message_times[update.message.chat_id]["messages"].append(last_message.message_id)
        message_times[update.message.chat_id]["timestamps"][last_message.message_id] = time.time()

    except Exception as e:
        handle_error(e, "Error occurred in start function")

# Function to delete messages after 20 seconds
async def delete_old_messages():
    while True:
        current_time = time.time()
        for chat_id, data in message_times.items():
            # Check each message's timestamp individually
            for message_id, timestamp in data["timestamps"].items():
                if current_time - timestamp >= 20:  # 20 seconds after the message is sent
                    try:
                        # Delete the user's message
                        if message_id in data["user_messages"]:
                            await app.bot.delete_message(chat_id, message_id)
                            print(f"Deleted user's message {message_id} for chat_id {chat_id}")

                        # Delete the bot's message
                        elif message_id in data["messages"]:
                            await app.bot.delete_message(chat_id, message_id)
                            print(f"Deleted bot's message {message_id} for chat_id {chat_id}")

                        # Remove the message from the tracking list
                        del data["timestamps"][message_id]
                    
                    except Exception as e:
                        handle_error(e, f"Failed to delete message {message_id} for chat_id {chat_id}")

            # Clean up once all messages are deleted
            if not data["timestamps"]:
                del message_times[chat_id]

        # Check every 5 seconds
        await asyncio.sleep(5)

async def main():
    try:
        # Create the Application and pass the bot token
        global app
        app = Application.builder().token(TOKEN).build()

        # Add command handler for /start
        app.add_handler(CommandHandler("start", start))

        # Start the polling
        asyncio.create_task(delete_old_messages())  # Start the background task for deleting old messages
        await app.run_polling()  # Start the polling to listen for updates

    except Exception as e:
        handle_error(e, "Error occurred in main function")

# This part will be executed when the script is run
if __name__ == "__main__":
    try:
        nest_asyncio.apply()  # Apply nest_asyncio to allow nested event loops
        asyncio.run(main())  # Properly run the async main function
    except Exception as e:
        handle_error(e, "Error occurred while running the bot")
