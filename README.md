# scrapy
A web scrapping bot specifically aimed at scraping dictionary definitions but it is adaptable to any website.

## Intuition
Words that hit an endpoint are added to are_words.txt. The rest are added to not_words.txt. 
When the program is initialised, it checks where it left-off by getting the last word recorded in the above two text files.
For now, the scraped html has been stripped of script tags. Noscript tags aren't as numerous but will be extracted in future releases.
The scraped content is purely for academic purposes.
