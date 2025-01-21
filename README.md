# Wikipedia Article Bridge

Based on the [Wiki Game](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game), a competition where players start at any given Wikipedia article, and try to find the goal article by clicking on article body links.

This Python project is a Shortest Path BFS algorithm that finds the bridge between two user-input Wikipedia articles. It makes use of Python's [Requests](https://pypi.org/project/requests/) and [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) libraries to parse a Wiki article's HTML code and find "child" articles. Code is documented, and makes use of Object Orientation for easier reading.

![{6F889BD2-64D5-4D9C-BF35-33C843E3EC45}](https://github.com/user-attachments/assets/181627eb-50d7-4e66-9542-9a29d9d8b3ba)

When two articles are entered, the program finds all children available in the starting article, and searches for the end result in each new unique article page. This, of course, means the program has the potential to run at an exponential growth rate, and can easily search through 100,000 articles before finding a relatively longer bridge.

Another part of the code that I'm proud of is the usage of Wikipedia's built-in search algorithm! 

![{628E7783-9CEA-427F-8C82-54BE50E2691B}](https://github.com/user-attachments/assets/deedd2b1-1117-4b5a-84e1-b5ba8a30456e)
![{D238E585-2283-4EB6-BEDB-3DB71B303121}](https://github.com/user-attachments/assets/08e966e0-00ec-43ed-8517-2d4d8f03e649)

Because Wikipedia's search button is a GET request that returns a json webpage, I can use that in Python to manually get an array of titles that are valid Wikipedia articles.

Like mentioned above, the program has the capacity to run for a very long time, and is in no way the fastest way to bridge two articles. I may come back to this project later to implement a more effective search, but as of now, it serves more as a proof-of-concept for the automation of the Wiki Game.
