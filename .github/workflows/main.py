import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView

# --- HEDGEHOG SENTINEL AYARLARI ---
BLOCKED = ["facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com"]
CLEAN_JS = "function h(){['#comments','ytd-comments','#chat','.live-chat','#secondary'].forEach(s=>{document.querySelectorAll(s).forEach(el=>el.remove())})}setInterval(h,2000);"

class HedgehogBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel")
        self.resize(1200, 800)
        
        # Sekme Yapısı
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.setCentralWidget(self.tabs)
        
        # Araç Çubuğu
        nav = QWidget(); nl = QHBoxLayout(nav)
        self.url_bar = QLineEdit(); self.url_bar.returnPressed.connect(self.navigate)
        nl.addWidget(self.url_bar)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.create_toolbar())
        
        self.add_new_tab(QUrl("https://www.google.com"))

    def create_toolbar(self):
        # Basit bir navigasyon alanı
        pass 

    def add_new_tab(self, qurl):
        browser = QWebEngineView()
        # Engelleme Mekanizması
        browser.urlChanged.connect(lambda q: self.check_filter(q, browser))
        browser.loadFinished.connect(lambda: browser.page().runJavaScript(CLEAN_JS))
        idx = self.tabs.addTab(browser, "Yükleniyor...")
        browser.setUrl(qurl)
        return browser

    def check_filter(self, q, browser):
        url = q.toString().lower()
        if any(site in url for site in BLOCKED):
            browser.setHtml("<h1>Hedgehog Sentinel: Bu site engellendi.</h1>")

    def navigate(self):
        u = self.url_bar.text()
        self.tabs.currentWidget().setUrl(QUrl(u if "://" in u else "https://" + u))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QWebEngineProfile.defaultProfile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; rv:115.0) Gecko/20100101 Firefox/115.0")
    window = HedgehogBrowser()
    window.show()
    sys.exit(app.exec())
