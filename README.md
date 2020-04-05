# scrapy
A web scrapping bot specifically aimed at scraping dictionary definitions from a CloudFlare-protected website, but it is adaptable to any website. Credit goes to Anarov for doing the heavy lifting regarding bypassing the anti-bot protection measures put in place by Cloud Flare. [Link to that repo](https://github.com/Anorov/cloudflare-scrape "cloudflare-scrape")

## Instructions
Clone the repo `git clone https://github.com/consciouscollective-online/scrapy.git`

Navigate to root directory and run `cd scrapy && pip install -r requirements.txt`

Run the program `python3 scrape.py`

The first layer of scraping doesn't take all-that long and needs to complete in its entirety, in order to be cached.

The second and third layers are actively cached (layer 3, in batches) to aid in recovery from system crashes/program halts.

### Recommended execution instructions
this script takes a long time to execute. It is recommended you run this script, unnattended.

Supposing you're on a linux server:

`crontab -e`

insert the following text at the end of the file ("from_email@address.com" can be a dummy string. Mail will use your configured email address):

> @reboot cd /path/to/scrapy/ && python3 scrape.py &
>
> 0 */3 * * * sh /path/to/scrapy/update-me.sh "from_email@address.com" "to_email@address.com"

Then execute the following:

`sudo service cron reload`

`sudo reboot`
