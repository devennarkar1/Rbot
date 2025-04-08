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

SECOND_MESSAGE = (
    "🎯 Ready for the reward?\n"
    "🎁 Here’s your exclusive link:\n\n\n"
    "👉 https://t.me/+z0oxXjImMvg1NmNl\n\n\n"
    "😎 Enjoy!"
)  # New second message with the link

# Dictionary to track messages by user
message_times = {}

# This function will send the first, second, and third messages
async def start(update: Update, context: CallbackContext):
    try:
        # Send the first message with the link clearly visible
        message = await update.message.reply_text(
            "🚨 **Want the link?**\n\n\n\n"
            "🎥 Just watch the video for *90 seconds* ⏱️ And hit  SUBSCRIBE Button 🔔.\n\n\n\n"
            "👇👇👇\n"
            "👉 [Watch here!](https://youtu.be/oeenz5JTaoo) 😎\n\n\n"
            "After that, You Will Get LINK!",
            disable_web_page_preview=True
        )
        
        # Save the timestamp of when the first message was sent
        message_times[update.message.chat_id] = {
            "first_message_time": time.time(),
            "messages": [message.message_id]
        }

        # Store the user's initial /start message ID for deletion
        user_start_message_id = update.message.message_id
        message_times[update.message.chat_id]["user_start_message_id"] = user_start_message_id

        # Wait for 5 seconds
        await asyncio.sleep(2)

        # Send the second message after 5 seconds (reminder to hang tight)
        message = await update.message.reply_text("⏳ Click the link To Get Link")

        # Wait for 5 seconds
        await asyncio.sleep(2)

        # Send the second message after 5 seconds (reminder to hang tight)
        message = await update.message.reply_text("⏳ Click the link To Get Link")

        # Wait for 5 seconds
        await asyncio.sleep(4)

        # Send the second message after 5 seconds (reminder to hang tight)
        message = await update.message.reply_text("⏳ 40 sec Left ")

        # Wait for 5 seconds
        await asyncio.sleep(2)

        # Send the second message after 5 seconds (reminder to hang tight)
        message = await update.message.reply_text("⏳ 20 sec Left ")

        # Wait for 5 seconds
        await asyncio.sleep(1)

        # Send the second message after 5 seconds (reminder to hang tight)
        message = await update.message.reply_text("⏳ 10 sec Left ")

        # Store the message ID for deletion later
        message_times[update.message.chat_id]["messages"].append(message.message_id)

        # Wait for 85 more seconds (total 90 seconds)
        await asyncio.sleep(3)

        # Send the third message after 90 seconds (the reward link)
        message = await update.message.reply_text(SECOND_MESSAGE)

        # Store the message ID for deletion later
        message_times[update.message.chat_id]["messages"].append(message.message_id)

    except Exception as e:
        print(f"Error occurred in start: {e}")

# Function to delete messages after 110 seconds
async def delete_old_messages():
    while True:
        current_time = time.time()
        for chat_id, data in message_times.items():
            first_message_time = data["first_message_time"]
            if current_time - first_message_time >= 110:  # 110 seconds
                try:
                    # Delete the user's initial /start message
                    user_start_message_id = data.get("user_start_message_id")
                    if user_start_message_id:
                        await app.bot.delete_message(chat_id, user_start_message_id)
                        print(f"Deleted start message {user_start_message_id}")
                
                    # Delete all messages associated with this user
                    for message_id in data["messages"]:
                        await app.bot.delete_message(chat_id, message_id)
                        print(f"Deleted message {message_id}")

                    # Remove the entry for this user after deleting messages
                    del message_times[chat_id]

                except Exception as e:
                    print(f"Failed to delete messages for chat_id {chat_id}: {e}")

        # Check every minute
        await asyncio.sleep(60)

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
        print(f"Error occurred in main: {e}")

# This part will be executed when the script is run
if __name__ == "__main__":
    try:
        nest_asyncio.apply()  # Apply nest_asyncio to allow nested event loops
        asyncio.run(main())  # Properly run the async main function
    except Exception as e:
        print(f"Error occurred while running the bot: {e}")
