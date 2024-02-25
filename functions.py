from decouple import config
import re
from sqlalchemy import create_engine, Column, Integer, String


def mysql_push(link, session, Link):
    # Remove "http://" or "https://" from the link if it exists
    link = link.replace("http://", "").replace("https://", "")

    new_link = Link(link=link, title=None, description=None, pict=None)
    print(new_link)
    print(new_link.link)
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
    ALL_CATEGORIES_CHANNEL_ID = config('ALL_CATEGORIES_CHANNEL_ID', int)
    GUILD_ID = config('GUILD_ID', list)
    TOKEN = config('TOKEN', str)
    SUBREDDIT_CHANNEL = config('SUBREDDIT_CHANNEL', int)
    EXTENSION_CHANNEL = config('EXTENSION_CHANNEL', int)
    VIDEOS_CHANNEL = config('VIDEOS_CHANNEL', int)
    PHONE_APPS_CHANNEL = config('PHONE_APPS_CHANNEL', int)
    GITHUB_CHANNEL = config('GITHUB_CHANNEL', int)
    BLENDER_ADDONS_CHANNEL = config('BLENDER_ADDONS_CHANNEL', int)
    EBOOKS_PDF_CHANNEL = config('EBOOKS_PDF_CHANNEL', int)
    VIDEO_GAMES_CHANNEL = config('VIDEO_GAMES_CHANNEL', int)
    AI_WEBSITE_CHANNEL = config('AI_WEBSITE_CHANNEL', int)
    SOFTWARE_CHANNEL = config('SOFTWARE_CHANNEL', int)
    HIDDEN_USERS = config('HIDDEN_USERS', cast=lambda x: [int(i) for i in x.split(',')])
    DEBUG_MODE = config('DEBUG_MODE', bool)
    SECRET_TOKEN = config('SECRET_TOKEN', bool)


    return SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL,BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN


def DEBUG_MESSAGE(SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, GUILD_ID, ALL_CATEGORIES_CHANNEL_ID, TOKEN, SUBREDDIT_CHANNEL, EXTENSION_CHANNEL, VIDEOS_CHANNEL, PHONE_APPS_CHANNEL, GITHUB_CHANNEL, BLENDER_ADDONS_CHANNEL, EBOOKS_PDF_CHANNEL, VIDEO_GAMES_CHANNEL, AI_WEBSITE_CHANNEL, SOFTWARE_CHANNEL, HIDDEN_USERS, DEBUG_MODE, SECRET_TOKEN
):
        
        print()
        DEBUG_MODE_STR = str(DEBUG_MODE)
        if DEBUG_MODE_STR == "True":
            print(f"{'##':#^150}\n{' DEBUG MODE IS ON ':#^150}\n{'##':#^150}")
            print(f"SQL_HOST: {SQL_HOST}")
            print(f"SQL_USER: {SQL_USER}")
            print(f"SQL_PASS: {SQL_PASS}")
            print(f"SQL_DATABASE: {SQL_DATABASE}")
            print(f"DISCORD_CHANNEL_ID: {DISCORD_CHANNEL_ID}")
            print(f"GUILD_ID: {GUILD_ID}")
            print(f"ALL_CATEGORIES_CHANNEL_ID: {ALL_CATEGORIES_CHANNEL_ID}")
            print(f"SUBREDDIT_CHANNEL: {SUBREDDIT_CHANNEL}")
            print(f"EXTENSION_CHANNEL: {EXTENSION_CHANNEL}")
            print(f"VIDEOS_CHANNEL: {VIDEOS_CHANNEL}"), 
            print(f"PHONE_APPS_CHANNEL: {PHONE_APPS_CHANNEL}")
            print(f"GITHUB_CHANNEL: {GITHUB_CHANNEL}")
            print(f"BLENDER_ADDONS_CHANNEL: {BLENDER_ADDONS_CHANNEL}")
            print(f"EBOOKS_PDF_CHANNEL: {EBOOKS_PDF_CHANNEL}")
            print(f"VIDEO_GAMES_CHANNEL: {VIDEO_GAMES_CHANNEL}")
            print(f"AI_WEBSITE_CHANNEL: {AI_WEBSITE_CHANNEL}")
            print(f"SOFTWARE_CHANNEL: {SOFTWARE_CHANNEL}")
            print(f"HIDDEN_USERS: {HIDDEN_USERS}")
            if SECRET_TOKEN == True:
                print(f"TOKEN: {TOKEN}")


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

async def command_use(message, session, Link, link):
    link_ignore = False
    link_delete = False
    if message.content.startswith("!ignore"):
        link_ignore = True
    elif message.content.startswith("!delete"):
        link_delete = True
    link = message.content.split()[1]
    link = link.replace("http://", "").replace("https://", "")
    result = session.query(Link).filter_by(link=link).first()
    
    print (result)
    
    return link, link_ignore, link_delete, result
    
    
