import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLineEdit, QPushButton)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

# --- HEDGEHOG GÜVENLİK FİLTRESİ ---
BLOCKED = ["facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com"]
CLEAN_JS = "function h(){['#comments','ytd-comments','#chat','.live-chat','#secondary'].forEach(s=>{document.querySelectorAll(s).forEach(el=>el.remove())})}setInterval(h,2000);"

class SentinelPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if any(site in url.toString().lower() for site in BLOCKED): return False
        return True
    def createWindow(self, _type): return window.add_new_tab()

class HedgehogFirefox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel (Firefox Core)")
        self.resize(1200, 800)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda i: self.tabs.removeTab(i) if self.tabs.count() > 1 else None)
        self.setCentralWidget(self.tabs)
        
        # Navigasyon
        nav_widget = QWidget()
        nav_layout = QHBoxLayout(nav_widget)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        btn = QPushButton(" ➕ ")
        btn.clicked.connect(lambda: self.add_new_tab())
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(btn)
        
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(nav_widget)
        main_layout.addWidget(self.tabs)
        self.setCentralWidget(container)

        self.add_new_tab(QUrl("https://www.google.com"))

    def add_new_tab(self, qurl=None):
        if qurl is None: qurl = QUrl("https://www.google.com")
        b = QWebEngineView(); b.setPage(SentinelPage(b))
        b.loadFinished.connect(lambda: b.page().runJavaScript(CLEAN_JS))
        idx = self.tabs.addTab(b, "Yükleniyor...")
        self.tabs.setCurrentIndex(idx)
        b.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()) if self.tabs.currentWidget() == b else None)
        b.setUrl(qurl); return b

    def navigate(self):
        u = self.url_bar.text()
        url = u if "://" in u else ("https://www.google.com/search?q=" + u if "." not in u else "https://" + u)
        self.tabs.currentWidget().setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QWebEngineProfile.defaultProfile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0")
    window = HedgehogFirefox(); window.show(); sys.exit(app.exec())
