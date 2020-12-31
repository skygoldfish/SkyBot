import sys, os
import datetime, time
import win32com.client
import multiprocessing as mp
from multiprocessing import Process, Queue, Pipe

class XASessionEvents(object):
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def OnLogin(self, code, msg):
        if self.parent != None:
            self.parent.OnLogin(code, msg)

    def OnLogout(self):
        if self.parent != None:
            self.parent.OnLogout()

    def OnDisconnect(self):
        if self.parent != None:
            self.parent.OnDisconnect()

class XASession(object):
    def __init__(self, parent=None):
        self.ActiveX = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
        self.ActiveX.SetMode("_XINGAPI7_", "TRUE")

        if parent == None:
            self.ActiveX.set_parent(parent=self)
        else:
            self.ActiveX.set_parent(parent=parent)

    def login(self, url='demo.ebestsec.co.kr', port=200001, svrtype=0, id='userid', pwd='password', cert='공인인증 비밀번호'):
        result = self.ActiveX.ConnectServer(url, port)

        if not result:
            nErrCode = self.ActiveX.GetLastError()
            strErrMsg = self.ActiveX.GetErrorMessage(nErrCode)

            return False, nErrCode, strErrMsg

        self.ActiveX.Login(id, pwd, cert, svrtype, 0)

        return True, 0, "OK"

    def logout(self):
        self.ActiveX.Logout()

    def disconnect(self):
        self.ActiveX.DisconnectServer()

    def IsConnected(self):
        return self.ActiveX.IsConnected()

class RealTimeWorker(mp.Process):

    def __init__(self, producerQ, consumerQ):
        super(RealTimeWorker, self).__init__()

        self.inputQ = producerQ
        self.outputQ = consumerQ

        # win32com pickling error 발생!!!
        self.connection = XASession(parent=self)

        self.exit = mp.Event()
    '''
    def login(self):
        self.connection.login(url='demo.ebestsec.co.kr', id='goldrune', pwd='sky0000', cert='sky@1037045')

    def OnLogin(self, code, msg):

        if code == '0000':
            print('로그인 성공...')
    '''
    def run(self):
        while not self.exit.is_set():
            pass
            #print('process is alive...')
        print("You exited!")

    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()            