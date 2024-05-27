# AnythingMayHappenBot

This bot takes links inputted into specific Discord channels and stores them in a MySQL database. It supports various commands and functionalities to manage and categorize these links.

## Features

- **Multiple Link Handling**: Process multiple links provided in a single message, each on a new line.
- **Link Validation**: Validate links to ensure they are properly formatted URLs.
- **Link Categorization**: Automatically categorize links into predefined categories (e.g., video games, Blender addons, AI websites, etc.).
- **MySQL Integration**: Store, retrieve, and delete links from a MySQL database.
- **Debug Mode**: Print debug information if enabled.
- **Channel Configuration**: Add specific channels to the allowed channels list dynamically.

## Commands

- `!setchannel <channel_id>`: Add a channel to the list of allowed channels.
- `!delete <link>`: Remove a link from the database.
- `!ignore <link>`: Ignore a specific link (not implemented in the provided code).

## Setup

### Prerequisites

- Python 3.7+
- MySQL server
- Discord bot token
- Required Python packages (see `requirements.txt`)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/AnythingMayHappenBot.git
   cd AnythingMayHappenBot
   ```
2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```
3. Configure the environment variables in a `.env` file:

   ```



   SQL_HOST=<your_mysql_host>
   SQL_USER=<your_mysql_user>
   SQL_PASS=<your_mysql_password>
   SQL_DATABASE=<your_mysql_database>
   DISCORD_CHANNEL_ID=<your_discord_channel_id>
   ALL_CATEGORIES_CHANNEL_ID=<all_categories_channel_id>
   GUILD_ID=<your_discord_guild_id>
   TOKEN=<your_discord_bot_token>
   SUBREDDIT_CHANNEL=<subreddit_channel_id>
   EXTENSION_CHANNEL=<extension_channel_id>
   VIDEOS_CHANNEL=<videos_channel_id>
   PHONE_APPS_CHANNEL=<phone_apps_channel_id>
   GITHUB_CHANNEL=<github_channel_id>
   BLENDER_ADDONS_CHANNEL=<blender_addons_channel_id>
   EBOOKS_PDF_CHANNEL=<ebooks_pdf_channel_id>
   VIDEO_GAMES_CHANNEL=<video_games_channel_id>
   AI_WEBSITE_CHANNEL=<ai_website_channel_id>
   SOFTWARE_CHANNEL=<software_channel_id>
   HIDDEN_USERS=<comma_separated_list_of_hidden_user_ids>
   DEBUG_MODE=<true_or_false>
   SECRET_TOKEN=<true_or_false>
   ```
4. Start the bot.

```Running
python AnythingMayHappenBot.py
```

## Functionality

### MySQL Connection Check

During startup, the bot checks the MySQL connection. If the connection fails, it sends a warning message to specified Discord channels and deletes the message after 20 seconds.

### Handling Messages

The bot processes messages in the allowed channels, splitting them into lines and validating each link. Depending on the command and the link, it performs the following actions:

- **Validation**: Ensures the link is a valid URL.
- **Categorization**: Identifies the category of the link (e.g., video game, Blender addon).
- **Database Operations**: Adds new links to the database or deletes existing ones based on commands.

### Debug Mode

If `DEBUG_MODE` is enabled, the bot prints detailed information about its operations, including the bot's name, ID, and message details.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the bot. Do not ever share your tokens inside the bot. 

## License

This project is licensed under the MIT License.
