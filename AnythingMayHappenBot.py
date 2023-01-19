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
engine = create_engine(f'mysql://{SQL_USER}:{SQL_PASS}@{SQL_HOST}/{SQL_DATABASE}')


Base = declarative_base()
class Link(Base):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True)
    link = Column(String)
Base.metadata.create_all(engine)



# create a session to execute queries
Session = sessionmaker(bind=engine)
session = Session()

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
        url = link
        link = link.replace("https://", "")
        if match:
            result = session.query(Link).filter_by(link=link).first()
            if not result:
                
                new_link = Link(link=link)
                session.add(new_link)
                session.commit()
                await message.delete()
                await message.channel.send(f"Link {message.content} added successfully!")
                print(f"Link {message.content} added successfully!")
            else: 
                await message.channel.send(f"{message.content} is already in the database {mention}.", delete_after=10)
                await message.delete()
                print(f"{message.content} is already in the database.")

bot.run(TOKEN)
