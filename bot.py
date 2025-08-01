import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands

from data_storage.json_functions import save_json

#? static imports\
from static.variables import data
from static.variables import RED
from static.variables import GREEN

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        await bot.tree.sync()
        print("Slash commands synced!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

#! run data
print(f"{RED}{data}")

@bot.tree.command(name="add_me")
async def add_me(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    print("")
    print("|----- Log -----")
    print(f"{GREEN} USER ID: {user_id}")
    print("")

    if user_id in data['saved_users']:
        await interaction.response.send_message("you are already added")
    elif user_id not in data['saved_users']:
        #! adding user
        data["saved_users"][user_id] = {
            "money": 0,

            "ingredients":{
                "flour": 0,
                "water": 0,
                "yogurt": 0,
                "meat": 0,
            },
            
            'equipment': {
                "oven": "regular oven",
            },

            "skill": {
                "dough handling xp": 0,
                "dough handling": 1
            }
        }
        from static.variables import data_path
        save_json(data_path, data)

        print("")
        print("|----- Log -----")
        print(f"user:{user_id} has been added to the json database ")
        print("")

        await interaction.response.send_message(f"Welcome {interaction.user.mention}")

if __name__ == "__main__":
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found in environment variables.")
    else:
        bot.run(TOKEN)
