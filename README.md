Note: I have stopped development on this script as I have managed to much more efficiently perform this data collection using API endpoints. I'm going to keep that script proprietary for now.

Web scraper that uses the Selenium library in Python to look for value in trading card markets. Given a collection of pages on TCGPlayer.com, the script iterates through as many pages as the user specifies and looks for cards and sellers that have listed cards at 30% or more below market price.

To use, take a URL from TCGPlayer containing any list of cards that can be sorted. I believe this works with booster packs as well but I haven't verified that it works with any other possible HTML elements that might be encountered with other product types.

This can also be a URL from a specific person's store. You can then specify how many pages to scrape and it will iterate through all of them, saving any results greater than 30% below market price to tgplayer_data.csv. I am hoping to add some functionality where you can continue a scrape that was interrupted from a specific page number.
