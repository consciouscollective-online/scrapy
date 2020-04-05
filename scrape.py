from bs4 import BeautifulSoup
import requests
from string import ascii_lowercase
import cfscrape
import os

def scrape_collins():
    lx, ly = [], [] 
    lx_complete, ly_complete = False, False
    lx_last_val, ly_last_val = "", ""
    reading = -1

    #INITIALISE
    if os.path.isfile("cache.data"):
        cache_r_file = open("cache.data", mode="r")
        print("Reading from cache...", end="", flush=True)
        for line in cache_r_file:
            if line[:-2]=="#END":
                reading = -1
                if line[:-1]=="#END0":
                    lx_complete = True
                elif line[:-1]=="#END1":
                    ly_complete = True

            if reading == 0:
                lx.append(line)
            elif reading == 1:
                ly.append(line)

            if line[:-1]=="#0":
                reading = 0
            elif line[:-1]=="#1":
                reading = 1           
        if ly != []:
            ly_last_val = ly[-1]
        print(" done.")

    else:
        print("Creating cache file...")
        cache_r_file = open("cache.data", mode="r+")
    cache_r_file.close()
    cache_a_file = open("cache.data", mode="a+")

    #SCRAPE A to Z, 0-9 lists
    if not lx_complete:
        print("Scraping layer 1/3...", end="", flush=True)
        for char in ascii_lowercase:
            data = BeautifulSoup(G_scraper.get("https://www.collinsdictionary.com/browse/english/words-starting-with-" + char).content.decode("UTF-8"),features="html.parser")
            for d in data.body.find("ul",class_="columns2").find_all("a"):
                lx.append(d['href'])
        cache_a_file.write("#0\n")
        for item in lx:
            cache_a_file.write(str(item)+"\n")
        cache_a_file.write("#END0\n")
        lx_complete = True
        cache_a_file.flush()
        print(" done.", end="\n")
    else:
        print("Using cached data for layer 1/3.")

    #SCAPE wordset
    if not ly_complete: 
        print("Scraping layer 2/3...", end="", flush=True)
        
        if ly_last_val != "\n":
            cache_a_file.write("#1\n")
        
        for url in lx:
            if url <= ly_last_val:
                pass
            else:
                data = BeautifulSoup(G_scraper.get(url).content.decode("UTF-8"),features="html.parser")
                for d in data.body.find("ul",class_="columns2").find_all("a"):
                    ly.append(d['href'])
                cache_a_file.write(url+"\n")
        data = BeautifulSoup(G_scraper.get("https://www.collinsdictionary.com/browse/english/words-starting-with-digit").content.decode("UTF-8"),features="html.parser")
        for d in data.body.find("ul",class_="columns2").find_all("a"):
            ly.append(d['href'])
        cache_a_file.write("#END1\n")
        ly_complete = True
        cache_a_file.flush()
        print(" done.", end="\n")
    else:
        print("Using cached data for layer 2/3.")
    
    #SCRAPE dictionary
    if not (lx_complete and ly_complete):
        print("Something went awry. Forcing a restart.")
        print("Clearing local cache...", end="", flush=True)
        os.remove("cache.data")
        print(" done.", end="\n")
    else:
        print("Scraping dictionary...",end="", flush=True)
        if os.path.isfile("checked.txt"):
            checked_file = open("checked.txt", mode="r")
            last_checked = str(checked_file.readlines()[-1][:-1])
            checked_file.close()
        else:
            checked_file = open("checked.txt", mode="a+")
            checked_file.write("0\n")
            last_checked = "0"
            checked_file.close()
        checked_file = open("checked.txt", mode="a")
        for url in ly:
            newrl = url[:-1]
            if last_checked >= newrl:
                pass
            else:
                print(newrl)
                data = BeautifulSoup(G_scraper.get(newrl).content.decode("utf-8"),features="html.parser")
                essence = data.find_all("div",class_="dictentry dictlink")
                essence = str(essence)
                out_file.write(essence)
                out_file.flush()
                checked_file.write(newrl+"\n")
                checked_file.flush()
        print(" done.")

### MAIN ###
if __name__ == "__main__":
    out_file = open("dictionary.html",mode="a", encoding='utf-8')
    G_scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
    scrape_collins()
    checked_file.flush()
    checked_file.close()
    out_file.flush()
    out_file.close()

