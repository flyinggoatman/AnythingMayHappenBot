from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import discord
from discord.ext import commands
import re
from functions import mysql_push, env_pull, DEBUG_MESSAGE, add_new_link, connector_function, check_mysql_connection
from sqlalchemy.ext.declarative import declarative_base

# Discord Bot Setup
intents = discord.Intents.all()  # Defines the intents for the bot
client = discord.Client(intents=intents)  # Defines the client for the bot
bot = commands.Bot(command_prefix='! ', intents=intents)  # Defines the bot itself

# SQLAlchemy Setup
Base = declarative_base()


def env_use():
    SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN = env_pull()
    return SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN


SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN = env_use()



# List of channels where the bot is allowed to send messages
allowed_channels = [int(DISCORD_CHANNEL_ID), int(ALL_CATEGORIES_CHANNEL_ID), int(SUBREDDIT_CHANNEL), int(EXTENSION_CHANNEL), int(VIDEOS_CHANNEL), int(PHONE_APPS_CHANNEL), int(GITHUB_CHANNEL), int(BLENDER_ADDONS_CHANNEL), int(EBOOKS_PDF_CHANNEL), int(AI_WEBSITE_CHANNEL), int(SOFTWARE_CHANNEL), int(VIDEO_GAMES_CHANNEL)]


@bot.event
async def on_ready():
    SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID_int, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN = env_use()

    print("Bot is ready.")
    if DEBUG_MODE:
        print(f"Bots name: {bot.user.name}")
        print(f"Bots ID: {bot.user.id}")
    DEBUG_MESSAGE(SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID_int, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN)
    # Check MySQL connection during startup
    await check_mysql_connection(SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, bot)
classified_user = HIDDEN_USERS
print(classified_user)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        if DEBUG_MODE:
            print("Bot message detected. Ignoring...")
        return

    # Split the message into lines to handle multiple links
    lines = message.content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        command_tag = ""
        if line.startswith("!setchannel"):
            channel_id = int(line.split()[1])
            allowed_channels.append(channel_id)
            await message.channel.send(f"Channel with ID {channel_id} has been added to the list of allowed channels.")
            continue
        elif message.channel.id not in allowed_channels:
            continue

        if line.startswith("!delete"):
            command_tag = "!delete"
            url = line.split()[1]
        else:
            url = line

        # Check if the link is a valid URL
        match = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', url)
        match_2 = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]+\.[a-zA-Z0-9()]{2,6}[/a-zA-Z0-9._?=\-&]+', url)
        link = url.replace("http://", "").replace("https://", "")

        if match or match_2:
            engine = await connector_function(SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE)
            if not engine:
                return

            Base = declarative_base()

            class Link(Base):
                __tablename__ = 'link'
                id = Column(Integer, primary_key=True)
                link = Column(String)

            Base.metadata.create_all(engine)

            Session = sessionmaker(bind=engine)
            session = Session()

            if command_tag == "!delete":
                result = session.query(Link).filter_by(link=link).first()
                if not result:
                    await message.channel.send(f"{url} is **not present** in the database {message.author.mention}.", delete_after=5)
                    print(f"{url} is not present in the database {message.author.name}.")
                else:
                    session.delete(result)
                    session.commit()
                    await message.channel.send(f"{url} has been **removed** from the database {message.author.mention}.", delete_after=5)
                    print(f"{url} has been **removed** from the database {message.author.name}.")
                continue  # Move to the next link

            result = session.query(Link).filter_by(link=link).first()
            if not result:
                new_link = Link(link=link)
                session.add(new_link)
                session.commit()
                await add_new_link(link, session, Link, message, bot, DEBUG_MODE, command_tag, url, message.author, int(DISCORD_CHANNEL_ID), int(GITHUB_CHANNEL), int(BLENDER_ADDONS_CHANNEL), int(ALL_CATEGORIES_CHANNEL_ID), classified_user, int(PHONE_APPS_CHANNEL), int(VIDEOS_CHANNEL), int(EXTENSION_CHANNEL), int(SUBREDDIT_CHANNEL), int(EBOOKS_PDF_CHANNEL), int(VIDEO_GAMES_CHANNEL), int(AI_WEBSITE_CHANNEL), int(SOFTWARE_CHANNEL), message.author.mention, message.author.name)
            else:
                target_channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
                if message.author.id in classified_user:
                    await target_channel.send(f"{url} is already in the database **user classified**.", delete_after=5)
                else:
                    await target_channel.send(f"{url} is already in the database {message.author.mention}.", delete_after=5)
                print(f"{url} is already in the database.")

bot.run(TOKEN)
