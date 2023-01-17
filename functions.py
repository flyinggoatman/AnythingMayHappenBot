from decouple import config


def mysql_push(cnx, cursor, link):
        # Remove "http://" or "https://" from the link if it exists
        link = link.replace("http://", "").replace("https://", "")

        # Insert a new row into the "link" table
        query = "INSERT INTO link (link, title, description, pict) VALUES (%s, %s, %s, %s)"
        values = (link, None, None, None)
        cursor.execute(query, values)

        # Commit the changes
        cnx.commit()
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
