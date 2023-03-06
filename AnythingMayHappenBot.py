from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import discord
from discord.ext import commands
import re
from functions import mysql_push, env_pull
from sqlalchemy.ext.declarative import declarative_base

#Discord Bot Setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='! ', intents=intents)


def env_use():
    SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, DEBUG_MODE, SECRET_TOKEN = env_pull()
    return SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, DEBUG_MODE, SECRET_TOKEN

SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, DEBUG_MODE, SECRET_TOKEN = env_use()
# create an engine to connect to the database



# create a session to execute queries
allowed_channels = [int(DISCORD_CHANNEL_ID)]

@bot.event
async def on_ready():
    SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, DEBUG_MODE, SECRET_TOKEN = env_use()
    print(f"Bots name: {bot.user.name}")
    print(f"Bots ID: {bot.user.id}")
    print()
    print(DEBUG_MODE)
    DEBUG_MODE_STR = str(DEBUG_MODE)
    if DEBUG_MODE == True:
        print(f"{'##':#^150}\n{' DEBUG MODE IS ON ':#^150}\n{'##':#^150}")
        print(f"SQL_HOST: {SQL_HOST}")
        print(f"SQL_USER: {SQL_USER}")
        print(f"SQL_PASS: {SQL_PASS}")
        print(f"SQL_DATABASE: {SQL_DATABASE}")
        print(f"DISCORD_CHANNEL_ID: {DISCORD_CHANNEL_ID}")
        print(f"GUILD_ID: {GUILD_ID}")
        print(f"SUBREDDIT_CHANNEL: {SUBREDDIT_CHANNEL}")
        print(f"EXTENSION_CHANNEL: {EXTENSION_CHANNEL}")
        print(f"VIDEOS_CHANNEL: {VIDEOS_CHANNEL}")
        if SECRET_TOKEN == True:
            print(f"TOKEN: {TOKEN}")

    
@bot.event
async def on_message(message):
    guild_id = message.guild.id
    author = message.author
    mention = author.mention
    discord_name = author.name
    if message.author == bot.user:
        return
    SUBREDDIT_CHANNEL_int = int(SUBREDDIT_CHANNEL)
    EXTENSION_CHANNEL_int = int(EXTENSION_CHANNEL)
    VIDEOS_CHANNEL_int = int(VIDEOS_CHANNEL)
    
    
    DISCORD_CHANNEL_ID_int = int(DISCORD_CHANNEL_ID)
    if message.content.startswith("!setchannel"):
        channel_id = int(message.content.split()[1])
        allowed_channels.append(channel_id)
        
        await message.channel.send(f"Channel with ID {channel_id} has been added to the list of allowed channels.")
    elif message.channel.id in allowed_channels:
        
        
        engine = create_engine(f'mysql://{SQL_USER}:{SQL_PASS}@{SQL_HOST}/{SQL_DATABASE}')


        Base = declarative_base()
        class Link(Base):
            __tablename__ = 'link'
            id = Column(Integer, primary_key=True)
            link = Column(String)
        Base.metadata.create_all(engine)
        
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        link = message.content
        if message.content.startswith('!delete'):
            await message.delete()
            link = message.content.split()[1]
            link = link.replace("http://", "").replace("https://", "")
            result = session.query(Link).filter_by(link=link).first()
            if not result:
                await message.channel.send(f"{link} is not present in the database {mention}.", delete_after=10)
                print(f"{link} is not present in the database {discord_name}.")
            else:
                session.delete(result)
                session.commit()
                await message.channel.send(f"{link} has been removed from the database {mention}.", delete_after=10)
                print(f"{link} has been removed from the database {discord_name}.")

        
        # check if the link is a valid URL
        match = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', link)
        match_2 = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]+\.[a-zA-Z0-9()]{2,6}[/a-zA-Z0-9._?=\-&]+', link)
        url = link
        link = link.replace("http://", "").replace("https://", "")
        if match or match_2:
            result = session.query(Link).filter_by(link=link).first()
            if not result:
                new_link = Link(link=link)
                session.add(new_link)
                session.commit()
                await message.delete()
                if re.search(r'(chrome\.google\.com/webstore|addons\.mozilla\.org|microsoftedge\.microsoft\.com/addons/detail/|addons\.opera\.com/en/extensions/details/)', url):
                    
                    target_channel = bot.get_channel(EXTENSION_CHANNEL_int)
                    await target_channel.send(f"{url} added successfully by {author.display_name}!")
                elif re.search(r"reddit\.com/r/", url):
                    target_channel = bot.get_channel(SUBREDDIT_CHANNEL_int)
                    await target_channel.send(f"{url} added successfully by {author.display_name}!")
                    
                elif re.search(r'(\/watch\?v=|youtu\.be/)', url):
                    target_channel = bot.get_channel(VIDEOS_CHANNEL_int)
                    await target_channel.send(f"{url} added successfully by {author.display_name}!")
                else:
                    target_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
                    await target_channel.send(f"{url} added successfully by {author.display_name}!")
                    print(f"Link {url} added successfully!")
            else: 
                
                target_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
                await target_channel.send(f"{url} is already in the database {mention}.", delete_after=10)
                await message.delete()
                print(f"{url} is already in the database.")
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise



bot.run(TOKEN)
