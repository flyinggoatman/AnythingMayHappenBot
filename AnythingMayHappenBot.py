import mysql.connector
import discord
from discord.ext import commands
import re
from functions import mysql_push, env_pull

#Discord Bot Setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='! ', intents=intents)
# Discord bot token


SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, TOKEN = env_pull()

    # Create a connection to the database
cnx = mysql.connector.connect(
    host=SQL_HOST,
    user=SQL_USER,
    password=SQL_PASS,
    database=SQL_DATABASE
)

# Create a cursor object
cursor = cnx.cursor()


@bot.event
async def on_ready():
    print("Bot is running")
@bot.event
async def on_message(message):
    guild_id = message.guild.id
    author = message.author
    mention = author.mention
    if message.author == bot.user:
        return
    
    DISCORD_CHANNEL_ID_int = int(DISCORD_CHANNEL_ID)
    if DISCORD_CHANNEL_ID_int == message.channel.id:
        link = message.content
        # check if the link is a valid URL
        match = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', link)
        if match:
            query = "SELECT * FROM link WHERE link = %s"
            cursor.execute(query, (link,))
            result = cursor.fetchone()
        
        
        
        
            if result:
                link = mysql_push(cnx, cursor, link)
                await message.delete()
                
                if match:
                    await message.channel.send(f"Link {message.content} added successfully!")
                    print(f"Link {message.content} added successfully!")
                else:
                    await message.channel.send(f"Invalid link. Please enter a valid URL.\n{message.content}")
                    print(f"Invalid link. Please enter a valid URL.\n{message.content}")
            else: 
                await message.channel.send(f"{link} is already in the database {mention}.", delete_after=10)
                await message.delete()
                print(f"{link} is already in the database.")

bot.run(TOKEN)















