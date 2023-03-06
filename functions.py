from decouple import config


def mysql_push(link, session, Link):
    # Remove "http://" or "https://" from the link if it exists
    link = link.replace("http://", "").replace("https://", "")

    new_link = Link(link=link, title=None, description=None, pict=None)
    session.add(new_link)
    session.commit()
    return link


def env_pull():
# MySQL login information
    SQL_HOST = config('SQL_HOST', default='localhost')
    SQL_USER = config('SQL_USER') or ''
    SQL_PASS = config('SQL_PASS') or ''
    SQL_DATABASE = config('SQL_DATABASE') or ''
    DISCORD_CHANNEL_ID = config('DISCORD_CHANNEL_ID', int)
    GUILD_ID = config('GUILD_ID', list)
    TOKEN = config('TOKEN', str)
    SUBREDDIT_CHANNEL = config('SUBREDDIT_CHANNEL', int)
    EXTENSION_CHANNEL = config('EXTENSION_CHANNEL', int)
    VIDEOS_CHANNEL = config('VIDEOS_CHANNEL', int)
    DEBUG_MODE = config('DEBUG_MODE', bool)
    SECRET_TOKEN = config('SECRET_TOKEN', bool)


    return SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, DEBUG_MODE, SECRET_TOKEN


async def use_subreddit_channel(SUBREDDIT_CHANNEL_int, DISCORD_CHANNEL_ID_int, url, author, message, bot, DEBUG_MODE):
    if SUBREDDIT_CHANNEL_int == DISCORD_CHANNEL_ID_int:
        
        if DEBUG_MODE == True:
            print("Subreddit channel is the same as the default channel.")
        await message.channel.send(f"{url} added successfully by {author.display_name}!")
    else:
        print("Subreddit channel is not the same as the default channel.")
        target_channel =  bot.get_channel(SUBREDDIT_CHANNEL_int)
        print(target_channel)
        await target_channel.send(f"{url} added successfully by {author.display_name}!")
        print(f"Subreddit {url} added successfully!")
        
    return url