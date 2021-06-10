import os
import subprocess
from datetime import datetime

log_path = '/home/sotpurk/sotlogs/'

def findinfo(start, end, line):
    print(start, line)
    x = line[line.find(start) + len(start):line.find(end)].split('\n')[0]
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
            plotdeets['total'] = findinfo(total, ' sec', line)
    return plotdeets


def create(temporary_directory, destination_directory, threads, #buckets,
           chia_location='chia', temporary2_directory=None, farmer_public_key=None, pool_public_key=None):
    flags = dict(
        t=temporary_directory,
        d=destination_directory,
        r=threads,
        #u=buckets,
        n=1,
        p=pool_public_key,
        f=farmer_public_key,
       # 2=temporary2_directory,
    )
    data = [chia_location]
    for key, value in flags.items():
        flag = f'-{key}'
        data.append(flag)
        if value == '':
            continue
        data.append(str(value))
    log_file = open(log_name(log_path, findinfo('/mnt/', '/', temporary_directory), findinfo('/mnt/', '/', destination_directory)), 'a')
    process = subprocess.Popen(
        args=data,
        stdout=log_file,
        stderr=log_file,
        shell=False,
    )
    return process



def log_name(log_path, temp, plot):
    tp=temp+'_'+plot
    return os.path.join(log_path, f'{tp}_{str(datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_")}.log')

process=create( 
        chia_location="/home/sotpurk/madmaxplotter/chia-plotter/build/chia_plot",
        farmer_public_key="b356b66c75c8d0373a788ebe67436d6d9a3554845d80cc11142d3bdcd61971027509aaa14aac90122623d93ae43c3c25",
        pool_public_key="aabf91e79d29f767c6ae0494c4a6bea3f8ead35e94b57ea2ef621f92df981823b746f9eefb3a076144aaf957de52f779",
        temporary_directory='/mnt/temp2/',
        destination_directory='/mnt/plot8/',
        threads=4,
        #buckets=job.buckets,
)
