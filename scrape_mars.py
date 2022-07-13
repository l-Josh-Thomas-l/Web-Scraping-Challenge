from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Mars News Scrape
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_paragrah = slide_elem.find('div', class_='article_teaser_body').get_text()

    browser.quit()


    # JPL Mars Space Images (Featured Images) Scrape
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    browser.quit()


    # Mars Facts Scrape
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://galaxyfacts-mars.com'
    mars_facts_df = pd.read_html(url)[0]
    mars_facts_df.columns=['Description', 'Mars', 'Earth']
    mars_facts_df = mars_facts_df.drop([0])
    mars_facts_df = mars_facts_df.set_index('Description')

    Facts_HTML = mars_facts_df.to_html()

    browser.quit()
   

   # Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []

    html = browser.html
    img_soup = soup(html, 'html.parser')

    for x in range(4):
        browser.find_by_css('div[class="description"] a')[x].click()
        html = browser.html
        img_soup = soup(html, 'html.parser')
    
        title = img_soup.find('h2', class_='title').get_text()
    
        link = img_soup.find(lambda tag:tag.name=="a" and "Sample" in tag.text)
        img_url = link.get('href')
    
        hemisphere = {}
        hemisphere['img_url'] = img_url
        hemisphere['title'] = title
        hemisphere_image_urls.append(hemisphere)
    
        browser.back()

    title1 = hemisphere_image_urls[0]["title"]
    image1 = hemisphere_image_urls[0]["img_url"]
    
    title2 = hemisphere_image_urls[1]["title"]
    image2 = hemisphere_image_urls[1]["img_url"]

    title3 = hemisphere_image_urls[2]["title"]
    image3 = hemisphere_image_urls[2]["img_url"]

    title4 = hemisphere_image_urls[3]["title"]
    image4 = hemisphere_image_urls[3]["img_url"]


    # Final dictionary for Mongo
    final_mars_data = {
    "latest_title": news_title,
    "latest_paragraph" : news_paragrah,
    "featured_image": img_url,
    "html_table": Facts_HTML,
    "hemisphere_scrape": hemisphere_image_urls,
    "title1": title1,
    "title2": title2,
    "title3": title3,
    "title4": title4,
    "image1": image1,
    "image2": image2,
    "image3": image3,
    "image4": image4,}

    return final_mars_data  

print(scrape())