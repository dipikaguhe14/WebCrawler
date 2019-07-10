from urllib2 import urlopen
from link_finder import link_finder
from domain import *
from  general import *
#grab the link from the waiting list 
#parse the page using link_finder
class spider:
    project_name=''
    base_url=''
    crawled_file=''
    queue_file=''
    domain_name=''
    crawled=set()
    queue=set()
    def __init__(self,project_name,base_url,domain_name):
        spider.base_url=base_url
        spider.project_name=project_name
        spider.domain_name=domain_name
        spider.crawled_file=spider.project_name+'/crawled.txt'
        spider.queue_file=spider.project_name+'/queue.txt'
        self.boot()
        self.crawl_page('First_Spider',spider.base_url)
    @staticmethod
    def boot():
        print spider.project_name
        create_project_dir(spider.project_name)
        create_data_files(spider.project_name,spider.base_url)
        spider.queue=file_to_set(spider.queue_file)
        spider.crawled=file_to_set(spider.crawled_file)
    @staticmethod
    def crawl_page(thread_name,page_url):
        if page_url not in spider.crawled:
            print(thread_name+' is crawling currently '+page_url)
            print('wating queue: '+str(len(spider.queue))+' |crawled queue: '+str(len(spider.crawled)))
            spider.add_links_to_queue(spider.gather_links(page_url))
            spider.queue.remove(page_url)
            spider.crawled.add(page_url)
            spider.update_file()
    @staticmethod
    def gather_links(page_url):
        #print page_url
        html_string=''
        try:
            #print 'hello'
            response=urlopen(page_url)
            #print response.getheader('Content.Type')
            
            if 'text/html' in response.getheader('Content-Type'):
                #print 'hello'
                html_bytes=response.read()
                html_string=html_bytes.decode('utf-8')
            finder=link_finder(spider.base_url,page_url)
            finder.feed(html_string)
        except:
            print('can not crawl this page')
            return set()
        return finder.page_links()
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in spider.queue:
                continue
            if url in spider.crawled:
                continue
            if spider.domain_name not in url:
                continue
            spider.queue.add(url)
    @staticmethod
    def update_file():
        set_to_file(spider.queue,spider.queue_file)
        set_to_file(spider.crawled,spider.crawled_file)


