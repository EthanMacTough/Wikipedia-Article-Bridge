# Wikipedia Article Bridge

Based on the [Wiki Game](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game), a competition where players start at any given Wikipedia article, and try to find the goal article by clicking on article body links.

This Python project implements a [Best-First Search](https://en.wikipedia.org/wiki/Best-first_search) algorithm that finds a navigation path between two user-input Wikipedia articles. It makes use of Python's [Requests](https://pypi.org/project/requests/) library to call Wikipedia's dedicated API to search through an article's outgoing links (or 'child' articles). The code is thoroughly documented with comments and split across several Python files. When running the project locally, run the WikipediaSearch.py file in a terminal.

<img width="728" height="284" alt="image" src="https://github.com/user-attachments/assets/f69dc8a9-40e1-4399-8e55-dc10dc70287f" />

## Algorithm Overview
When two articles are entered, the program finds all children available in the starting article, and determines the most relevant article to explore next. It will repeat this process until the destination article is found.

The algorithm is modeled as a directed graph in which each node represents a Wikipedia article, and each edge represents an in-article link from one page to another. Starting from a source article, the algorithm searches this graph to reach a target article using a best-first strategy.

The search is directed by a priority queue (min-heap). At each step, the article with the lowest heuristic score is expanded, and its outgoing links are added to the queue if they have not been visited previously.

Article prioritization is determined using a combination of heuristics:
- Category Overlap: Articles that share more Wikipedia categories with the destination article are prioritized, under the assumption that related topics are more likely to lead toward the goal.
- Title Similarity: Articles whose titles partially match the destination title receive a priority boost, favoring semantically related pages.
- Depth Bias: Shallower paths are preferred to discourage unnecessarily deep exploration.

Unlike a traditional [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search), this approach does not guarantee a shortest path. However, it dramatically reduces the number of articles explored in practice, allowing the search to complete within a reasonable time for many real-world article pairs.

The algorithm is designed to run within real-world constraints. Wikipedia API requests are cached, redirects are resolved automatically, and network timeouts are handled gracefully by skipping failed articles rather than terminating the search. An early-exit check is also used to detect when the destination article appears one link away from the current node, allowing the search to terminate sooner when possible.


## Runtime Article Search
Another feature worth mentioning is the usage of Wikipedia's built-in search algorithm. If an entered article does not exactly match the URL of a Wikipedia article, the program will prompt the user to select one of five similar titles to use instead.

![{628E7783-9CEA-427F-8C82-54BE50E2691B}](https://github.com/user-attachments/assets/deedd2b1-1117-4b5a-84e1-b5ba8a30456e)
![{D238E585-2283-4EB6-BEDB-3DB71B303121}](https://github.com/user-attachments/assets/08e966e0-00ec-43ed-8517-2d4d8f03e649)

Because Wikipedia's search button is a GET request that returns a JSON response, I can use that in Python to manually get an array of titles that are valid Wikipedia articles.

##
This project was updated to replace the Breadth-First Search algorithm that initialized the concept. It no longer guarantees a shortest-path destination between articles, but runs fast enough to be practically usable, which could not be said about the previous version.
