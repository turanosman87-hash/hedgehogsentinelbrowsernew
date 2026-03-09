import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

# Engelleme Listesi
BLOCKED = ["facebook.com", "instagram.com", "twitter.com", "tiktok.com"]

class SentinelPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if any(site in url.toString().lower() for site in BLOCKED):
            return False
        return True

class HedgehogBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel")
        self.resize(1100, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        layout.addWidget(self.url_bar)
        
        self.browser = QWebEngineView()
        self.browser.setPage(SentinelPage(self.browser))
        layout.addWidget(self.browser)
        
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate(self):
        u = self.url_bar.text()
        url = u if "://" in u else "https://" + u
        self.browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HedgehogBrowser()
    window.show()
    sys.exit(app.exec())
