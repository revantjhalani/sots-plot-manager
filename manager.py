from log import *
from time import sleep 
from plotter import *

def logloop():
    setlogs()
    sleep(5)

create(temporary_directory='/mnt/temp2/', destination_directory='/mnt/plot8/', threads=4)
