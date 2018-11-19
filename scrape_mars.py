import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_data():
    try:
        # Scrape latest title/paragraph from NASA Mars News site
        browser = init_browser()
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')

        slide = soup.find('div', class_='image_and_description_container')
        news_title = slide.find('h3').text
        news_teaser = slide.find('div', class_='article_teaser_body').text

        # Scrape featured image from JPL Mars Space Images site
        url = 'https://www.jpl.nasa.gov/spaceimages/'
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')

        container = soup.find('div', class_='carousel_container')
        style = container.find('article', class_='carousel_item')['style']
        str = style.replace("background-image: url('/spaceimages/","")
        str = str.replace("');","")
        jpl_image = url + str

        # Scrape latest weather report from NASA Mars Twitter page
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')

        timeline = soup.find('div', class_='ProfileTimeline')
        tweets = timeline.find_all('p', class_='tweet-text')
        weather = tweets[0].text

        # Scrape Mars facts table from space facts site
        url = 'https://space-facts.com/mars/'
        tables = pd.read_html(url)
        df = tables[0]
        df.columns = ['Description', 'Value']
        df.set_index('Description', inplace=True)
        df.index.name = None

        html = df.to_html()
        fact_table = html.replace('\n', '')

        # Scrape HD images of each of Mar's hemispheres from USGS Astrogeology site
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')

        results = soup.find('div', class_='collapsible results')
        items = results.find_all('div', class_='item')
        hemispheres = []
        for item in items:
            desc = item.div.a.h3.text
            title = desc.replace(' Enhanced','')
            browser.click_link_by_partial_text(desc)
            soup = BeautifulSoup(browser.html, 'html.parser')
            dl = soup.find('div', class_='downloads')
            img_url = dl.ul.li.a['href']
            dict = {
                'title': title,
                'img_url': img_url
            }
            hemispheres.append(dict)
            browser.click_link_by_partial_text('Back')
        browser.quit()

        # Store data in a dictionary
        mars_data = {
            "news_title": news_title,
            "news_teaser": news_teaser,
            "jpl_image": jpl_image,
            "weather": weather,
            "fact_table": fact_table,
            "hemispheres": hemispheres
        }

        return mars_data
    except Exception as e:
        print(e)
        return 'err'