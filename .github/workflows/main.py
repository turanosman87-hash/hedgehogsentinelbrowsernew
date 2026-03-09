import sys
from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLineEdit, QPushButton, QToolBar)
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView

# --- HEDGEHOG GÜVENLİK FİLTRESİ ---
BLOCKED = ["facebook.com", "fb.com", "instagram.com", "twitter.com", "x.com", "tiktok.com", "discord.com"]
# YouTube Temizleyici (Yorumlar ve Önerilenler Gider)
CLEAN_JS = "function h(){['#comments','ytd-comments','#chat','.live-chat','#secondary'].forEach(s=>{document.querySelectorAll(s).forEach(el=>el.remove())})}setInterval(h,2000);"

class SentinelPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        u = url.toString().lower()
        if any(site in u for site in BLOCKED):
            return False
        return True
    def createWindow(self, _type):
        return window.add_new_tab()

class HedgehogFirefox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel (Firefox Core)")
        self.resize(1300, 850)

        # Firefox stili sekme yapısı
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # Navigasyon Araç Çubuğu
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Firefox ile güvenle arayın...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        new_tab_btn = QPushButton("🦊 Yeni Sekme")
        new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        nav_bar.addWidget(new_tab_btn)

        # İlk sekmeyi aç
        self.add_new_tab(QUrl("https://www.google.com"), "Hedgehog Home")

    def add_new_tab(self, qurl=None, label="Yeni Sekme"):
        if qurl is None: qurl = QUrl("https://www.google.com")
        browser = QWebEngineView()
        page = SentinelPage(browser)
        browser.setPage(page)
        
        # YouTube Temizliğini Başlat
        browser.loadFinished.connect(lambda: browser.page().runJavaScript(CLEAN_JS))
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        
        browser.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()) if self.tabs.currentWidget() == browser else None)
        browser.titleChanged.connect(lambda t: self.tabs.setTabText(self.tabs.indexOf(browser), t[:15]))
        browser.setUrl(qurl)
        return browser

    def navigate_to_url(self):
        u = self.url_bar.text()
        if "." not in u: u = "https://www.google.com/search?q=" + u
        elif "://" not in u: u = "https://" + u
        self.tabs.currentWidget().setUrl(QUrl(u))

    def close_current_tab(self, i):
        if self.tabs.count() > 1: self.tabs.removeTab(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Firefox User Agent (Siteler bizi Firefox sansın)
    QWebEngineProfile.defaultProfile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0")
    global window
    window = HedgehogFirefox()
    window.show()
    sys.exit(app.exec())
