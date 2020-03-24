from bs4 import BeautifulSoup
import cfscrape
import multiprocessing

def worker(word):
    is_word = False
    data = BeautifulSoup(scraper.get("http://www.collinsdictionary.com/dictionary/english/"+word).content.decode("UTF-8"),features="html.parser")
    data = data.body.main.find(class_="dictionaries dictionary")
    if data is not None:
        [s.extract() for s in data('script')]
        print(word)
        is_word = True
    return word, data, is_word

# headers = {'X-API-TOKEN': 'your_token_here'}
# payload = {'title': 'value1', 'name': 'value2'}
#
# s = requests.Session()
# r = s.get("https://www.collinsdictionary.com/")
# cookies = r.cookies
# r = s.get("https://www.collinsdictionary.com/dictionary/english/barrel", cookies=cookies)
# soup = BeautifulSoup(r.text)


# file = open('out.html', mode='w+')
# file.write(data)  # => "<!DOCTYPE html><html><head>..."
# file.close()
def get_last_words():
    """
    returns the last_is_word WORD, last_not_word WORD
    """
    with open('are_words.txt', 'r') as f:
        lines = f.read().splitlines()
        last_is_word = lines[-1]

    with open('not_words.txt', 'r') as f:
        if f:
            lines = f.read().splitlines()
            last_not_word = lines[-1]

    return last_is_word,last_not_word





if __name__ == '__main__':
    scraper = cfscrape.create_scraper() 
    last_is_word, last_not_word = get_last_words()
    last_word = max(last_is_word,last_not_word)
    at_lw_pos = False
    in_file = open("words.txt").readlines()

    out_file = open("out.html", mode="a")
    are_words_file = open("are_words.txt", "a")
    not_words_file = open("not_words.txt", "a")
    
    for line in in_file:
        if line>=last_word:
            word,data,is_word = worker(line.lower())
            if is_word:
              out_file.write(word+"\n")
              out_file.write(str(data) +"\n")
              are_words_file.write(word)
            else:
               not_words_file.write(word)
        else:
            continue 

    are_words_file.close()
    not_words_file.close()
    # out_file.close()
