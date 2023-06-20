import threading 

def function1():
    for x in range(1,20000000000000000):
        print(x)
def function2():
    for y in range(500,1000000000):
        print(y)

thread1 = threading.Thread(target = function1)
thread2 = threading.Thread(target = function2)

thread1.start()
print('hello')
thread2.start()

thread1.join()
thread2.join()