import func
import graph
import heapq
import sys

# Stack to determine the next article to search from
# Structure: [(priority, article title, search depth)]
search_queue = []

# Global array to store the target article's categories
target_categories = set()

# Global graph object to direct the search.
article_tree = graph.graph()

# Function to reset all used variables when searching more than once
def reset():
    global search_queue 
    search_queue = []

    global article_tree 
    article_tree = graph.graph()

# Function to determine the priority of an article in the queue
def find_priority(title, article_categories, depth):

    # Weights for priority
    CATEGORY_WEIGHT = 3
    TITLE_WEIGHT = 5
    DEPTH_WEIGHT = 1

    priority = 0

    # Category overlap
    overlap = len(article_categories & target_categories)
    priority -= CATEGORY_WEIGHT * overlap

    # Title similarity
    target_title = end_title
    article_title = title.lower().replace('_', ' ')

    if target_title in article_title:
        priority -= TITLE_WEIGHT

    # Depth bias (prefer shorter paths)
    priority += DEPTH_WEIGHT * depth

    return priority

# Function to search through one parent article's children for the searched article.
def searchChildren(links, end_title, depth):

    for article in links:

        href = article['href']
        title = article['title']

        # Returns False if the article exists in the tree
        isNewArticle = article_tree.insertNode(title)

        # Check for final match
        if (end_title.lower() == title.lower()):
            article_tree.printTrace()
            return True

        if isNewArticle:

            # Because of the speed of lower depth values, the first few passes will be in canonical order
            if (depth >= 1):

                # Determine categories of article
                child_titles, child_categories = func.fetch_page_api(title)

                # Check 1 depth in to see if a child has the end in it
                if any(link["title"].lower() == end_title.lower() for link in child_titles):
                    article_tree.newParent(title)
                    article_tree.insertNode(end_title)
                    article_tree.printTrace()
                    return True

                # Determine priority of article
                priority = find_priority(title, child_categories, depth + 1)
            else:
                priority = depth

            # If queue becomes too large, irrelevant articles are not stored
            if not (priority >= 5 and len(search_queue) > 500):
                heapq.heappush(search_queue, (priority, title, depth + 1))
                
            article_tree.printTrace()
            
    return False

# Article to initiate and direct the search.
def findPath(local_start_title, local_end_title):

    # Initialize start and end title as global variable
    global end_title
    end_title = local_end_title
    global start_title
    start_title = local_start_title

    # Initialize target categories
    target_categories.clear()
    _, categories = func.fetch_page_api(end_title)
    target_categories.update(categories)
    
    heapq.heappush(search_queue, (0, start_title, 0))
    article_tree.start_graph(start_title)

    found = False

    while not (found):

        # Check for empty queue
        if not search_queue:
            print("\nSearch failed: queue exhausted.")
            sys.exit()

        # Articles will be searched through in order of priority
        _, current_title, depth = heapq.heappop(search_queue)
        article_tree.newParent(current_title)

        # Create list of links for the currently searched article
        links, _ = func.fetch_page_api(current_title)

        found = searchChildren(links, end_title, depth)

    print('')
