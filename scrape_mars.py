# Import dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # Call the init_browser function (otherwise browser.visit won't work!!!)
    browser =  init_browser()

    mars_facts = {}
    ## NASA Mars News 

    # URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(news_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # Collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    news_title = soup.find('div', class_="content_title").find('a').text
    news_p = soup.find('div', class_="rollover_description_inner").text
    mars_facts['news_title'] = news_title
    mars_facts['news_p'] = news_p

    ## JPL Mars Space Images - Featured Image

    # URL to visit and open with Splinter
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = (jpl_url.split('/spaceimages'))[0]
    browser.visit(jpl_url)

    # HTML object
    jpl_html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(jpl_html, 'html.parser')
    # Retrieve the image URL
    image = soup.find('article', class_='carousel_item')["style"]

    # Get unique image URL
    featured_image_url = base_url + '/spaceimages/images/wallpaper/PIA19920-1920x1200.jpg'
    mars_facts['featured_image_url'] = featured_image_url

    ## Mars weather

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    # HTML object
    weather_html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(weather_html, 'html.parser')
    # Retrieve text contained in first tweet
    tweet = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_facts['mars_weather'] = tweet

    # Mars facts

    # pass the URL
    facts_url = "https://space-facts.com/mars/"

    # read the URL using read_html. This will find any table structures in the HTML
    # There is only one table on this page, shown below
    tables = pd.read_html(facts_url)
    tables

    # pass to a DataFrame
    df = tables[0]
    df.columns = ['Fact', 'Value']
    df.head()

    # set first column as Index
    df.set_index('Fact', inplace=True)
    df.head()

    # convert to HTML table string
    html_table = df.to_html()
    html_table

    # replace '/n' with ''
    html_table.replace('\n', '')

    mars_facts['html_table'] = html_table

    ## Mars hemispheres

    # Mars Hemispheres URL
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    # Split the base_url
    base_hemispheres_url = (hemispheres_url.split('/search'))[0]
    base_hemispheres_url

    # List to hold hemisphere image URLs
    hemisphere_image_urls = []

    # Find the class to that holds each hemisphere info
    hemispheres = soup.find_all('div', class_='description')

    # For loop to extract info for each hemisphere
    for hemisphere in hemispheres:
        
        # Create dictionary to hold title and URL
        hemisphere_title_url = {}  
        
        # Find the title and remove "Enhanced"
        hemisphere_title = hemisphere.find('h3').text
        hemisphere_title_url['title'] = hemisphere_title.split(' Enhanced')[0]
        
        # Find the html route to each page
        route = hemisphere.find('a', class_='itemLink product-item')['href']
        individual_hemisphere_route = base_hemispheres_url + route
        browser.visit(individual_hemisphere_route)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_image_url = soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        
        # Image URL added to dictionary
        hemisphere_title_url['image_url'] = hemisphere_image_url
        
        # Dictionary added to list
        hemisphere_image_urls.append(hemisphere_title_url)
        
        mars_facts['hemisphere_image_urls'] = hemisphere_image_urls
    
    browser.quit()

    return mars_facts






