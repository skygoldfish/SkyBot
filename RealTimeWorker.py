import sys, os
import datetime, time
import multiprocessing as mp
from multiprocessing import Process, Queue, Pipe

from XASessions import *

class RealTimeWorker(mp.Process):

    def __init__(self, producerQ, consumerQ):
        super(RealTimeWorker, self).__init__()

        self.daemon = True

        self.inputQ = producerQ
        self.outputQ = consumerQ

        # win32com pickling error 발생!!!
        #self.connection = XASession(parent=self)

        self.exit = mp.Event()
    '''
    def login(self):
        self.connection.login(url='demo.ebestsec.co.kr', id='goldrune', pwd='sky0000', cert='sky@1037045')

    def OnLogin(self, code, msg):

        if code == '0000':
            print('로그인 성공...')
    '''
    def run(self):
        print('RealTimeWorker Start...')
        while not self.exit.is_set():
            pass
            #print('process is alive...')
        print("You exited!")

    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()            