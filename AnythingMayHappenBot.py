from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import discord
from discord.ext import commands
import re
from functions import mysql_push, env_pull, DEBUG_MESSAGE, add_new_link
from sqlalchemy.ext.declarative import declarative_base

#Discord Bot Setup
intents = discord.Intents.all() #Defines the intents for the bot
client = discord.Client(intents=intents) #Defines the client for the bot
bot = commands.Bot(command_prefix='! ', intents=intents) #Defines the bot itself

#SQLAlchemy Setup
Base = declarative_base()



def env_use():
    SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN = env_pull()
    return SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN



SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN = env_use()
# create an engine to connect to the database


# List of channels where the bot is allowed to send messages
allowed_channels = [int(DISCORD_CHANNEL_ID), int(ALL_CATEGORIES_CHANNEL_ID), int(SUBREDDIT_CHANNEL), int(EXTENSION_CHANNEL), int(VIDEOS_CHANNEL), int(PHONE_APPS_CHANNEL), int(GITHUB_CHANNEL), int(BLENDER_ADDONS_CHANNEL), int(EBOOKS_PDF_CHANNEL), int(AI_WEBSITE_CHANNEL), int(SOFTWARE_CHANNEL), int(VIDEO_GAMES_CHANNEL)]

@bot.event
async def on_ready():
    SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID_int, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN = env_use()


    print(f"Bots name: {bot.user.name}")
    print(f"Bots ID: {bot.user.id}")
    DEBUG_MESSAGE(SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID_int, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN)

classified_user = HIDDEN_USERS
print(classified_user)

