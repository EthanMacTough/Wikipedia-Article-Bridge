import time
import datetime

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

    # Function that sets the starting values for the search.
    def start_graph(self, start_title):
        self.start = Node(start_title, None)
        self.totalArr.append(self.start)
        self.currentParent = self.start
        self.head = self.start

    # Function to insert a new article into the current set parent.
    def insertNode(self, title):

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
        temp = None

        for p in self.totalArr:
            if (p.title == title):
                temp = p
        
        self.currentParent = temp

    # Function to display progress in the search.
    def printTrace(self):
        printArr = []

        temp = self.head
        while (temp != None):
            printArr.insert(0, temp.title)
            temp = temp.parent
        
        j = len(printArr)
        if (j >= 0):
            p = ''

            for i in range(0, j):
                strin = printArr[i]
                if (len(strin) >= 40):
                    strin = strin[:36] + '...'

                p = p +'[' + strin + ']'

                if (i != j - 1):
                    p = p + ' --> '
                if ((i + 1) % 4 == 0 and i != 0 and i < j):
                    self.enterNum += 1
                    p = p + '\n'

            # '\x1b[1A' moves the console's cursor one line up.
            # '\x1b[2K' erases the current line in stdout.
            # Using a combination of '\r', cursor moving and erasure, I can replace old data with new data on the same line.
            print('\x1b[1A' * (4 + self.enterNum), end='\r')

            dTime = (datetime.datetime.now() - self.startTime)
            sec = dTime.seconds
            if (sec < 3600):
                timeStr = f'{int(sec / 60):02}:{((sec) % 60):02}'
            else:
                timeStr = f'{int(sec / 3600):02}:{int((sec % 3600) / 60):02}:{(sec % 60):02}'

            print('\x1b[2K Time Elapsed: ' + timeStr + '\r')

            print('\x1b[2K Articles Searched: ' + str(self.count) + '\r\n')
            print('\x1b[2K' + p)

            self.enterNum = 0
            time.sleep(0.01)