async def connector_function(SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE):
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
    return engine

async def add_new_link(link, session, Link, message, bot, DEBUG_MODE, command_tag, url, author, DISCORD_CHANNEL_ID_int, GITHUB_CHANNEL_int, BLENDER_ADDONS_CHANNEL_int, ALL_CATEGORIES_CHANNEL_ID_int, classified_user, PHONE_APPS_CHANNEL_int, VIDEOS_CHANNEL_int, EXTENSION_CHANNEL_int, SUBREDDIT_CHANNEL_int, EBOOKS_PDF_CHANNEL_int, VIDEO_GAMES_CHANNEL_int, AI_WEBSITE_CHANNEL_int, SOFTWARE_CHANNEL_int, mention, discord_name):
    
    all_target_channel = bot.get_channel(ALL_CATEGORIES_CHANNEL_ID_int)
    if re.search('!ignore', command_tag):
        
        
        
        
        target_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        
        if author.id in classified_user:
            await target_channel.send(f"{url} addded sucessfully by **user classified**!")
            await all_target_channel.send(f"{url} addded sucessfully by **user classified**!")
        else:

            await target_channel.send(f"{url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"{url} added successfully by **{author.display_name}**!")
    #video games
    elif re.search(r'(store\.steampowered\.com/app/|store\.playstation\.com/.*/product/|store\.xbox\.com/.*/Xbox-One/Games/|nintendo\.com/games/detail/|epicgames\.com/store/.*/product/)', url):
        target_channel = bot.get_channel(VIDEO_GAMES_CHANNEL_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await temp_channel.send(f"We have added the video game sucessfully Please check <#{VIDEO_GAMES_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"Video Game {url} added successfully by **user classified**!")
            await all_target_channel.send(f"Video Game {url} added successfully by **user classified**!")
        else:
            await target_channel.send(f"Video Game {url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"Video Game {url} added successfully by **{author.display_name}**!")
    elif re.search(r'(blendermarket\.com/products/)', url) or message.channel.id == BLENDER_ADDONS_CHANNEL_int:
        target_channel = bot.get_channel(BLENDER_ADDONS_CHANNEL_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await temp_channel.send(f"We have added the blender addon sucessfully Please check <#{BLENDER_ADDONS_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"Blender Addon {url} added successfully by **user classified**!")
            await all_target_channel.send(f"Blender Addon {url} added successfully by **user classified**!")
        else:
            await target_channel.send(f"Blender Addon {url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"Blender Addon {url} added successfully by **{author.display_name}**!")  
            
    elif message.channel.id == AI_WEBSITE_CHANNEL_int or re.search(r'(\.ai)', url):
        target_channel = bot.get_channel(AI_WEBSITE_CHANNEL_int)
        
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await message.channel.send(f"We have added the AI Website sucessfully Please check <#{AI_WEBSITE_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"AI Website {url} added successfully by **user classified**!")
            await all_target_channel.send(f"AI Website {url} added successfully by **user classified**!")
        else:
            await target_channel.send(f"AI Website {url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"AI Website {url} added successfully by **{author.display_name}**!")
            
            
    elif re.search(r'(github\.com/)', url):
        target_channel = bot.get_channel(GITHUB_CHANNEL_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await temp_channel.send(f"We have added the GitHub Repo sucessfully Please check <#{GITHUB_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"Github repository {url} added successfully by **user classified**!")
            await all_target_channel.send(f"Github repository {url} added successfully by **user classified**!")
        else:
            await target_channel.send(f"Github repository {url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"Github repository {url} added successfully by **{author.display_name}**!")
            
    elif re.search(r'(\.epub|\.mobi|\.pdf|\.azw3?|\.cbz|\.cbr|\.azw4?|\.djvu?|\.fb2?|\.html|\.xhtml?|\.ebook|\.ereader|\.kindle|play\.google\.com/store/books/details/|(?:barnesandnoble|barnesandnoble)\.com/w/|kobo\.com/.*/ebook/|gutenberg\.org/ebooks/|ebooks\.com/en-gb/book/).*', url):
        target_channel = bot.get_channel(EBOOKS_PDF_CHANNEL_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await temp_channel.send(f"We have added the E-Book sucessfully Please check <#{EBOOKS_PDF_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"E-Book {url} added successfully by **user classified**!")
            await all_target_channel.send(f"E-Book {url} added successfully by **user classified**!")
        else:
            await target_channel.send(f"E-Book {url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"E-Book {url} added successfully by **{author.display_name}**!")
        
    elif re.search(r'(play\.google\.com/store/apps|apps\.apple\.com/)', url) or command_tag == "!app" or message.channel.id == PHONE_APPS_CHANNEL_int:
        
        link = re.sub(r'&hl=[^&]*', '', url)
        link = re.sub(r'&gl=[^&]*', '', url)
        target_channel = bot.get_channel(PHONE_APPS_CHANNEL_int)
        
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        if message.channel.id != PHONE_APPS_CHANNEL_int:
            await temp_channel.send(f"We have added the phone app sucessfully Please check <#{PHONE_APPS_CHANNEL_int}> for your submitted link.", delete_after=5)

        if author.id in classified_user:
            await target_channel.send(f"Phone app {url} added successfully by **user classified**! Please keep in mind we do not control or own any of the content posted on the apps we share.")
            await all_target_channel.send(f"Phone app {url} added successfully by **user classified**! Please keep in mind we do not control or own any of the content posted on the apps we share.")
        else:
        
            await target_channel.send(f"Phone app {url} added successfully by **{author.display_name}**! Please keep in mind we do not control or own any of the content posted on the apps we share.")
            await all_target_channel.send(f"Phone app {url} added successfully by **{author.display_name}**! Please keep in mind we do not control or own any of the content posted on the apps we share.")
            
    elif re.search(r'(chrome\.google\.com/webstore|addons\.mozilla\.org|microsoftedge\.microsoft\.com/addons/detail/|addons\.opera\.com/en/extensions/details/)', url) or message.channel.id == EXTENSION_CHANNEL_int:
        
        target_channel = bot.get_channel(EXTENSION_CHANNEL_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await temp_channel.send(f"We have added the extension sucessfully Please check <#{EXTENSION_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"Extension {url} added successfully by **user classified**! Please keep in mind extensions may not be varified by the Chrome Web Store, Mozilla Addons, Opera Addons, or Microsoft Edge Addons.")
            await all_target_channel.send(f"Extension {url} added successfully by **user classified**! Please keep in mind extensions may not be varified by the Chrome Web Store, Mozilla Addons, Opera Addons, or Microsoft Edge Addons.")
        else:
            await target_channel.send(f"Extension {url} added successfully by **{author.display_name}**! Please keep in mind extensions may not be varified by the Chrome Web Store, Mozilla Addons, Opera Addons, or Microsoft Edge Addons.")
            await all_target_channel.send(f"Extension {url} added successfully by **{author.display_name}**! Please keep in mind extensions may not be varified by the Chrome Web Store, Mozilla Addons, Opera Addons, or Microsoft Edge Addons.")
        
        
    elif re.search(r"reddit\.com/r/", url) and not re.search(r"/comments/", url):
        target_channel = bot.get_channel(SUBREDDIT_CHANNEL_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await temp_channel.send(f"We have added the subreddit sucessfully Please check <#{SUBREDDIT_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"Subreddit {url} added successfully by **user classified**! Please keep in mind we do not control or own any of the content posted on the subreddits we share.")
            await all_target_channel.send(f"Subreddit {url} added successfully by **user classified**! Please keep in mind we do not control or own any of the content posted on the subreddits we share.")
        else:
            
            await target_channel.send(f"Subreddit {url} added successfully by **{author.display_name}**! Please keep in mind we do not control or own any of the content posted on the subreddits we share.")
            await all_target_channel.send(f"Subreddit {url} added successfully by **{author.display_name}**! Please keep in mind we do not control or own any of the content posted on the subreddits we share.")
        
    elif re.search(r'(\/watch\?v=|youtu\.be/)', url):
        target_channel = bot.get_channel(VIDEOS_CHANNEL_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await temp_channel.send(f"We have added the YouTube video sucessfully Please check <#{VIDEOS_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"Video {url} added successfully by **user classified**!")
            await all_target_channel.send(f"Video {url} added successfully by **user classified**!")
        else:
            await target_channel.send(f"Video {url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"Video {url} added successfully by **{author.display_name}**!")
    elif message.channel.id == SOFTWARE_CHANNEL_int:
        
        target_channel = bot.get_channel(SOFTWARE_CHANNEL_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        await temp_channel.send(f"We have added the software sucessfully Please check <#{SOFTWARE_CHANNEL_int}> for your submitted link.", delete_after=5)
        if author.id in classified_user:
            await target_channel.send(f"Software {url} added successfully by **user classified**!")
            await all_target_channel.send(f"Software {url} added successfully by **user classified**!")
        else:
            await target_channel.send(f"Software {url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"Software {url} added successfully by **{author.display_name}**!")
            
        
    else:
        target_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        temp_channel = bot.get_channel(DISCORD_CHANNEL_ID_int)
        if author.id in classified_user:
            await target_channel.send(f"{url} added successfully by **user classified**!")
            await all_target_channel.send(f"{url} added successfully by **user classified**!")
        else:
            await target_channel.send(f"{url} added successfully by **{author.display_name}**!")
            await all_target_channel.send(f"{url} added successfully by **{author.display_name}**!")
        print(f"Link {url} added successfully!")
        