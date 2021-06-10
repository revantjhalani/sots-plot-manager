import redis 
import glob
from time import sleep

r = redis.Redis(
    host='localhost',
    port=6379, 
    password='',
    decode_responses=True)

log_path = '/home/sotpurk/sotlogs/'

def findinfo(start, end, line):
    #print(start, line, end)
    x = line[line.find(start) + len(start):line.rfind(end)].split('\n')[0]
    return x
def readlog(filename):
    f = open(filename)
    plotdeets = {}
    config_dict = {}
    for line in f:
        if line.find('Phase') != -1:
            plotdeets[findinfo('Phase ', ' took ', line)]=findinfo(' took ', ' sec', line)
        pids = 'Process ID: '
        if line.find(pids) != -1:
            plotdeets['pid'] = findinfo(pids, '\n', line)
        temp = 'Working Directory:   '
        if line.find(temp) != -1:
            plotdeets['temp'] = findinfo(temp, '\n', line)
        threads = 'Number of Threads: '
        if line.find(threads) != -1:
            plotdeets['threads'] = findinfo(threads, '\n', line)
        dest = 'Final Directory: '
        if line.find(dest) != -1:
            plotdeets['dest'] = findinfo(dest, '\n', line)
        plot = 'Plot Name: '
        if line.find(plot) != -1:
            plotdeets['plot'] = findinfo(plot, '\n', line)
        copy= 'finished, took '
        if line.find(copy) != -1:
            plotdeets['copy'] = findinfo(copy, ' sec', line)
        total = 'Total plot creation time was '
        if line.find(total) != -1:
            plotdeets['5'] = findinfo(total, ' sec', line)
    return plotdeets


while True:  
    for file in glob.glob("logs/*.log"):
        r.hset('plots', file, str(readlog(file)))
#    for i in r.hgetall('plots'):
#        print(eval(r.hgetall('plots')[i])['5'])
    sleep(5)
