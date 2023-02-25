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
    TOKEN = config('TOKEN', str)


    return SQL_HOST, SQL_USER, SQL_PASS, SQL_DATABASE, DISCORD_CHANNEL_ID, TOKEN
