from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


browser = webdriver.Edge("edgedriver_win32\msedgedriver.exe")

cardLinks = set()


def getLinks(url):
    browser.get(url)

    pageNumbers = browser.find_elements(By.CLASS_NAME, "page-numbers")

    pageLinks = []
    for page in pageNumbers:
        link = page.get_attribute('href')
        pageLinks.append(link)

    if pageLinks:
        pageLinks.remove(None)

    cards = browser.find_elements(By.CLASS_NAME, "cardGridCell")

    links = []

    for card in cards:
        a = card.find_element(By.TAG_NAME, 'a')
        link = a.get_attribute('href')
        links.append(link)

    for page in pageLinks:
        browser.get(page)
        cards = browser.find_elements(By.CLASS_NAME, "cardGridCell")
        for card in cards:
            a = card.find_element(By.TAG_NAME, 'a')
            link = a.get_attribute('href')
            links.append(link)

    counter = 0

    for link in links:
        browser.get(link)

        cardFront = browser.find_element(By.ID, 'CardLeft')
        a = cardFront.find_element(By.TAG_NAME, 'a')
        imgFront = a.get_attribute('href')

        cardBack = browser.find_element(By.ID, 'CardRight')
        a = cardBack.find_element(By.TAG_NAME, 'a')
        imgBack = a.get_attribute('href')


        cardLinks.add(imgFront)
        cardLinks.add(imgBack)


        counter += 1
        print("Searched {x}/{y} images in {z}".format(x = counter, y = len(links), z=url), end='\r')



def getImages():
    print("\n====================== Links to {x} images ======================".format(x = len(cardLinks)))
    for count, cardLink in enumerate(cardLinks):
        print(count+1, '\t->\t', cardLink)
    print("============================================================")
    count = 0

    size = len(cardLinks)
    while cardLinks:
        print("Downloading {x}/{y} images".format(x = count+1, y = size), end='\r')
        imgLoad = requests.get(cardLinks.pop())

        cardPath = 'cards/' + imgLoad.url[49:]

        with open(cardPath, 'wb') as f:
            f.write(imgLoad.content)
        count += 1



    browser.close()



f=open("links.txt", 'r')
for url in f:
    getLinks(url)


getImages()

print("\n====================== Finished ======================")

browser.quit()
f.close()