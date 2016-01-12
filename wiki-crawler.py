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
            
        self.destination = self.current_url    
        self.max_distance = max_distance
        self.pages_visited = [(self.current_page, self.current_url)]
        self.citations = dict()
        self.scrape_citations()

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
        if len(self.pages_visited) <= self.max_distance:
            soup = bs4.BeautifulSoup(str(self.current_soup.find('p')),
                                     "html.parser")
            #print("New Soup:\n" + str(soup) + "\n")
            for link in soup.findAll('a'):
                #print("\nLink:\n"+ str(link) +"\n")
                if "Help:IPA" in link.get('href'):
                    continue
                else:
                    self.destination = WIKIPEDIA + link.get('href')
                    break
            self.current_url = self.destination
            self.current_soup = url_soup(self.destination)
            self.current_page = str(self.current_soup.p.b)[3:-4]
            self.pages_visited.append((self.current_page, self.current_url))
            self.scrape_citations()
        else:
            print("Maximum depth reached.")

    def scrape_citations(self):
        """start_url is a string telling the crawler where to start."""
        sources = []
        soup = url_soup(self.current_url)
        
        citation_num = 1
        for reference in soup.findAll('span', {'class': 'reference-text'}):
            print("\n" + str(citation_num) + '.')
            citation_soup = bs4.BeautifulSoup(str(reference), "html.parser")
            #print(citation_soup)
            citation = citation_soup.find('a')#, {'class': 'external text'})
            if not citation:
                source = str(citation_soup)
            else:
                #print("\n" + str(citation))
                href = citation.get('href')
                #print("href: " + str(href))
                if citation.string is not None:
                    title = citation.string
                    source = title + ", " + href
                else:
                    source = "<Title Unavailable>, " + href
            sources.append(source)
            citation_num += 1
        page_name = str(soup.p.b)[3:-4]
        self.citations[page_name] = sources
        
        

def url_soup(url):
    """A function to truncate the steps between a url and a BeautifulSoup
    object.
    """
    
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = bs4.BeautifulSoup(plain_text, "html.parser")
    return soup


page = 'https://en.wikipedia.org/wiki/Dishonored'
page2 = 'https://en.wikipedia.org/wiki/Marc_Bendavid'
spider = Spider(start=page, max_distance=2)
for key in spider.citations:
    print(key + ":\n\n")
    for citation in spider.citations[key]:
        print(citation)
        print("\n")
