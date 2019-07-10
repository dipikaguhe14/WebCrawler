import threading
from queue import Queue
from spider import spider
from domain import *
from general import *

PROJECT_NAME=raw_input()
HOME_PAGE=raw_input()
DOMAIN_NAME=get_domain_name(HOME_PAGE)
QUEUE_FILE=PROJECT_NAME+'queue.txt'
CRAWLED_FILE=PROJECT_NAME+'crawled.txt'
NUMBER_OF_THREADS=5
q=Queue()
#this thread will stop working only when main thread ends. 
def createworkers():
        for _ in range(NUMBER_OF_THREADS):
                t=threading.Thread(target=work)
                t.daemon=True
                t.start()
#here Queue is thread queue
def work():
        while True:
                url=q.get()
                spider.crawl_page(threading.current_thread().name,url)
                q.task_done()


#each Queue is assigned new job
def create_job():
        for link in file_to_set(QUEUE_FILE):
                q.put(link)
        q.join()
        crawl()
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_job()
createworkers()
crawl()
