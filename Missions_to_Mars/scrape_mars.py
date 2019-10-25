from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import os

import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path ={"executable_path":"c:/Users/ai3ca/web-scraping-challenge/Missions_to_Mars/chromedriver"}
   
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_all={}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")


    #scrape latest news 
    title= soup.find("div", class_="content_title").text
    paragraph= soup.find("div", class_="article_teaser_body").text
    mars_all["News Title"]=title
    mars_all["News Paragraph"]=paragraph
    
    # scrape the image
    image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    #Getting the base url
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(image_url))
    print(base_url)
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    url_image = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = base_url + url_image
    print(featured_image_url)
    mars_all["featured_image"]=featured_image_url
    
    # scrape the weather data
    
    weather_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html_weather= browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_all["weather"]=mars_weather
    
    # scrape the fact data
    
    fact_url="https://space-facts.com/mars/"
    browser.visit(fact_url)
    mars_table = pd.read_html(fact_url)
    mars_table[0]
    mars_df=mars_table[0]
    mars_df.columns=["Parameter","Mars","Earth"]
    mars_df.set_index(["Parameter"], inplace=True)

    mars_df
    mars_fact=mars_df.to_html(index=True,header=True)
    mars_fact=mars_fact.replace("\n","")
    mars_all["fact"]=mars_fact

    # mars hemisphere
    hemis_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)
    #Getting the base url
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(hemis_url))
    print(base_url)

    # create a empty for these hemisphere url
    all_urls=[]
    
    hemisphere_html = browser.html
    soup = bs(hemisphere_html, 'html.parser')
    image_list = soup.find_all('div', class_='item')
    # Loop through list of hemispheres 
    for image in image_list:
        hemisphere_dict = {}
        # Find link
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        # Visit the link
        browser.visit(link)
        # Parse the html of the new page

        hemisphere_html2 = browser.html
        soup2 = bs(hemisphere_html2, 'html.parser')
        
        # Find the title
        img_title = soup2.find('div', class_='content').find('h2', class_='title').text
        # Append to dict
        hemisphere_dict['Title'] = img_title
        # Find image url
        img_url = soup2.find('div', class_='downloads').find('a')['href']
        # Append to dict
        hemisphere_dict['URL_IMG'] = img_url

        # Append dict to list

        all_urls.append(hemisphere_dict)

    mars_all["hemisphere_img_url"] = all_urls


    return mars_all




    
 
