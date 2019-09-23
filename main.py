import webview
import threading
import sys
from backend import start_server
from application_api import PlayerApi, LibraryApi

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window('Load CSS Example', "http://localhost:5000/", js_api=PlayerApi)
    webview.create_window('', 'http://localhost:5000/library', js_api=LibraryApi)
    webview.start(debug=True)
    sys.exit()
