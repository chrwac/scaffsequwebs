

import sys
import threading

i=0
def test():
    global i
    i+=1
    print(i)
    test()

sys.setrecursionlimit(20000000)
threading.stack_size(64000000)
thread=threading.Thread(target=test)
thread.start()
thread.join()



#test()
