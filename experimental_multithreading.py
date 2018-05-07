#%%
import urllib
from queue import Queue, Empty
from threading import Thread
THREAD_POOL_SIZE = 8

def fetch_image(url):
    
    name = urllib.parse.urlsplit(url).path.split(sep = "/")[-1]
    
    urllib.request.urlretrieve(url, name)

def worker(work_queue):
    
    while not work_queue.empty():
        
        try:
            
            item = work_queue.get(block=False)
            
        except Empty:
            
            break
        
        else:
            
            fetch_image(item)
            work_queue.task_done()
 
def main(urls):
    
    work_queue = Queue()
    
    for u in urls:
        
        work_queue.put(u)

    threads = [
            
            Thread(target=worker, args=(work_queue,))
            for _ in range(THREAD_POOL_SIZE)
            
            ]
    
    for thread in threads:
        
        thread.start()
        
        work_queue.join()
        
    while threads:
        
        threads.pop().join()
        
ur = list(df.imageUrl.values)
#%time main(ur)


def loop(urls):
    
    for url in urls:
        
        fetch_image(url)
        
%time main(ur)
    
