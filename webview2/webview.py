
from PySide6.QtCore import QUrl, Signal,QObject
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

import sys , os
import mitm
import  threading


__author__ = "https://github.com/its-me-abi"
__author__  = "16-4-2025"

"""
this is a pyside extention that provides http connection monitoring option to pyside6 webview widget
fully compatible with pyside6 webview so whenever you want to use webview use this instead orignal widget

Webview.on_http_connection willbe called everytime webview initiate http conenction
so you can create subclass and overrtde that fucntion to get connection events.

argument received on that method is mitmproxy's flow objects so 
please check mitmproxy addons documents to understand its structure
https://docs.mitmproxy.org/stable/api/mitmproxy/http.html#HTTPFlow

usage :
   import webview2.webview as webview
   import sys
   from PySide6.QtWidgets import QApplication
   from PySide6.QtCore import QUrl

   class mywebview ( Webview ):
        def on_http_connection (self, flow ) :
            print ( "connection received " )

   if __name__ == "__main__":
       app = QApplication(sys.argv)
       window = mywebview()
       window.setUrl(QUrl("https://www.python.org"))
       window.show()
       sys.exit(app.exec())
"""

class Interceptor(QWebEngineView):
    "this is a webview interceptor. it can monmitor all connections from webview"
    def __init__(self,*args,proxy = "http://127.0.0.1:8080",**kargs):
        super().__init__(*args,**kargs)
        self.setup_proxy(proxy)
        self.setWindowTitle("xrayapi v1.0 ")
        self.resize(700, 468)

    @staticmethod
    def setup_proxy(proxy):
        if proxy:
            os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = f"--proxy-server={proxy} --ignore-certificate-errors"
        else:
            os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = ""


class MitmAddon((QObject)):
    on_callback = Signal(object)
    def __init__(self, gui_callback=None):
        super().__init__()
        self.callback = gui_callback
        self.on_callback.connect(self.callback)

    def http_connect(self, flow):
        print("http cooect called")
        self.callback(flow)
        #self.on_callback.emit(flow)


    def request(self, flow):
        self.on_callback.emit(flow)

    def responce(self, flow):
        self.on_callback.emit(flow)

class Webview (Interceptor):
    "this is a pyside6 webview, use it instead inbuilt pyside6 webview"
    def __init__(self,*args,**kargs):
        self.UPSTREAM = ("127.0.0.1", 8082) #"http://127.0.0.1:8081"
        self.proxy = mitm.MitmProxyManager(host="127.0.0.1",port=8080)
        self.addon = MitmAddon(gui_callback=self.on_http_connection)
        self.proxy.add_addon(self.addon)
        self.mitm_thread = threading.Thread( target=self.proxy.start)
        self.mitm_thread.start()
        super().__init__(*args, **kargs)

    def load_new_url(self, url):
        super().setUrl(QUrl(url))

    def on_http_connection(self, flow):
        "you can override this  method to monitor save conenction reauests and responces"
        print( " *********************** request received *****************" )
        if not flow.response:
            print( "Responce not received " )


class mywebview ( Webview ):
    def on_http_connection (self, flow ) :
        print ( "connection received " )

if __name__ == "__main__":
       app = QApplication(sys.argv)
       window = mywebview()
       window.setUrl(QUrl("https://www.python.org"))
       window.show()
       sys.exit(app.exec())
