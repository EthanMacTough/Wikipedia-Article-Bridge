import requests
import time
from requests.exceptions import RequestException, Timeout

# Necessary header for requesting into Wikipedia
# Due to stricter bot enforcing, requests without a User-Agent header will be Forbidden
HEADERS = {
    "User-Agent": (
        "Wikipedia-Article-Bridge/1.0 "
        "(https://github.com/EthanMacTough/Wikipedia-Article-Bridge)"
    )
}

# Session for requesting into API with
session = requests.Session()
session.headers.update(HEADERS)

# Caching sets to store pre-searched articles and their category sets
api_cache = {}

# Function for getting an array of titles as the result of a search query.
def searchArr(r):
    try:
        data = r.json()
    except ValueError:
        return []

    opt = []
    for link in data.get('pages', []):
        opt.append(link['title'])

    return opt

# Function for having the user choose an article if the one they entered was not valid.
def searchForArticle(search):
        
    r = requests.get(
        url=('https://en.wikipedia.org/w/rest.php/v1/search/' +
            'title?q=' + search + 
            '&limit=5'),
        headers=HEADERS
    )
    
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

# Function to fetch the children and categories of an article by its title
# Replaces the need for Beautiful Soup though calling the Wikipedia API instead
def fetch_page_api(title):
    
    # Checks cache first to make sure it hasn't already been grabbed
    if title in api_cache:
        return api_cache[title]

    # API Parameters to grab a JSON list of links and categories
    params = {
        "action": "query",
        "format": "json",
        "prop": "links|categories",
        "titles": title,
        "plnamespace": 0,
        "pllimit": "max",
        "cllimit": "max",
        "redirects": 1
    }

    plcontinue = None
    clcontinue = None

    while True:

        if plcontinue:
            params["plcontinue"] = plcontinue
        if clcontinue:
            params["clcontinue"] = clcontinue

        # If request fails, try one more time before skipping altogether
        for attempt in range(2):
            try:
                # API get request
                r = session.get(
                    "https://en.wikipedia.org/w/api.php",
                    params=params,
                    timeout=(10)
                )
                r.raise_for_status()
                break

            # Timeout Exception Handling
            except (Timeout, RequestException) as e:

                if attempt == 1:
                    api_cache[title] = ([], set())
                    return [], set()

        # Small Delay
        time.sleep(0.05)

        # Parse JSON data
        root = r.json()
        pages = root.get("query", {}).get("pages", {})
        data = next(iter(pages.values()), {})

        # Extract links
        links = []
        for link in data.get("links", []):
            title = link["title"]
            links.append({
                "title": title,
                "href": "/wiki/" + title.replace(" ", "_")
            })

        # Extract categories
        categories = set()
        for cat in data.get("categories", []):
            name = cat["title"].replace("Category:", "").lower()
            categories.add(name)

        cont = root.get("continue")
        if not cont:
            break

        plcontinue = cont.get("plcontinue")
        clcontinue = cont.get("clcontinue")


    # Cache title data for later use
    api_cache[title] = (links, categories)
    return links, categories
