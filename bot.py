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
            },

            "extra": {
                "beg_counter": 0
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

@bot.tree.command(name="beg", description="beg to earn some cash (you can only use this command 5 times)")
async def beg(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user_beg_counter = int(data['saved_users'][user_id]['extra']['beg_counter'])

    print("")
    print("|----- Log -----|")
    print(f"{GREEN} USER ID: {user_id}")
    print("")

    not_added_embed = discord.Embed(
        title="Not found",
        description="It seems that your not in the saved users json file \n try running /add_me",
        color=discord.Color.red()
    )

    max_beg_reached_embed = discord.Embed(
        title="Stop begging",
        description="No way your that desperate for money \n get your money up not your funny up and **stop begging**",
        color=discord.Color.blurple()
    )

    if user_id not in data['saved_users']:
        await interaction.response.send_message(embed=not_added_embed)
    elif user_id in data['saved_users']:

        #? LOG
        print("USER IS ADDED")
        print(f"USER BEG COUNT: {user_beg_counter}")

        if user_beg_counter < 5:
            from functions.beg_function import beg
            beg_income = beg()
            print(f"{GREEN}BEG INCOME: {beg_income}")


            #TODO SETTING EMBED
            beg_result_embed = discord.Embed(
                title="**Lucky Duck**",
                description=f"A kind person named woniw decided to give you {beg_income} wibucks \n (dont spend it all at once😉)",
                color=discord.Color.green()
            )
            beg_result_embed.set_author(name="winow luck servers")        
            beg_result_embed.set_image(url="https://i.pinimg.com/736x/9e/03/87/9e0387462d886aefa9089ce644f95fc1--money-emoji-kanker.jpg")


            #! json function
            data['saved_users'][user_id]['extra']['beg_counter'] = data['saved_users'][user_id]['extra']['beg_counter'] + 1
            data["saved_users"][user_id]['money'] = data["saved_users"][user_id]['money'] + beg_income
            from static.variables import data_path
            save_json(data_path, data)

            await interaction.response.send_message(embed=beg_result_embed)

        elif data['saved_users'][user_id]['extra']['beg_counter'] <= 5:
            await interaction.response.send_message(embed=max_beg_reached_embed)

if __name__ == "__main__":
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found in environment variables.")
    else:
        bot.run(TOKEN)
