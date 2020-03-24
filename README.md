# scrapy
A web scrapping bot specifically aimed at scraping dictionary definitions from a CloudFlare-protected website, but it is adaptable to any website.

## How to Use
Words are initially read from a master "words" list.
Words that hit an endpoint are added to are_words.txt. The rest are added to not_words.txt. 
When the program is initialised, it checks where it left-off by getting the last word recorded in the above two text files.
The scraped content is purely for academic purposes.

To keep the project adaptable/generic, dictionary-specific text extraction code will fall-over to the dictionary branch. The output data in out.html of the main repo is (mostly) raw html. I've tried to keep extraneous/duplicate code to a minimum.

## Some Hurdles Along the Way
cloudflares protection requires the client to present with cookies, i.e, a Session is to be established. The client also needs to be accepting of javasript content. Credit goes to user Anorov, a link to the original repo here: https://github.com/Anorov/cloudflare-scrape/tree/master/cfscrape
