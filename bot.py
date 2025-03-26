import discord
from discord.ext import commands
import json
import os

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# File paths for storage
ACCOUNTS_MAPPING_FILE = "accounts.json"  # Internal mapping: discord_user_id -> X account
X_ACCOUNTS_FILE = "x_accounts_list.txt"    # Public list: one X account per line

# Load existing mapping if available; otherwise initialize an empty dictionary.
if os.path.exists(ACCOUNTS_MAPPING_FILE):
    with open(ACCOUNTS_MAPPING_FILE, "r") as f:
        accounts = json.load(f)
else:
    accounts = {}

# Helper function: Update the public list file
def update_x_accounts_file():
    with open(X_ACCOUNTS_FILE, "w") as f:
        for x_account in accounts.values():
            f.write(x_account + "\n")

# Set up Discord bot intents (make sure "Message Content Intent" is enabled in the developer portal)
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with a command prefix (e.g., "!")
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Command for users to set their X account handle
@bot.command(name="setaccount")
async def set_account(ctx, account: str):
    user_id = str(ctx.author.id)

    # Check if this Discord user has already submitted an account.
    if user_id in accounts:
        await ctx.send("You have already set your X account handle!")
        return

    # Check if the account already exists in the list to prevent duplicates.
    if account in accounts.values():
        await ctx.send("This X account is already registered by another user!")
        return

    # Save the new account and update both files.
    accounts[user_id] = account
    with open(ACCOUNTS_MAPPING_FILE, "w") as f:
        json.dump(accounts, f)
    update_x_accounts_file()

    await ctx.send(f"Your X account handle '{account}' has been registered.")

# Optional: Command to check the public X accounts list (for admin purposes only, for example)
@bot.command(name="listaccounts")
async def list_accounts(ctx):
    if os.path.exists(X_ACCOUNTS_FILE):
        with open(X_ACCOUNTS_FILE, "r") as f:
            content = f.read()
        await ctx.send("**Registered X Accounts:**\n" + content)
    else:
        await ctx.send("No accounts have been registered yet.")

# Run the bot (replace "YOUR_BOT_TOKEN" with your actual bot token)
bot.run(DISCORD_BOT_TOKEN)
