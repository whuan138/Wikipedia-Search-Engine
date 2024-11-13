import scrapy
import requests
from bs4 import BeautifulSoup
from scrapy.http import Request

class WikiSpider(scrapy.Spider):
    const = 60 
    curr = 0
    max_files = 70000
    name = "wiki-spider"
    all_links = []
    #start_urls = ['https://en.wikipedia.org/wiki/Main_Page']

     #GET ALL SUBLINKS FROM A STARTING URL
    def getSublinks(self, start_link):
        page = requests.get(start_link) #"https://en.wikipedia.org/wiki/Main_page"
    
        # create parser
        soup = BeautifulSoup(page.content, 'html.parser')
        list(soup.children)
        
        # find all sublinks
        for link in soup.find_all('a'):
            url = link.get("href")

            self.curr = 0
            if url is not None:
                if self.curr < 45:
                    self.curr += 1
                if not url.startswith("#") and url.startswith("/wiki/"):
                    # make all urls click-able links
                    if url.startswith("/"):
                        url = "https://en.wikipedia.org"+ url 
                        self.curr += 1
                    
                    if self.curr >= self.const: 
                         curr = 0 
                         return 
                        
                    if url not in self.all_links:
                        print(url)
                        self.all_links.append(url) # only add if it doesn't exist
                        if len(self.all_links) == 70000:
                            return

    def getLinks(self, url, hop=0, hop_lim=4):
        # keep track of what hop we are on
        if hop > hop_lim:
            return

        print("\n\n\n------> HOP :" + str(hop) + "\n")
        print(url, "current page")

        if len(self.all_links) == 70000:
            return
        
        # get the sublinks of the current hop
        self.getSublinks(url)
        
        # save the sublinks to a file (links.txt)
        #self.saveLinks(all_links) 
        
        # iterate over sublinks
        for link in self.all_links:
            # increase the hop number, get those links --> RECURSIVE STEP
            self.getLinks(link, hop + 1, hop_lim)
            

    def start_requests(self):
        #all_links = ['https://en.wikipedia.org/wiki/Main_Page']
        self.getLinks("https://en.wikipedia.org/wiki/U.S._Route_11_in_Louisiana")
        temp = 35
        while temp != 0:
            self.all_links.pop(0)
            temp = temp - 1
        for url in self.all_links:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        title = response.css('title::text').get()
        paragraphs = response.css('p::text').getall()
        category_elements = response.css('#mw-normal-catlinks ul li a')
        categories = []
        for category_element in category_elements:
            category = category_element.css('::text').get()
            categories.append(category)
        content = "\n".join(paragraphs)
        yield { #yields a dictionary
            'title': title,
            'content': content,
            'categories': categories,
            'link': response.url
            #'text': response.css('span.text::text').get()
            
        }

   