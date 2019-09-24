import webview
import threading
import sys
from sqlalchemy import create_engine

from backend import start_server
from application_api import PlayerApi, LibraryApi
from models import Base

if __name__ == '__main__':
    # Base = declarative_base()
    engine = create_engine('sqlite:///music.db')
    Base.metadata.create_all(engine)

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window('Load CSS Example', "http://localhost:5000/", js_api=PlayerApi)
    webview.create_window('Library', 'http://localhost:5000/library', js_api=LibraryApi)
    webview.start(debug=True)
    # sys.exit()
