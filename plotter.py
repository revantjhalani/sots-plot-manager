import os 
import subprocess 
import redis
from datetime import datetime 

r = redis.Redis(
    host='localhost',
    port=6379, 
    password='password',
    decode_responses=True)

log_path = '/home/sotpurk/sotlogs/'

def findinfo(start, end, line):
    print(start, line, end)
    x = line[line.find(start) + len(start):line.rfind(end)].split('\n')[0]
    return x

def create(temporary_directory, destination_directory, threads, chia_location="/home/sotpurk/madmaxplotter/chia-plotter/build/chia_plot",
        farmer_public_key="b356b66c75c8d0373a788ebe67436d6d9a3554845d80cc11142d3bdcd61971027509aaa14aac90122623d93ae43c3c25",
        pool_public_key="aabf91e79d29f767c6ae0494c4a6bea3f8ead35e94b57ea2ef621f92df981823b746f9eefb3a076144aaf957de52f779" ):

    def log_name(log_path, temp, plot):
        tp=temp+'_'+plot
        return os.path.join(log_path, f'{tp}_{str(datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_")}.log')


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
