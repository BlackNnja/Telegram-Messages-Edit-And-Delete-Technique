# 🧹 Telegram Message Scrubber

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Telethon](https://img.shields.io/badge/telethon-1.36.0-orange.svg)

**A privacy-focused Python tool for securely wiping your Telegram message history**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security) • [FAQ](#-faq)

</div>

---

## 📖 Overview

Telegram Message Scrubber is a powerful Python utility that allows you to securely erase your digital footprint from Telegram groups and channels. Unlike standard message deletion, this tool implements a **two-step secure wipe process**: first overwriting each message with a `*` character to clear server-side content, then permanently deleting it.

This approach ensures that your original message content is purged from Telegram's database, providing an extra layer of privacy protection.

### 🎯 Use Cases

- **Privacy Management**: Remove old messages from groups you no longer participate in
- **Data Minimization**: Reduce your digital footprint across chat platforms
- **Account Cleanup**: Prepare accounts for archival or deletion
- **Security Hygiene**: Clear sensitive information from chat histories

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **User-Level Access** | Operates as a UserBot, allowing deletion even without admin privileges |
| 🎯 **Smart Overwrite** | Edits messages to `*` before deletion to ensure content is scrubbed from server logs |
| 📋 **Interactive Menu** | Displays all your groups and channels in an easy-to-navigate interface |
| ⚡ **Rate Limit Protection** | Automatically handles Telegram's `FloodWaitError` to prevent account restrictions |
| 📊 **Real-time Progress** | Visual feedback showing deletion count and message IDs |
| 🛡️ **Safe & Selective** | Choose exactly which group to clean with confirmation prompts |

---

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **Telegram Account**
- **API Credentials** from Telegram

### Step 1: Obtain Telegram API Credentials

1. Visit [my.telegram.org](https://my.telegram.org) and log in
2. Navigate to **API development tools**
3. Create a new application (you can name it "Message Scrubber")
4. Save your `api_id` and `api_hash` - you'll need these later

### Step 2: Clone and Setup

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/telegram-message-scrubber.git
cd telegram-message-scrubber

# Install dependencies
pip install -r req.py
```

### Step 3: Configure API Credentials

Open `script.py` and replace the placeholder values:

```python
API_ID = 'YOUR_API_ID'      # Replace with your actual API ID
API_HASH = 'YOUR_API_HASH'  # Replace with your actual API Hash
```

**💡 Pro Tip**: For better security, use environment variables instead of hardcoding credentials.

---

## 📂 Project Structure

```
telegram-message-scrubber/
├── script.py              # Main application script
├── req.py     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Core Files

#### `script.py` - Main Application Script

```python
import asyncio
import sys
from telethon import TelegramClient, errors

# --- CONFIGURATION ---
API_ID = 'YOUR_API_ID' 
API_HASH = 'YOUR_API_HASH'
# ---------------------

async def run_scrubber():
    client = TelegramClient('privacy_session', API_ID, API_HASH)
    
    try:
        await client.start()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    me = await client.get_me()
    print(f"\n✅ Authenticated as: {me.first_name} (@{me.username or 'No Username'})")

    print("\n[1] Fetching active chats...")
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if d.is_group or d.is_channel]

    if not groups:
        print("⚠️  No groups or channels found.")
        return

    print("\n" + "═"*50)
    print(f"{'Index':<8} | {'Group Name'}")
    print("─"*50)
    for i, g in enumerate(groups):
        print(f"[{i:<6}] | {g.name[:35]}")
    print("═"*50)

    try:
        choice = int(input("\n🎯 Select the index number to scrub: "))
        target = groups[choice]
    except (ValueError, IndexError):
        print("❌ Error: Invalid selection.")
        return

    print(f"\n⚠️  CRITICAL WARNING")
    print(f"━"*50)
    print(f"Target: {target.name}")
    print(f"Action: OVERWRITE + DELETE all your messages")
    print(f"━"*50)
    confirm = input("\n⚠️  Type 'YES' to proceed (case-sensitive): ")
    
    if confirm != "YES":
        print("✋ Operation cancelled.")
        return

    print(f"\n🚀 Starting secure wipe on '{target.name}'...\n")
    count = 0
    
    async for msg in client.iter_messages(target, from_user='me'):
        try:
            # Step 1: Overwrite original content
            await msg.edit("*")
            await asyncio.sleep(0.35)  # Delay to avoid rate limits
            
            # Step 2: Delete message permanently
            await msg.delete()
            
            count += 1
            sys.stdout.write(f"\r🧹 Messages Scrubbed: {count}")
            sys.stdout.flush()
            
        except errors.FloodWaitError as e:
            print(f"\n⏳ Rate limit detected. Pausing for {e.seconds}s...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"\n⚠️  Error processing message {msg.id}: {e}")

    print(f"\n\n✅ Mission Accomplished! {count} messages successfully removed.")
    await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(run_scrubber())
    except KeyboardInterrupt:
        print("\n\n🛑 Script stopped by user.")
```

#### `req.py` - Dependencies

```
telethon==1.36.0
```

#### `.gitignore` - Security Protection

```
# Session files (contain authentication tokens)
*.session
*.session-journal

# Python cache
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
env/
ENV/

# Environment variables
.env

# IDE files
.vscode/
.idea/
*.swp
*.swo
```

---

## 🎮 Usage

### Running the Script

```bash
python script.py
```

### Step-by-Step Process

1. **Authentication**
   - Enter your phone number (with country code, e.g., `+1234567890`)
   - Enter the verification code sent to your Telegram app
   - A `.session` file will be created for future use

2. **Group Selection**
   - Review the list of your groups and channels
   - Enter the index number of your target group

3. **Confirmation**
   - Read the warning carefully
   - Type `YES` (case-sensitive) to proceed

4. **Execution**
   - Watch the real-time progress counter
   - The script will automatically handle rate limits

5. **Completion**
   - Review the final count of deleted messages
   - The script will disconnect automatically

### Example Session

```
✅ Authenticated as: John Doe (@johndoe)

[1] Fetching active chats...

══════════════════════════════════════════════════
Index    | Group Name
──────────────────────────────────────────────────
[0     ] | Old Project Team
[1     ] | Gaming Squad 2023
[2     ] | Study Group - History
══════════════════════════════════════════════════

🎯 Select the index number to scrub: 1

⚠️  CRITICAL WARNING
──────────────────────────────────────────────────
Target: Gaming Squad 2023
Action: OVERWRITE + DELETE all your messages
──────────────────────────────────────────────────

⚠️  Type 'YES' to proceed (case-sensitive): YES

🚀 Starting secure wipe on 'Gaming Squad 2023'...

🧹 Messages Scrubbed: 247

✅ Mission Accomplished! 247 messages successfully removed.
```

---

## 🛡️ Security & Best Practices

### Why the Two-Step Process?

**Step 1: Overwrite** - Telegram's servers may retain edit history for administrative purposes. By editing to `*`, we ensure that any retained logs show only the redacted character.

**Step 2: Delete** - Permanently removes the message from the visible chat and database.

### Critical Security Notes

⚠️ **Session File Protection**
- The `.session` file contains your authentication tokens
- Treat it like a password - never share or upload it
- The included `.gitignore` prevents accidental commits

⚠️ **Rate Limiting**
- Telegram monitors for automated behavior
- The built-in 0.35s delay mimics human interaction
- **Do not decrease** this delay or risk temporary account restrictions

⚠️ **Irreversibility**
- Once deleted, messages **cannot be recovered**
- Always double-check your group selection
- Consider exporting important data before bulk deletion

### Permission Requirements

- **Groups**: You can delete your own messages in any group
- **Channels**: Depends on channel settings (usually 48-hour edit window)
- **Supergroups**: May have time-based restrictions on message editing

---

## 🔧 Advanced Configuration

### Using Environment Variables (Recommended)

Create a `.env` file:

```bash
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=abcdef1234567890
```

Modify `script.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
```

Add to `req.py`:
```
python-dotenv==1.0.0
```

### Custom Delay Settings

To adjust the rate limit delay, modify line 67 in `script.py`:

```python
await asyncio.sleep(0.35)  # Default: 0.35 seconds
```

**Recommended range**: 0.3 - 0.5 seconds

---

## ❓ FAQ

**Q: Will this delete messages in private chats?**  
A: No, the script only targets groups and channels. Private chats are excluded by design.

**Q: Can admins still see my deleted messages?**  
A: The overwrite method minimizes this risk, but Telegram may retain some metadata.

**Q: What happens if I lose internet connection?**  
A: The script will safely error out. Re-run it to continue from where it stopped.

**Q: Can I delete messages older than a specific date?**  
A: The current version deletes all your messages. Date filtering would require custom modifications.

**Q: Is this against Telegram's ToS?**  
A: This tool uses official APIs and operates within rate limits. However, review Telegram's terms yourself.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Feature Ideas

- [ ] Date range filtering
- [ ] Keyword-based selective deletion
- [ ] Multi-group batch processing
- [ ] Export chat history before deletion
- [ ] GUI interface

---

## 📜 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚖️ Disclaimer

This tool is provided for **educational purposes** and **personal privacy management** only. 

- Users are responsible for compliance with Telegram's Terms of Service
- The developers assume no liability for account restrictions or data loss
- Always ensure you have backups of important data before bulk operations
- This tool should be used ethically and responsibly

---

## 🌟 Acknowledgments

- Built with [Telethon](https://github.com/LonamiWebs/Telethon) - Python Telegram client library
- Inspired by privacy-first principles and digital minimalism
- Thanks to the open-source community for security best practices

---

## 📞 Support

If you encounter issues:

1. Check the [FAQ section](#-faq)
2. Review your API credentials
3. Ensure you're using Python 3.8+
4. Open an issue on GitHub with:
   - Error message
   - Python version
   - Operating system

---

<div align="center">

**⭐ If this tool helped you, consider giving it a star!**

Made with ❤️ for privacy-conscious users

</div>
