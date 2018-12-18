#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 00:21:21 2018

@author: arthur
"""

from Queue import Queue
import numpy as np
from threading import thread

#
#

def encoder():
    leitura = random.randint(0,50)
    print("Encoder: " + str(leitura) + " km/h")
    
def ultrassom():
    for i in range(0,50):
        leitura_ultra = random.randint(0,50)
    leitura = np.median(leitura_ultra)
    print("Ultrassom: " + str(leitura) + " m")
    
def gps():
    for i in range(0,50):
        leitura_ultra = random.randint(0,50)
    leitura = np.median(leitura_ultra)
    print("GPS lat: " + str(leitura) + " ")
    print("GPS long: " + str(leitura) + " ")

# Threaded function for queue processing.
def crawl(q, result):
    while not q.empty():
        work = q.get()                      #fetch new work from the Queue
        try:
            data = urlopen(work[1]).read()
            logging.info("Requested..." + work[1])
            result[work[0]] = data          #Store data back at correct index
        except:
            logging.error('Error with URL check!')
            result[work[0]] = {}
        #signal to the queue that task has been processed
        q.task_done()
    return True

leitura_ultra = []

#set up the queue to hold all the urls
q = Queue(maxsize=0)
# Use many threads (50 max, or one for each url)
num_theads = min(50, len(urls))

    #Populating Queue with tasks
    results = [{} for x in urls];
    #load up the queue with the urls to fetch and the index for each job (as a tuple):
    for i in range(len(urls)):
        #need the index and the url in each queue item.
        q.put((i,urls[i]))
        
for i in range(num_theads):
    logging.debug('Starting thread ', i)
    worker = Thread(target=crawl, args=(q,results))
    worker.setDaemon(True)    #setting threads as "daemon" allows main program to 
                              #exit eventually even if these dont finish 
                              #correctly.
    worker.start()
#now we wait until the queue has been processed
q.join()
logging.info('All tasks completed.')