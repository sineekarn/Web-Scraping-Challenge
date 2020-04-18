#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
from pprint import pprint
import re


def scrape():
      
        # # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
        # get_ipython().system('which chromedriver')

        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=True)
        


        # # NASA Mars News

        # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title     and Paragraph Text. 
        # Assign the text to variables that you can reference later.

        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)


        # Html object
        html = browser.html


        # Create a Beautiful Soup object / Parse the HTML using the Beautiful Soup library
        soup = bs(html, 'html.parser')
        # print(soup.prettify())


        # Retrieve the latest element that contains news title
        news_find = soup.find("ul", class_="item_list")
        news_title = news_find.find("div", class_="content_title").text
        # Display scrapped data 
        print(news_title)


        # Retrieve the latest element that contains news_paragraph
        news_pg = soup.find("div", class_="article_teaser_body").text

        # # Display scrapped data 
        print(news_pg)


        # # JPL Mars Space Images - Featured Image


        # Use splinter to navigate the site 
        space_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(space_image_url)


        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_image, "html.parser")

        # Retrieve full size `.jpg` background-image url from style tag attribute for the current Featured           Mars Image 
        image_path  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')   [1:-1]

        # Website Url 
        featured_image_url = "https://www.jpl.nasa.gov" + image_path

        # Display full link to featured image
        featured_image_url


        # # Mars Weather

        # Use splinter to navigate Mars Weather Twitter 
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.driver.set_window_size(1000,8000)
        browser.visit(weather_url)
        time.sleep(8)


        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_weather, 'html.parser')

        results = soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
        print(results)
        # scrape the latest Mars weather tweet from the page.
        mars_weather = [v.text for v in results if "gusting" in v.text]
        print(mars_weather[0]) 
        

        # # Mars Facts

        # Use splinter to navigate Mars Facts webpage
        fact_url = "https://space-facts.com/mars/"
        # browser.visit(url)

        # Use Pandas to "read_html" 
        table = pd.read_html(fact_url)
        table[0]


        table_df = table[0].to_html(classes = 'table table-striped', index = False, header = False)
        print(table_df)


        # # Mars Hemispheres

        # Visit hemispheres website through splinter module 
        hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='description')
        items

        main_url = "https://astrogeology.usgs.gov"

        hemisphere_titles_image_urls = []

        for i in items:
            page_url = main_url + i.find("a")['href']
            browser.visit(page_url)
            page_url_soup = bs(browser.html, 'html.parser')
            hemispheres_image_url = page_url_soup.find("ul").find("a")['href']
            hemispheres_title = page_url_soup.find("h2", class_="title").text
            hemisphere_titles_image_urls.append({"Title": hemispheres_title, "Image_Url": hemispheres_image_url})

        hemisphere_titles_image_urls
    
        mission_to_mars = {
        "news_title": news_title,
        "news_pg": news_pg,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather[0],
        "table_df": table_df,
        "hemisphere_titles_image_urls": hemisphere_titles_image_urls
        }
        return mission_to_mars
