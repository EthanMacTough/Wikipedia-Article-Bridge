import requests
from bs4 import BeautifulSoup
import json

# Function for deciding whether a link is valid or not.
def validLink(link):
    if (link.startswith('/wiki')):

        link = link.split('/wiki/')[1]
        return not (
            link.startswith('File:') or
            link.startswith('Special:') or
            link.startswith('Category:') or
            link.startswith('Help:') or
            link.startswith('Wikipedia:') or
            link.startswith('Template:') or
            '(disambiguation)' in link
        )
    else: return False

# Function for getting an array of HREF and Title children of an article soup.
def getArr(b):

    opt = []

    allLinks = b.find(id="bodyContent").find_all("a")

    for link in allLinks:
        if not ('href' in link.attrs):
            continue
        if not validLink(link['href']): 
            continue
        opt.append(link) 

    return opt

# Function for getting an array of titles as the result of a search query.
def searchArr(r):
    opt = []

    soup = BeautifulSoup(r.content, 'html.parser')

    allLinks = json.loads(soup.text)

    for link in allLinks['pages']:
        opt.append(link['title'])

    return opt

# Function for having the user choose an article if the one they 
# entered was not valid.
def searchForArticle(search):
        
    r = requests.get(
        url=('https://en.wikipedia.org/w/rest.php/v1/search/' +
            'title?q=' + search + 
            '&limit=5'))
    
    response = searchArr(r)

    resNum = len(response)

    if (resNum > 0):
        print("Article Name '" + search + "' Does not Exist. Did you Mean...")
        print('=' * 100)

        for i in range(1, len(response)+1 ):
            print(' ' + str(i) + ') ' + response[i-1])
        print('=' * 100 + '\n')

        res = int(input('Enter Choice (1-5): '))
        print('')

        # Even though spaces (%20) work in the URL of the response, for the sake of
        # consistency in searching, they will be replaced with an underscore.
        return 'https://en.wikipedia.org/wiki/' + response[res-1].replace(' ', '_')
    else:
        print("Article Name '" + search + "' Could not be Found.")
        print('=' * 100)
        newTitle = input('\n Please Type Another Title: ')
        print('')

        return 'https://en.wikipedia.org/wiki/' + newTitle.replace(' ', '_')


# Function to gain a BeautifulSoup object from the HREF of an article
def soupByURL(url):
    r = requests.get(
        url = "https://en.wikipedia.org/wiki/" + url
    )

    soup = BeautifulSoup(r.content, 'html.parser')
    return soup
