# Using queue and threading for unlocked data distribution
from tqdm import tqdm
import os,glob
import numpy as np
import queue, threading
import time

def testQcontent(queue,data):
    count = 0
    while True:
        print(f'queue : {queue} --> data {data}')
        time.sleep(1)
        count +=1
        if count >=5:
            break
    exit()

def createQ(data):
    newQ = queue.Queue()
    tF = threading.Thread(target = testQcontent, args = (newQ,data))
    tF.setDaemon(True)
    tF.start()
    return tF

def main():
    dataProcessOnce = 5
    dataNeedProcess = list(range(30))
    # detTxtDir = '/mnt/nas_shared/........'
    # detTxtPaths = glob.glob(detTxtDir+".txt")
    # lastInferenceFace = time.time()
    tfs = [createQ(dataNeedProcess[i]) for i in range(dataProcessOnce)]
    tfs_alive_status = [tf.is_alive() for tf in tfs]
    dataNeedProcess = dataNeedProcess[dataProcessOnce:]

    while True:
        
        for tfIdx,tf in enumerate(tfs):
            tfs_alive_status[tfIdx] = tf.is_alive()
            print(f'[main]  {tfIdx} alive ?',tfs_alive_status[tfIdx])
            if not tfs_alive_status[tfIdx]:
                if len(dataNeedProcess):
                    tfs[tfIdx] = createQ(dataNeedProcess[0])
                    dataNeedProcess = dataNeedProcess[1:]
                    # tfs_alive_status[tfIdx] = tfs[tfIdx].is_alive()
        if not len(dataNeedProcess):
            tfs_alive_status = [tf.is_alive() for tf in tfs]
            if not True in tfs_alive_status:
                exit()
        time.sleep(1)


if __name__ == '__main__':
    main()
