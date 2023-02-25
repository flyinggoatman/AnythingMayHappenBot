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

SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, TOKEN = env_pull()

# create an engine to connect to the database




# create a session to execute queries
allowed_channels = [int(DISCORD_CHANNEL_ID)]

@bot.event
async def on_ready():
    print("Bot is running")
    
@bot.event
async def on_message(message):
    guild_id = message.guild.id
    author = message.author
    mention = author.mention
    discord_name = author.name
    if message.author == bot.user:
        return
    
    
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
                await message.channel.send(f"{message.content} added successfully!")
                print(f"Link {message.content} added successfully!")
            else: 
                await message.channel.send(f"{message.content} is already in the database {mention}.", delete_after=10)
                await message.delete()
                print(f"{message.content} is already in the database.")


bot.run(TOKEN)
