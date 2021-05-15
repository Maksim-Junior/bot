# Telegram-bot to search for vacancies python developer on jobs.tut.by
/search - show all search words\
/list - show all vacancies suitable for search\
When you send any message to a bot, it is saved as a search word.\
When you send the same message, the word is removing from the list.

Every 5 minutes the bot checks if there are new vacancies that match the search words.\
If there are any, it will be sent to the user.
