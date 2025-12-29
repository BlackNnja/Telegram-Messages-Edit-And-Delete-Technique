import asyncio
from telethon import TelegramClient, errors

# --- CONFIGURATION --- https://my.telegram.org
API_ID = 'YOUR_API_ID' 
API_HASH = 'YOUR_API_HASH'
# ---------------------

async def run_cleaner():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start()
    
    # Fetch dialogs
    print("Fetching chats...")
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if d.is_group or d.is_channel]

    for i, g in enumerate(groups):
        print(f"[{i}] {g.name}")

    choice = int(input("\nSelect Group Number: "))
    target = groups[choice]
    
    confirm = input(f"Wipe messages in {target.name}? (y/n): ")
    if confirm.lower() != 'y': return

    async for msg in client.iter_messages(target, from_user='me'):
        try:
            await msg.edit("*")
            await asyncio.sleep(0.3)
            await msg.delete()
            print(f"Deleted message {msg.id}", end="\r")
        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Error: {e}")

    print("\nDone!")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(run_cleaner())
