
# Imports
from urllib.request import urljoin 
from bs4 import BeautifulSoup 
import requests 
import pandas as pd
from urllib.request import urlparse 

def get_n_hop_links(depth,input_url):
    # Set for storing urls with same domain 
    links_intern = set() 
    
    # Set for storing urls with different domain 
    links_extern = set() 
    
    
    # Method for crawling a url at next level 
    def level_crawler(input_url): 
        temp_urls = set() 
        current_url_domain = urlparse(input_url).netloc 
    
        # Creates beautiful soup object to extract html tags 
        beautiful_soup_object = BeautifulSoup( 
            requests.get(input_url).content, "lxml") 
    
        # Access all anchor tags from input  
        # url page and divide them into internal 
        # and external categories 
        for anchor in beautiful_soup_object.findAll("a"): 
            href = anchor.attrs.get("href") 
            if(href != "" or href != None): 
                href = urljoin(input_url, href) 
                href_parsed = urlparse(href) 
                href = href_parsed.scheme 
                href += "://"
                href += href_parsed.netloc 
                href += href_parsed.path 
                final_parsed_href = urlparse(href) 
                is_valid = bool(final_parsed_href.scheme) and bool( 
                    final_parsed_href.netloc) 
                if is_valid: 
                    if current_url_domain not in href and href not in links_extern: 
                        print("Extern - {}".format(href)) 
                        links_extern.add(href) 
                    if current_url_domain in href and href not in links_intern: 
                        print("Intern - {}".format(href)) 
                        links_intern.add(href) 
                        temp_urls.add(href) 
        return temp_urls 
    
    
    if(depth == 0): 
        print("Intern - {}".format(input_url)) 
    
    elif(depth == 1): 
        level_crawler(input_url) 
    
    else: 
        queue = [] 
        queue.append(input_url) 
        for j in range(depth): 
            for count in range(len(queue)): 
                url = queue.pop(0) 
                urls = list(level_crawler(url))
                queue.extend(urls)

    return links_intern, links_extern



if __name__ == "__main__":
    links_intern, links_extern = get_n_hop_links(depth=5,input_url='https://docs.nvidia.com/cuda/')

    df = pd.DataFrame(links_intern,columns=['links'])
    df.to_csv('links.csv',index=False)