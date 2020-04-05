# scrapy
A web scrapping bot specifically aimed at scraping dictionary definitions from a CloudFlare-protected website, but it is adaptable to any website.
## Instructions
1) Navigate to root directory and run `pip install -r requirements.txt`
2) using Python 3, run `python scrape.py`

The first layer of scraping doesn't take all-that long and needs to complete in its entirety, in order to be cached.

### Recommended execution instructions
this script takes a long time to execute.
It is recommended you run this script, unnattended.

Supposing you're on a linux server:
`crontab -e`

insert the following text at the end of the file ("from_email@address.com" can be a dummy string. Mail will use your configured email address):
> @reboot cd /path/to/scrapy/ && python3 scrape.py &\n
> 0 */3 * * * sh /path/to/scrapy/update-me.sh "from_email@address.com" "to_email@address.com"


Then execute the following:
`sudo service cron reload`\n
`sudo reboot`
