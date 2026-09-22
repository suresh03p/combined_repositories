import logging,threading,time;from concurrent.futures import ThreadPoolExecutor;from pathlib import Path;from urllib.request import urlopen;logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s');logger=logging.getLogger(__name__);class MyThread(threading.Thread):
    def __init__(self,n,d=0.2):super().__init__(name=n);self.d=d
    def run(self):logger.info('%s started',self.name);time.sleep(self.d);logger.info('%s finished',self.name)
class Counter:
    def __init__(self):self.v=0;self.l=threading.Lock()
    def add(self):
        with self.l:self.v+=1
class RCounter:
    def __init__(self):self.v=0;self.l=threading.RLock()
    def add(self):
        with self.l:self.v+=1;self._i()
    def _i(self):
        with self.l:self.v+=1
class EventDemo:
    def __init__(self):self.r=threading.Event();self.s=threading.Event()
    def worker(self):logger.info('Waiting');self.r.wait();logger.info('Started');self.s.wait(2);logger.info('Stopped')
class SemDemo:
    def __init__(self,l):self.s=threading.Semaphore(l)
    def access(self,n):
        with self.s:logger.info('%s got access',n);time.sleep(0.5);logger.info('%s released',n)
class QDemo:
    def __init__(self):self.q=[];self.l=threading.Lock()
    def produce(self,items):
        for i in items:
            with self.l:self.q.append(i);logger.info('Produced: %s',i)
    def consume(self):
        while True:
            with self.l:
                if not self.q:time.sleep(0.1);continue
                item=self.q.pop(0)
            if item is None:break
            logger.info('Consumed: %s',item)
def run_t():ts=[MyThread(f'T-{i}',0.2+i*0.1)for i in range(3)];[t.start()for t in ts];[t.join()for t in ts]
def run_p():
    with ThreadPoolExecutor(max_workers=3) as p:res=list(p.map(lambda x:x*x,[1,2,3,4]));logger.info('Pool: %s',res)
def run_d():t=threading.Thread(target=lambda:(time.sleep(0.5),logger.info('Daemon done')),daemon=True);t.start();t.join(timeout=0.2);logger.info('Main keeps going')
def run_e():d=EventDemo();t=threading.Thread(target=d.worker);t.start();time.sleep(0.5);d.r.set();time.sleep(0.5);d.s.set();t.join()
def run_l():c=Counter();rc=RCounter();
    def work():
        for _ in range(5):c.add();rc.add()
    ts=[threading.Thread(target=work)for _ in range(3)];[t.start()for t in ts];[t.join()for t in ts];logger.info('Lock: %s',c.v);logger.info('RLock: %s',rc.v)
def run_s():d=SemDemo(2);ts=[threading.Thread(target=d.access,args=(f'T-{i}',))for i in range(4)];[t.start()for t in ts];[t.join()for t in ts]
def run_q():d=QDemo();p=threading.Thread(target=d.produce,args=(['A','B','C',None],));c=threading.Thread(target=d.consume);p.start();c.start();p.join();c.join()
def download(url,dst):data=urlopen(url).read();Path(dst).write_bytes(data);logger.info('Downloaded %s',dst)
def process(path):logger.info('Processing %s',path);time.sleep(0.3);logger.info('Done %s',path)
def readf(path):t=Path(path).read_text(encoding='utf-8');logger.info('Read %d chars from %s',len(t),path)
def build():logger.info('Starting downloader');download('https://example.com','downloaded_page.html');logger.info('Starting jobs');
    with ThreadPoolExecutor(max_workers=3) as p:list(p.map(process,['img1.jpg','img2.jpg','img3.jpg']));logger.info('Starting reads');
    with ThreadPoolExecutor(max_workers=2) as p:list(p.map(readf,['Day04/multithreading_examples.py','Day04/async_examples.py']))
if __name__=='__main__':run_t();run_p();run_d();run_e();run_l();run_s();run_q();build()