@bot.event
async def on_message(message):
    
    guild_id = message.guild.id
    author = message.author
    mention = author.mention
    print(f"Author: {author}")
    discord_name = author.name
    print(f"Discord name: {discord_name}")
    
    if message.author == bot.user:
        print("Bot message detected. Ignoring...")
        return
    SUBREDDIT_CHANNEL_int = int(SUBREDDIT_CHANNEL)
    EXTENSION_CHANNEL_int = int(EXTENSION_CHANNEL)
    VIDEOS_CHANNEL_int = int(VIDEOS_CHANNEL)
    PHONE_APPS_CHANNEL_int = int(PHONE_APPS_CHANNEL)
    GITHUB_CHANNEL_int = int(GITHUB_CHANNEL)
    BLENDER_ADDONS_CHANNEL_int = int(BLENDER_ADDONS_CHANNEL)
    EBOOKS_PDF_CHANNEL_int = int(EBOOKS_PDF_CHANNEL)
    VIDEOS_CHANNEL_int = int(VIDEOS_CHANNEL)
    VIDEO_GAMES_CHANNEL_int = int(VIDEO_GAMES_CHANNEL)
    AI_WEBSITE_CHANNEL_int = int(AI_WEBSITE_CHANNEL)
    SOFTWARE_CHANNEL_int = int(SOFTWARE_CHANNEL)
    ALL_CATEGORIES_CHANNEL_ID_int = int(ALL_CATEGORIES_CHANNEL_ID)
    
    
    DISCORD_CHANNEL_ID_int = int(DISCORD_CHANNEL_ID)
    if message.content.startswith("!setchannel"):
        channel_id = int(message.content.split()[1])
        allowed_channels.append(channel_id)
        
        await message.channel.send(f"Channel with ID {channel_id} has been added to the list of allowed channels.")
    elif message.channel.id in allowed_channels:
        #delete message
        ##try loop that tries 3 times to connect to the database
        for i in range(3):
            try:
                print("Trying to connect to the database...")
                engine = create_engine(f"mysql+pymysql://{SQL_USER}:{SQL_PASS}@{SQL_HOST}/{SQL_DATABASE}")
                break
            except:
                print("Database connection failed. Trying again...")
                continue
        else:
            print("Database connection failed. Exiting...")
            return
        


        Base = declarative_base()
        class Link(Base):
            __tablename__ = 'link'
            id = Column(Integer, primary_key=True)
            link = Column(String)
        Base.metadata.create_all(engine)
        if re.search('http://', message.content) or re.search('https://', message.content):
            await message.delete()  
        
        Session = sessionmaker(bind=engine)
        session = Session()
        link = message.content
        if message.content.startswith('!delete'):
            
            command_tag = message.content.split()[0]
            url = message.content.split()[1]
            link = message.content.split()[1]
            link = re.sub(r'http://', '', link)
            link = re.sub(r'https://', '', link)
            link = re.sub(r'&hl=[^&]*', '', url)
            link = re.sub(r'&gl=[^&]*', '', url)
                
            link = link.replace("http://", "").replace("https://", "")
            
            print(link)
            result = session.query(Link).filter_by(link=link).first()
            if not result:
                await message.channel.send(f"{url} is **not present** in the database {mention}.",delete_after=5)
                print(f"{url} is not present in the database {discord_name}.")
            else:
                session.delete(result)
                session.commit()
                await message.channel.send(f"{url} has been **removed** from the database {mention}.",delete_after=5)
                print(f"{url} has been **removed** from the database {discord_name}.")
        elif message.content.startswith('!ignore'):
            await message.delete()
            command_tag = message.content.split()[0]
            link = message.content.split()[1]
            link = re.sub(r'&hl=[^&]*', '', url)
            link = re.sub(r'&gl=[^&]*', '', url)
        elif message.content.startswith('!e'):
            command_tag = message.content.split()[0]
            link = message.content.split()[1]
            link = re.sub(r'http://', '', link)
            link = re.sub(r'https://', '', link)
        elif message.content.startswith('!app'):
            command_tag = message.content.split()[0]
            link = message.content.split()[1]
            link = re.sub(r'http://', '', link)
            link = re.sub(r'https://', '', link)    
            print("command_tag:" + command_tag)
            
            
            
            result = session.query(Link).filter_by(link=link).first()
        else:
            command_tag = ""
        # check if the link is a valid URL
        
        # link = re.sub(r'http://', '', link)
        # link = re.sub(r'https://', '', link)
        # link = link.replace("www.", "")
        # link = re.sub(r'&hl=[^&]*', '', link)
        # link = re.sub(r'&gl=[^&]*', '', link)
        print(f"Link: {link}")
        match = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', link)
        match_2 = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]+\.[a-zA-Z0-9()]{2,6}[/a-zA-Z0-9._?=\-&]+', link)
        url = link
        link = link.replace("http://", "").replace("https://", "")
        

        if match or match_2:
            result = session.query(Link).filter_by(link=link).first()
            if not result:
                if command_tag == "!delete":
                    return
                
                link = link.replace("http://", "").replace("https://", "")
                new_link = Link(link=link)
                session.add(new_link)
                session.commit()
                await add_new_link(link, session, Link, message, bot, DEBUG_MODE, command_tag, url, author, DISCORD_CHANNEL_ID_int, GITHUB_CHANNEL_int, BLENDER_ADDONS_CHANNEL_int, ALL_CATEGORIES_CHANNEL_ID_int, classified_user, PHONE_APPS_CHANNEL_int, VIDEOS_CHANNEL_int, EXTENSION_CHANNEL_int, SUBREDDIT_CHANNEL_int, EBOOKS_PDF_CHANNEL_int, VIDEO_GAMES_CHANNEL_int, AI_WEBSITE_CHANNEL_int, SOFTWARE_CHANNEL_int, mention, discord_name)
                    
            else: 
                
                target_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
                if author.id in classified_user:
                    await target_channel.send(f"{url} is already in the database **user classified**.",delete_after=5)
                else:    
                    await target_channel.send(f"{url} is already in the database {mention}.",delete_after=5)
                print(f"{url} is already in the database.")





bot.run(TOKEN)
