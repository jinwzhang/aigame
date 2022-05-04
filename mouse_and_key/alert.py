import winsound
import time
import threading


class alarm:
    # 为了能够中途异步运行
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            winsound.Beep(600, 500)
            n -= 1
            time.sleep(0.5)


def alert():
    alarm1 = alarm()
    t = threading.Thread(target=alarm1.run, args=(10,))
    print('aleart initialize...')
    t.start()
    x = input('输入Y以终止警报：')
    if x.upper() == 'Y':
        alarm1.terminate()
        print('警报解除')
        t.join()
    else:
        t.join()
        alert()


if __name__ == '__main__':
    alert()
