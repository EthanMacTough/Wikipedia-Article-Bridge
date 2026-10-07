import datetime
import time
import textwrap
import threading
import func

class Node:
    def __init__(self, title, parent):
        self.title = title
        self.parent = parent

class graph:

    start = None
    totalArr = []
    currentParent = None
    head = start
    enterNum = 0

    # The time elapsed is calculated by comparing the user's
    # computer time with the one saved when the program started.
    startTime = datetime.datetime.now()
    count = 1

    # Constructor for graph.
    def __init__(self):
        self.start = None
        self.totalArr = []
        self.currentParent = None
        self.head = self.start
        self.enterNum = 0

        self.startTime = datetime.datetime.now()
        self.count = 1
        self.outputLock = threading.Lock()
        self.timerThread = None
        self.renderedLines = 0

    # Function that sets the starting values for the search.
    def start_graph(self, start_title):
        with self.outputLock:
            self.start = Node(start_title, None)
            self.totalArr.append(self.start)
            self.currentParent = self.start
            self.head = self.start

    # Function to insert a new article into the current set parent.
    def insertNode(self, title):
        with self.outputLock:
            for p in self.totalArr:
                if (p.title == title):
                    return False

            temp = Node(title, self.currentParent)
            self.head = temp
            self.totalArr.append(temp)

            self.count += 1
            return True

    # Function to set a new current parent to add children to.
    def newParent(self, title):
        with self.outputLock:
            temp = None

            for p in self.totalArr:
                if (p.title == title):
                    temp = p
        
            self.currentParent = temp

    # Function to print the article path on a separately threaded timer.
    # This will make the timer in the output update every second even if the search is delayed.
    def _timer_loop(self, stop_event):
        while not stop_event.is_set():
            self.printTrace()
            if stop_event.wait(1):
                break

    # Function to start the timer loop thread.
    def start_timer(self):
        stop_event = threading.Event()
        self.timerThread = threading.Thread(
            target=self._timer_loop,
            args=(stop_event,)
        )
        self.timer_stop_event = stop_event
        self.timerThread.start()

    # Function to stop the timer loop thread.
    def stop_timer(self):
        if self.timerThread is not None:
            self.timer_stop_event.set()
            self.timerThread.join()
            self.timerThread = None

    # Function to display progress in the search.
    def printTrace(self):
        with self.outputLock:

            # Create an array of the path from the current article back to the starting node.
            printArr = []
            temp = self.head
            while (temp != None):
                printArr.insert(0, temp.title)
                temp = temp.parent

            # Begin parsing array to build output string
            j = len(printArr)
            if (j >= 0):

                # p is the string that will be printed to the console
                p = ''

                # Iterate through each array element to build string
                self.enterNum = 0
                for i in range(0, j):
                    strin = printArr[i]
                    if (len(strin) >= 40):
                        strin = strin[:36] + '...'

                    # If the string can be long enough to reach the edge of the terminal, a new line of nodes will be started.
                    if (len(p.split('\n')[self.enterNum] +'[' + strin + ']' + ' --> ') >= func.get_terminal_width()):
                        self.enterNum += 1
                        p = p + '\n'

                    p = p +'[' + strin + ']'

                    # Add an arrow between all nodes, excluding the final node in the path.
                    if (i != j - 1):
                        p = p + ' --> '

                    
                # Find the time elapsed since the start of the search and format it into a string.
                dTime = (datetime.datetime.now() - self.startTime)
                sec = int(dTime.total_seconds())
                if (sec < 3600):

                    # Format for time less than one hour (3600 seconds)
                    # MM:SS
                    timeStr = f'{int(sec / 60):02}:{((sec) % 60):02}'
                else:

                    # Format for time greater than or equal to one hour (3600 seconds)
                    # HH:MM:SS
                    timeStr = f'{int(sec / 3600):02}:{int((sec % 3600) / 60):02}:{(sec % 60):02}'


                # Build output string into an array of lines to print
                # Time Elapsed: HH:MM:SS
                # Articles Searched: XXXX
                # ----------------------------------------...
                lines = [
                    ' Time Elapsed: ' + timeStr,
                    ' Articles Searched: ' + str(self.count),
                    '-' * func.get_terminal_width()
                ]

                # Split the path string into lines that fit within the terminal width.
                for path_line in p.split('\n'):
                    lines.extend(textwrap.wrap(
                        path_line,
                        width=func.get_terminal_width(),
                        break_long_words=True,
                        break_on_hyphens=False
                    ) or [''])

                # '\x1b[1A' moves the console's cursor one line up.
                # '\x1b[2K' erases the current line in stdout.
                # Using a combination of '\r', cursor moving and erasure, I can replace old data with new data on the same line.
                for i in range(self.renderedLines if self.renderedLines > 0 else 4):
                    print('\x1b[2K\x1b[1A', end='\r')

                self.renderedLines = len(lines)
                for line in lines:
                    print('\x1b[2K' + line)

                # Adding a small delay makes strings that disappear too fast look cooler.
                time.sleep(0.01)