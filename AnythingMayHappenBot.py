import mysql.connector
from decouple import config
import discord
from discord.ext import commands
import re

# Discord bot token


# MySQL login information
SQL_HOST_2 = config('SQL_HOST_2', default='localhost')
SQL_USER_2 = config('SQL_USER_2') or ''
SQL_PASS_2 = config('SQL_PASS_2') or ''
SQL_DATABASE_2 = config('SQL_DATABASE_2') or ''
TOKEN = config('TOKEN', str)

# Create a connection to the database
cnx = mysql.connector.connect(
    host=SQL_HOST_2,
    user=SQL_USER_2,
    password=SQL_PASS_2,
    database=SQL_DATABASE_2
)

# Create a cursor object
cursor = cnx.cursor()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='! ', intents=intents)
@bot.event
async def on_ready():
    print("Bot is running")
@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return
    link = message.content
    # check if the link is a valid URL
    match = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', link)
    if match:
        # Remove "http://" or "https://" from the link if it exists
        link = link.replace("http://", "").replace("https://", "")

        # Insert a new row into the "link" table
        query = "INSERT INTO link (link, title, description, pict) VALUES (%s, %s, %s, %s)"
        values = (link, None, None, None)
        cursor.execute(query, values)

        # Commit the changes
        cnx.commit()
        await message.channel.send(f"Link {message.content} added successfully!")
    else:
        await message.channel.send(f"Invalid link. Please enter a valid URL. {message.content}")

bot.run(TOKEN)















