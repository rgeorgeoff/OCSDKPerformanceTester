import queue
import subprocess
import threading

#03-06 23:06:59.005  2029  7905 I VrApi   : FPS=90/90,Prd=0ms,Tear=0,Early=0,Stale=0,Stale2/5/10/max=0/0/0/0,VSnc=0,
# Lat=-1,Fov=0,CPU4/GPU=4/4,1478/525MHz,OC=FF,TA=0/70/0,SP=N/F/N,Mem=2092MHz,Free=5350MB,PLS=0,Temp=31.0C/0.0C,TW=0.63ms,
# App=0.48ms,GD=0.00ms,CPU&GPU=0.74ms,LCnt=1(DR90,LM0),GPU%=0.12,CPU%=0.02(W0.05),DSF=1.00,CFL=14.67/19.84,LD=0
class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        assert isinstance(queue, queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()

def is_fps_line(line):
    return True

def update_fps(line):
    print(line)

def start_logger():
    # You'll need to add any command line arguments here.
    process = subprocess.Popen(["adb logcat -s VrApi"], stdout=subprocess.PIPE)

    # Launch the asynchronous readers of the process' stdout.
    stdout_queue = queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()

    # Check the queues if we received some output (until there is nothing more to get).
    while not stdout_reader.eof():
        while not stdout_queue.empty():
            line = stdout_queue.get()
            if is_fps_line(line):
                update_fps(line)
