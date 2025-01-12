import func
import graph

# Stack to determine the next article to search from
search_queue = []

# Global graph object to direct the search.
article_tree = graph.graph()

# Function to reset all used variables when searching more than once
def reset():
    global search_queue 
    search_queue = []

    global article_tree 
    article_tree = graph.graph()

# Function to search through one parent article's children for the searched article.
def bfs(node, end):

    # Get array of children from the current node
    arr = func.getArr(node)

    for article in arr:

        href = article['href']
        title = article['title']

        visited = article_tree.insertNode(title)

        if visited:
            search_queue.append(title)
                
            article_tree.printTrace()
            if (end.lower() == href.lower()):
                return True
            
    return False

# Article to initiate and direct the search.
def findShortestPath(start_title, end):
    
    search_queue.append(start_title)
    article_tree.start_graph(start_title)

    found = False

    while not (found):

        # Articles will be searched through in order of time, in order to find the shortest path.
        article_tree.newParent(search_queue[0])

        # Pop a new article from the list and create a BeautifulSoup object from it
        node = func.soupByURL(search_queue[0])
        search_queue.pop(0)

        found = bfs(node, end)

    print('')
