import threading
import queue
import random
import time

class UnlockProcessor:
    def __init__(self, processorNum=5):
        self.processorNum = processorNum
        self.createQs()
    
    def createQs(self):
        self.Qs = queue.Queue()

    def worker(self):
        while True:
            task = self.Qs.get()  # 取得任務
            if task is None:  # 如果是結束信號，退出循環
                break
            func, args, callback = task
            result = func(*args)  # 執行任務
            if callback:
                callback(result)  # 回調函數處理結果
            self.Qs.task_done()  # 標記任務完成

    def start(self):
        self.threads = []
        for _ in range(self.processorNum):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True  # 設定為守護進程
            thread.start()
            self.threads.append(thread)
    
    def add_task(self, func, args=(), callback=None):
        self.Qs.put((func, args, callback))  # 將任務加入隊列
    
    def wait_completion(self):
        self.Qs.join()  # 等待所有任務完成
    
    def stop(self):
        for _ in range(self.processorNum):
            self.Qs.put(None)  # 加入結束信號以終止線程
        for thread in self.threads:
            thread.join()


class ADDing(object):
    def add(self,A, B):
        time.sleep(1)
        result = A + B
        print(result)
        return  result
    
if __name__ == "__main__":
    ADDer = ADDing()
    random_numbersA = [random.randint(0, 100) for _ in range(100)]
    random_numbersB = [random.randint(0, 100) for _ in range(100)]
    processor = UnlockProcessor(processorNum=5)
    processor.start()

    for a, b in zip(random_numbersA, random_numbersB):
        processor.add_task(ADDer.add, args=(a, b), callback=None)

    # 等待所有任務完成
    processor.wait_completion()
    processor.stop()

