# WikiRacer

## Summary
Wikiracer is a Python command line tool to solve the WikiRace game. Specifically, the tool allows users to enter a source and destination topic; the tool returns a list of topics that form a path between the source and destination.

## Prerequisites
1. Python 3.6.5

## Installation
1. `virtualenv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python main.py 'Source' 'Destination'`

## Implementation
### MVP 1: A Synchronous BFS
The initial MVP included an API for a WikiTopic and a WikiGraph. A WikiGraph is instantiated with a start and end topic. An API call is made to MediaWiki for each topic's children, which are then added to the queue. A dictionary is used to keep track of each topic's parent. The queue continues until a current topic matches the destination. At this point, a path is traced backwards from the current topic to the source topic via the dictionary.

While this method ultimately found the shortest path, it was not optimized for speed. Each check in the BFS is sequential, rather than concurrent: the program must wait for a response from each API call before continuing to search.

### MVP 2: An Asynchronous BFS
To improve the speed, a few options became apparent: use multiple processes, use multiple threads or use coroutines with a single-threaded appraoch. Python3 offers an API for asynchronous programming and coroutines, Asyncio, so the last option was selected. Asyncio provides the interface to create asynchronous queues and event loops. Subsequent tasks can be initialized without waiting for responses from previous ones.

In the WikiRacer problem, the BFS is checking items from a queue to see if they match our destination; if the item does not, the BFS produces work (network requests to the MediaWiki API) that need to be queued up and completed. This begs the question - where will the network requests queue up?

With this model, we need two asynchronous queues - one for the BFS to check (WikiGraph) and one for a group of workers to fetch from the MediaWiki API (WikiFetcher). The latter (WikiFetcher) includes producers, which put topics on the queue, and workers, which pick up topics from the queue, send network requests and issue a callback on response. The callback, delineated by the WikiGraph, inserts the response (topic and list of child topics) into the graph.

This appraoch significantly improved the runtime, as the program is no longer waiting for one network request to complete at a time. Unfortunately, some duplicate work occurs. For example, two Wikipedia pages may have idential sub-links, both sub-links are queued up for network requests and completed. Once they return, the first response is recorded and the second simply replaces the original. While this does not impact accuracy of results, it is an unnecessary step.

### MVP 3: An Asynchronous Double-Ended BFS
In the previous two approaches, the BFS occurred from a single start point. This last appraoch instantiates two graphs, one from the start to the end topic and the other from the end topic to the start topic. The WikiGraph class was abstracted further for this flexibility. In this case, three asynchronous queues run: start graph's to_visit, end graph's to_visit and a single WikiFetcher's to_fetch.

Each graph is also passed it's opposing graph's came_from dictionary, which keeps track of visited/parent topics. Once a topic is visited that also exists in the opposing came_from dictionary, the program has successfully found a path, halfway on each graph.

The speed of the program is now 240x faster. The resulting path is not always the shortest however.

| MVP                                 | Time   |
| ------------------------------------|:------:|
| 1. A Synchronous BFS                |
| 2. An Asynchronous BFS              |
| 3. An Asynchronous Double-Ended BFS | 1.722s |