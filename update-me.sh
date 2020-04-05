#!/bin/bash
cd ~/projects/scrapy
echo "Stage 2 scraping progress:\n" > tmp
tail -n 5 cache.data >> tmp
echo "Latest words scraped:\n" >> tmp
tail -n 5 checked.txt >> tmp
echo "\nEnd transmission." >> tmp
mail -a "From: Robot <{$1}>" -s "Update: Dictionary Scrape" $2 < ./tmp
rm tmp
