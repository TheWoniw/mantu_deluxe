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
    print("|----- Log -----|")
    print(f"{GREEN} USER ID: {user_id}")
    print("")

    already_added_embed = discord.Embed(
        title="‼️Already Added‼️",
        description="Your already added, stop making woniw write more code for error handling",
        color=discord.Color.red()
    )
    if user_id in data['saved_users']:
        await interaction.response.send_message(embed=already_added_embed)

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

@bot.tree.command(name="resources")
async def resources(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    print("")
    print("|----- Log -----|")
    print(f"{GREEN} USER ID: {user_id}")
    print("")

    if user_id in data['saved_users']:
        #? resource variables
        #data['saved_users'][user_id]['ingredients']['']
        balance = data['saved_users'][user_id]['money']
        flour = data['saved_users'][user_id]['ingredients']['flour']
        water = data['saved_users'][user_id]['ingredients']['water']
        yogurt = data['saved_users'][user_id]['ingredients']['yogurt']
        meat = data['saved_users'][user_id]['ingredients']['meat']


        resource_embed = discord.Embed(
            title="**RESOURCES**",
            description=f"Balance: **{balance}** \n Flour: {flour} \n Water: {water} \n Yogurt: {yogurt} \n Meat: {meat}",
            color=discord.Color.green(),  
        ) 

        resource_embed.set_image(url="https://cdn-icons-png.flaticon.com/512/4241/4241664.png")
        resource_embed.set_author(name="winow resource facility")

        not_added_embed = discord.Embed(
            title="Not found",
            description="It seems that your not in the saved users json file \n try running /add_me",
            color=discord.Color.red()
        )

        await interaction.response.send_message(embed=resource_embed)

    elif user_id not in data['saved_users']:
        print(f"{RED}USER IS NOT ADDED")
        await interaction.response.send_message(embed=not_added_embed)

@bot.tree.command(name="skill_level")
async def skill_level(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    print("")
    print("|----- Log -----|")
    print(f"{GREEN} USER ID: {user_id}")
    print("")


    if user_id in data['saved_users']:
        pass
    elif user_id not in data["saved_users"]:
        pass

if __name__ == "__main__":
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found in environment variables.")
    else:
        bot.run(TOKEN)
