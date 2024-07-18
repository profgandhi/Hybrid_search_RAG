# Imports
import asyncio
import aiohttp
import pandas as pd
import html2text
from tqdm import tqdm
tqdm.pandas()

import nest_asyncio
nest_asyncio.apply()


#------------------------------ Functions ----------------------------------------
def parse(html_content):
    """
    Parses HTML content and extracts text using html2text.

    Args:
    - html_content (str): A string containing HTML content.

    Returns:
    - str: Extracted text from the HTML content.
    """
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    text = h.handle(html_content)
    return text

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            html = await response.text()
            #text = await parse(html)
            return html
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None
    except asyncio.TimeoutError:
        print(f"Request to {url} timed out")
        return None
    


async def fetch_all(urls, max_concurrent):
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch(session, url) for url in urls] 
        texts = await asyncio.gather(*tasks,return_exceptions=True)
        return texts

#----------------------------------------------------------------------------------

# Chunk links in groups of 5000

if __name__ == "__main__":

    # Get links to retrive
    urls = pd.read_csv('links.csv')['links'].tolist()

    # Get HTML in chunks of 5000 
    print('Getting HTML')
    for i in range(0,6):
        chunked_url = urls[5000*i:5000*(i+1)]
        content = await fetch_all( chunked_url, max_concurrent=100)
        df = pd.DataFrame({'docs': content})
        df['links'] = urls[5000*i:5000*(i+1)]
        df.to_csv(f'docs{i}.csv',index=False)

        del content
        del df 

    print('Parsing Docs')
    # Parse Docs
    for i in range(0,6):
        df = pd.read_csv(f'docs{i}.csv')
        df['parsed_docs'] = df['docs'].progress_apply(lambda x: parse(str(x)))
        df.to_csv(f'parsed_docs{i}.csv',index=False)
        del df
