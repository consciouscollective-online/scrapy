#!/bin/bash
cd ~/projects/scrapy
echo "Latest words scraped:\n" >> tmp
tail -n 15 checked.txt >> tmp
echo "\nEnd transmission." >> tmp
mail -a "From: Robot <$1>" -s "Update: Dictionary Scrape" $2 < ./tmp
rm tmp
