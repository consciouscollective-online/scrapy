from bs4 import BeautifulSoup
import requests
from string import ascii_lowercase
import cfscrape
import os, sys
from progress.bar import IncrementalBar

#GLOBAL NAMESPACE VAR DECLARATIONS
out_file = open("dictionary.html",mode="a", encoding='utf-8')
scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
lx, ly, lz = [], [], []
lx_begins, ly_begins = False, False
lx_completed, ly_completed = False, False
lx_last_val, ly_last_val, lz_last_val = "", "", ""
reading = -1

def read_cache():
    global reading,     lx,  lx_completed, lx_begins, lx_last_val
    global lz_last_val, ly, ly_completed, ly_begins, ly_last_val
    lx, ly,lz = [], [], [] 
    if os.path.isfile("cache.data"):
        cache_r_file = open("cache.data", mode="r")
        print("Reading from cache...", end="", flush=True)
        for line in cache_r_file:
            if line[:-2]=="#END":
                reading = -1
                if line[:-1]=="#END0":
                    lx_completed = True
                elif line[:-1]=="#END1":
                    ly_completed = True

            if reading == 0:
                lx.append(line)
            elif reading == 1:
                ly.append(line)
            elif reading == 2:
                lz.append(line)

            if line[:-1]=="#0":
                reading = 0
                lx_begins = True
            elif line[:-1]=="#1":
                reading = 1
                ly_begins = True    
            elif line[:-1]=="#2":
                reading = 1
                ly_begins = True     

        if ly != []:
            ly_last_val = ly[-1]
        if lz != []:
            lz_last_val = lz[-1]

        print(" done.")
        cache_r_file.close()
    else:
        print("Creating cache file...", end="", flush=True)
        cache_file = open("cache.data", mode="w+")
        cache_file.close()
        print(" done.")
    return open("cache.data", mode="a")
def scrape_collins():
    global reading,     lx,  lx_completed, lx_begins, lx_last_val
    global lz_last_val, ly, ly_completed, ly_begins, ly_last_val
    #INITIALISE
    cache_file = read_cache()

    #SCRAPE METADATA
    if not lx_completed:
        print("Scraping meta-data")
        bar = IncrementalBar("Scraping stage 1/3", max=len(ascii_lowercase), suffix='%(percent).1f%% - %(index)s of %(max)s')
        for char in ascii_lowercase:
            data = BeautifulSoup(scraper.get("https://www.collinsdictionary.com/browse/english/words-starting-with-" + char).content.decode("UTF-8"),features="html.parser")
            for d in data.body.find("ul",class_="columns2").find_all("a"):
                lx.append(d['href'])
            bar.next()
        cache_file.write("#0\n")
        for item in lx:
            cache_file.write(str(item)+"\n")
        cache_file.write("#END0\n")
        lx_completed = True
        cache_file.flush()
        bar.finish()
    else:
        print("Using cached data for stage 1/3.")

    #SCRAPE WORD LIST
    if not ly_completed: 
        print("Building word list")
        if not ly_begins:
            cache_file.write("#1\n")
            data = BeautifulSoup(scraper.get("https://www.collinsdictionary.com/browse/english/words-starting-with-digit").content.decode("UTF-8"),features="html.parser")
            for d in data.body.find("ul",class_="columns2").find_all("a"):
                ly.append(d['href'])
                cache_file.write(d['href']+"\n")
                cache_file.flush()
        cache_file.close()
        cache_file = read_cache()   
        bar = IncrementalBar("Scraping stage 2/3", max=len(lx), suffix='%(percent).1f%% - %(index)s of %(max)s')
        for url in lx:
            newrl = url.strip()
            if newrl.strip("https://www.collinsdictionary.com/dictionary/english/") < ly_last_val.strip("https://www.collinsdictionary.com/dictionary/english/"):
                pass
            else:
                data = BeautifulSoup(scraper.get(newrl).content.decode("UTF-8"),features="html.parser")
                for d in data.body.find("ul",class_="columns2").find_all("a"):
                    ly.append(d['href'])
                    cache_file.write(d['href']+"\n")
                cache_file.flush()
            bar.next()
        cache_file.write("#END1\n")
        bar.finish()
        ly_completed = True
        cache_file.flush()
    else:
        print("Using cached data for layer 2/3.")
    
    #SCRAPE DICTIONARY
    if not (lx_completed and ly_completed):
        print("Something went awry. Forcing a restart.")
        print("Clearing local cache...", end="", flush=True)
        os.remove("cache.data")
        print(" done.", end="\n")
    else:
        print("Scraping dictionary...")
        if os.path.isfile("checked.txt"):
            checked_file = open("checked.txt", mode="r")
            last_checked_word = str(checked_file.readlines()[-1][:-1])
            checked_file.close()
        else:
            checked_file = open("checked.txt", mode="a+")
            checked_file.write("0\n")
            last_checked_word = "0"
            checked_file.close()
        checked_file = open("checked.txt", mode="a")
        bar = IncrementalBar("Scraping stage 3/3", max=len(ly), suffix='%(percent).1f%% - %(index)s of %(max)s')
        cache_file.write("#2\n")
        for url in ly:
            newrl = url.strip()
            if newrl < lz_last_val.strip() :
                pass
            else:
                print(newrl)
                data = BeautifulSoup(scraper.get(newrl).content.decode("utf-8"),features="html.parser")
                essence = data.find_all("div",class_="dictentry dictlink")
                essence = str(essence)
                out_file.write(essence)
                out_file.flush()
                checked_file.write(newrl.strip("https://www.collinsdictionary.com/browse/english/")+"\n")
                checked_file.flush()
                cache_file.write(newrl+"\n")
                cache_file.flush()
        checked_file.flush()
        checked_file.close()
        out_file.flush()
        out_file.close()
        cache_file.write("#END2\n")
        cache_file.flush()
        cache_file.close()
        print(" done.")

### MAIN ###
if __name__ == "__main__":
    scrape_collins()
    