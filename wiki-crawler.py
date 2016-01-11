import requests
import bs4

WIKIPEDIA = 'https://en.wikipedia.org'

class Spider(object):
    """A Wikipedia spider that follows the first link of of first paragraph of an
    article. As it crawls, it prints the name of the article it is on, and
    the url.
    """
    
    def __init__(self, start=None, max_distance=10):
        """
        Spider defaults to the Today's Featured Article from the English main
        page of Wikipedia.

        Unresolved glitch: Spider does not properly print the article title
        when it follows the link to /wiki/International_Phonetic_Alphabet.
        """
        
        if start == None:
            # Sets starting point to Today's Featured Article when default
            soup = url_soup(WIKIPEDIA)
            featured = soup.find('div', {'id': 'mp-tfa'})
            href = featured.b.a.get('href')
            self.current_url = WIKIPEDIA + href
            self.current_page = featured.b.a.get('title')
            self.current_soup = url_soup(self.current_url)
        else:
            self.current_url = start
            self.current_soup = url_soup(start)
            self.current_page = str(self.current_soup.p.b)[3:-4]
            
            
        self.max_distance = max_distance
        self.pages_visited = [(self.current_page, self.current_url)]

        while len(self.pages_visited) <= self.max_distance:
            print(self.current_page + ":\n" + self.current_url)
            self.crawl()
            
        # Option to display all pages visited after the fact    
        #for page in self.pages_visited:
        #    print(page[0] + ":\n" + page[1])

    def crawl(self):
        """Method to follow the first link of the first paragraph of a
        Wikipedia article.
        """
        
        destination = WIKIPEDIA + self.current_soup.p.a.get('href')
        self.current_url = destination
        self.current_soup = url_soup(destination)
        self.current_page = str(self.current_soup.p.b)[3:-4]
        self.pages_visited.append((self.current_page, self.current_url))
        
        

def url_soup(url):
    """A function to truncate the steps between a url and a BeautifulSoup
    object.
    """
    
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = bs4.BeautifulSoup(plain_text, "html.parser")
    return soup


page = 'https://en.wikipedia.org/wiki/Dishonored'
spider = Spider()

