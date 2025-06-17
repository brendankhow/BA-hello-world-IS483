import os
import csv
import asyncio
import time
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import FloodWaitError

# Load environment variables from the .env file
load_dotenv()

# Get Telegram API credentials and channel details from the environment
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")
channel = os.getenv("TELEGRAM_CHANNEL")

# Initialize Telegram client
client = TelegramClient("smu_confess_session", api_id, api_hash)

async def fetch_channel_posts():
    # Start the Telegram client
    await client.start(phone=phone)
    
    # Resolve the channel entity
    ch = await client.get_entity(channel)
    print(f"Channel '{ch.title}' resolved (ID {ch.id})")

    posts = []  # List to store all the fetched posts
    last_id = 0  # Keep track of the last post ID for pagination
    fetch_count = 0  # Counter to track how many times we fetch posts

    while True:
        try:
            fetch_count += 1
            print(f"\nFetching batch {fetch_count}...")

            # Fetch posts from the channel using GetHistoryRequest
            hist = await client(GetHistoryRequest(
                peer=ch,
                limit=200,   # Number of posts to fetch per request
                offset_id=last_id,   # Use last_id for pagination
                offset_date=None,    # Keep the offset date as None
                add_offset=0,        # Default value to prevent errors
                max_id=0,            # Default value to prevent errors
                min_id=0,            # Default value to prevent errors
                hash=0               # Default value to prevent errors
            ))

            msgs = hist.messages  # List of messages fetched
            if not msgs:
                print("No more posts found.")
                break  # Exit loop if no more messages are found

            print(f"Fetched {len(msgs)} posts in this batch.")
            
            # Process each message
            for msg in msgs:
                if not msg.message:
                    continue

                text = msg.message.replace("\n", " ")  # Sanitize newline characters

                posts.append({
                    "post_id": msg.id,
                    "timestamp": msg.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "sender_id": msg.sender_id or "",
                    "text": text,
                    "reply_to_msg_id": msg.reply_to_msg_id or ""
                })

            # Update last_id to continue fetching older posts in the next iteration
            last_id = msgs[-1].id
            print(f"Last ID updated to {last_id}")

            # Add a short delay to avoid hitting rate limits
            time.sleep(1)

        except FloodWaitError as e:
            print(f"Rate limit hit, sleeping for {e.seconds} seconds...")
            time.sleep(e.seconds)

    # Save the fetched posts to a CSV file
    await save_to_csv(posts)

async def save_to_csv(posts):
    # Define the CSV field names
    chan_fields = ["post_id", "timestamp", "sender_id", "text", "reply_to_msg_id"]

    # Write the posts to a CSV file
    with open("channel_posts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(chan_fields)  # Write header row
        for row in posts:
            writer.writerow([row[k] for k in chan_fields])

    print(f"✅ Saved channel_posts.csv ({len(posts)} posts)")

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(fetch_channel_posts())
