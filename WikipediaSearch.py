import requests
import func
import search
import sys

# Basic Functionality of BeautifulSoup and HTML usage:
    # 1: URL - Gained through user input or Wikipedia search algorithm
    # 2: HTML / HTTP Request - GET request through URL
    # 3: BeautifulSoup Object - html parser for request object
    # 4: Specified Array - Title or HREF array gained through selection from Soup

print('\n' + '=' * 100)
print(' -Wikipedia Article Bridge-')
print('=' * 100 + '\n\n')

while (True):

    # Even though spaces (%20) work in the URL of the response, for the sake of
    # consistency in searching, they will be replaced with an underscore.
    start_name = input(" Enter Starting Article Name - ")
    start_URL = "https://en.wikipedia.org/wiki/" + start_name.replace(' ', '_')

    end_name = input(" Enter Destination Article Name - ")
    end_URL = "https://en.wikipedia.org/wiki/" + end_name.replace(' ', '_')

    print('')

    # This loop is to make sure that both of the entered articles are valid Wikipedia pages.
    # If an entered article is not valid, the function file's search method will be called.
    while (True):

        response_S = requests.get(url=start_URL)
        if (response_S.status_code != 200):
            start_URL = func.searchForArticle(start_name)
            continue

        response_E = requests.get(url=end_URL)
        if (response_E.status_code != 200):
            end_URL = func.searchForArticle(end_name)
            continue
        break

    # Entered articles cannot both be the same article.
    if (start_URL == end_URL):
        print('Articles Are Identical. Please Enter Unique Article Names.\n')
        continue

    # We split the end URL as a destination for the response children to find.
    start_HREF = start_URL.split('.org')[1]
    start_title = start_HREF.split('/wiki/')[1].replace('_', ' ')
    end_HREF = end_URL.split('.org')[1]

    # ANSI Escape Codes are used several times throughout the project.
    # They are explained in more detail in graph.py, but I used this website for reference:
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797 
    print('\x1b[?25l-' * 100 + '\n\n\n' + '-' * 100 + '\n')

    search.reset()

    search.findShortestPath(start_title, end_HREF)

    print('\x1b[?25hBridge Found!\n')
    print('Search for Another?\n 1) Search Again\n 2) Quit\n')
    again = int(input('Enter Choice: '))

    if (again == 2):
        print('\nExiting...')
        sys.exit()
    elif (again == 1):
        print('')
        continue
    else:
        # When given two options, people will often pick the third.
        print('\nInvalid Input. Let\'s go again!')
        continue
